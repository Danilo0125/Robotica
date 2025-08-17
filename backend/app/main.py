from contextlib import asynccontextmanager
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings
from app.core.firebase import init_firebase, shutdown_firebase
from app.api.routes import all_http_routers
from app.websocket.endpoints import ws_router
from app.auth import router as auth_router
from app.robot import router as robot_router

settings = Settings()
logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    firebase_resources = init_firebase(settings)
    if firebase_resources:
        app.state.db = firebase_resources.db
        app.state.bucket = firebase_resources.bucket
    yield
    shutdown_firebase(firebase_resources)


app = FastAPI(title=settings.APP_NAME, version=settings.VERSION, lifespan=lifespan)

allow_origins = settings.ALLOWED_ORIGINS or ["*"]
allow_methods = settings.ALLOWED_METHODS or ["*"]
allow_headers = settings.ALLOWED_HEADERS or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

for r in all_http_routers:
    app.include_router(r)
app.include_router(auth_router)
app.include_router(robot_router)
app.include_router(ws_router)

logger.info("HTTP + WebSocket endpoints registered.")
