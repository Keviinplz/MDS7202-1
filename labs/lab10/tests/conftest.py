import os
import asyncio

import pytest
from httpx import AsyncClient
from tinydb import TinyDB

from main import api
from api.dependencies.config import get_config, override_get_config

@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()



@pytest.fixture(scope="session", autouse=True)
async def create_test_database(event_loop):
    """
    Crea una base de datos JSON de prueba antes de los tests.
    Se asegura de que cada test corra con una base de datos limpia.
    """

    if os.path.exists("db_testing.json"):
        os.remove("db_testing.json")
    db = TinyDB("db_testing.json")
    db.all()  # TinyDB al parecer es lazy, así que con esto fuerzo a que cree el archivo .json
    yield  # Aquí correrán los tests
    db.close() # Cierro el cursor, siempre es bueno cerrar los archivos uwu
    try:
        os.remove("db_testing.json") # Elimino la base de datos de prueba
    except PermissionError:
        pass 


@pytest.fixture()
async def app():
    """
    Creamos una fixture que retorne una instancia de la API para los casos de Test,
    La idea es que más adelante sea sencillo crear una base de datos de testing
    usando esta API.

    Ejemplo de uso:

    ```python
    async def test_get_predictions(app):
        response = await app.get("/potabilidad/")
        assert response.status_code == 200
        assert response.json() == {"message": "working"}
    ```
    """
    # Usamos la base de datos de prueba que creamos en la fixture anterior
    api.dependency_overrides[get_config] = override_get_config

    db = TinyDB("db_testing.json") # Para que los tests solo usen una instancia de TinyDB
    db.clear_cache() # Limpio la cache de TinyDB
    async with AsyncClient(app=api, base_url="http://test") as client:
        yield (client, db)  # Los tests correran usando esta aplicación
    db.clear_cache() # Limpio la cache de TinyDB
    db.truncate()