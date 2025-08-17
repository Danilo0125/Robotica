"""Basic HTTP routes."""
from __future__ import annotations
from fastapi import APIRouter
from app.core.config import Settings

router = APIRouter()
settings = Settings()


@router.get("/")
async def root():
    return {"message": "Welcome to Robotica Backend API"}


@router.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.VERSION}
