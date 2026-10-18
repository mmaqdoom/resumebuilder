import os
from pathlib import Path


def get_database_url():
    database_url = (
        os.environ.get("NEON_DATABASE_URL")
        or os.environ.get("DATABASE_URL")
        or os.environ.get("Database_Url")
    )
    if not database_url:
        for key, val in os.environ.items():
            if key.lower() == "neon_database_url" and val.strip():
                database_url = val.strip()
                break
        if not database_url:
            for key, val in os.environ.items():
                if key.lower() == "database_url" and val.strip():
                    database_url = val.strip()
                    break

    database_url = (
        (database_url and database_url.strip())
        or f"sqlite:///{Path(__file__).resolve().parent / 'instance' / 'resume_builder.db'}"
    )
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # Resend API Configuration (Recommended & Secure)
    RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
    RESEND_FROM_EMAIL = os.environ.get(
        "RESEND_FROM_EMAIL",
        os.environ.get("MAIL_DEFAULT_SENDER", "ResumeBuilder <onboarding@resend.dev>"),
    )

    # Legacy SMTP Configuration (Fallback)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER", "ResumeBuilder <noreply@resumebuilder.com>"
    )
