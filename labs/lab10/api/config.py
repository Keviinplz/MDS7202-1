import os

from pydantic import BaseSettings

class ApplicationConfig(BaseSettings):
    model: str = os.getenv("MODEL_NAME", "modelo.joblib")
    database: str = os.getenv("DATABASE_NAME", "db.json")