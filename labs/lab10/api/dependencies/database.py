from tinydb import TinyDB
from fastapi import Depends

from .config import get_config
from ..config import ApplicationConfig

async def get_database(config: ApplicationConfig = Depends(get_config)):
    db = TinyDB(config.database)
    yield db