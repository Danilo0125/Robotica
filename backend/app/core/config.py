import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH") # pyright: ignore[reportAssignmentType]
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_DATABASE_URL: str = os.getenv("FIREBASE_DATABASE_URL")
    FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET")
    FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY")
    FIREBASE_AUTH_DOMAIN: str = os.getenv("FIREBASE_AUTH_DOMAIN")
    FIREBASE_MESSAGING_SENDER_ID: str = os.getenv("FIREBASE_MESSAGING_SENDER_ID")
    FIREBASE_APP_ID: str = os.getenv("FIREBASE_APP_ID")

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5432"))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")

    API_HOST: str = os.getenv("API_HOST")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
    ALLOWED_METHODS: list[str] = os.getenv("ALLOWED_METHODS", "").split(",") if os.getenv("ALLOWED_METHODS") else []
    ALLOWED_HEADERS: list[str] = os.getenv("ALLOWED_HEADERS", "*").split(",") if os.getenv("ALLOWED_HEADERS") else ["*"]
    REDIS_URL: str = os.getenv("REDIS_URL")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_USER: str = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    APP_NAME: str = os.getenv("APP_NAME")
    VERSION: str = os.getenv("VERSION")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)