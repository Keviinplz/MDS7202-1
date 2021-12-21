from fastapi import Depends
from joblib import load
from sklearn.ensemble import BaggingClassifier

from .config import get_config
from ..config import ApplicationConfig

async def get_model(config: ApplicationConfig = Depends(get_config)) -> BaggingClassifier:
    model: BaggingClassifier = load(config.model)
    yield model