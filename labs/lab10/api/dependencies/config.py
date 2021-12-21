from ..config import ApplicationConfig

async def get_config():
    return ApplicationConfig()

async def override_get_config():
    return ApplicationConfig(database="db_testing.json")