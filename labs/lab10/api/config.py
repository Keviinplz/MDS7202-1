import os

from pydantic import BaseSettings

class ApplicationConfig(BaseSettings):
    model: str = os.getenv("MODEL_NAME", "super_model.joblib")
    database: str = os.getenv("DATABASE_NAME", "owo_database.json")