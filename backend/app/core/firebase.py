"""Firebase initialization (optional).

Provides function to initialize Firebase only if credentials exist, so
WebSocket/local development works without cloud setup.
"""
from __future__ import annotations

import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore, storage
from typing import Optional

from .config import Settings

logger = logging.getLogger(__name__)


class FirebaseResources:
    def __init__(self, app: firebase_admin.App):
        self.app = app
        self.db = firestore.client()
        self.bucket = storage.bucket()


def init_firebase(settings: Settings) -> Optional[FirebaseResources]:
    cred_path = settings.FIREBASE_CREDENTIALS_PATH
    if not cred_path or not os.path.isfile(cred_path):
        logger.info("Firebase credentials not found; skipping Firebase init.")
        return None
    try:
        cred = credentials.Certificate(cred_path)  # type: ignore[arg-type]
        firebase_app = firebase_admin.initialize_app(cred, {
            'storageBucket': settings.FIREBASE_STORAGE_BUCKET,
            'databaseURL': settings.FIREBASE_DATABASE_URL
        })
        logger.info("Firebase initialized.")
        return FirebaseResources(firebase_app)
    except Exception as e:  # pragma: no cover - defensive
        logger.warning(f"Firebase init failed: {e}")
        return None


def shutdown_firebase(resources: Optional[FirebaseResources]) -> None:
    if resources:
        firebase_admin.delete_app(resources.app)
        logger.info("Firebase app deleted.")
