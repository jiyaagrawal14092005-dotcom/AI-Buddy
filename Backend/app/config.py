import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)


class Settings:

    PROJECT_NAME = "AI Buddy"

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ).lower() == "true"

    HOST = os.getenv(
        "HOST",
        "127.0.0.1"
    )

    PORT = int(
        os.getenv(
            "PORT",
            "8000"
        )
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        ""
    )

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-in-production"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "60"
        )
    )

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173"
    )

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173"
        ).split(",")
        if origin.strip()
    ]

    @classmethod
    def get_status(cls) -> dict:

        return {
            "project_name": cls.PROJECT_NAME,
            "environment": cls.ENVIRONMENT,
            "debug": cls.DEBUG,
            "host": cls.HOST,
            "port": cls.PORT,
            "gemini_configured": bool(
                cls.GEMINI_API_KEY
            ),
            "database_configured": bool(
                cls.DATABASE_URL
            ),
            "frontend_url": cls.FRONTEND_URL
        }


settings = Settings()