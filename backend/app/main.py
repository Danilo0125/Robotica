import firebase_admin
from firebase_admin import credentials, firestore, storage
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import Settings
import os

# Load settings
settings = Settings()

# Initialize Firebase
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Firebase on startup
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_app = firebase_admin.initialize_app(cred, {
        'storageBucket': settings.FIREBASE_STORAGE_BUCKET,
        'databaseURL': settings.FIREBASE_DATABASE_URL
    })
    
    # Make Firebase instances available to the app
    app.state.db = firestore.client()
    app.state.bucket = storage.bucket()
    
    yield
    
    # Clean up on shutdown
    firebase_admin.delete_app(firebase_app)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Basic routes
@app.get("/")
async def root():
    return {"message": "Welcome to Robotica Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.VERSION}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process the data here
            await manager.broadcast(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client disconnected")

# You can add more routes and functionality here
