from typing import List, Tuple

import pytest
from tinydb import TinyDB
from httpx import AsyncClient

from tests.utils import get_points_data

pytestmark = pytest.mark.asyncio

@pytest.fixture()
async def app_poblated(app: Tuple[AsyncClient, TinyDB]):
    """
    Poblamos la base de datos de prueba, y luego retornamos la misma app,
    así los tests que requieran datos los tendrán
    """

    app[1].insert_multiple(get_points_data())
    yield app[0]

# Hago esto para que los tests sean legibles, sino nimodo
POINT_DATA: List[dict] = get_points_data()

async def test_get_predictions(app_poblated: AsyncClient):
    response = await app_poblated.get("/potabilidad/")
    assert response.status_code == 200
    assert response.json() == POINT_DATA

    response = await app_poblated.get("/potabilidad_diaria/?day=18&month=7&year=2021")
    assert response.status_code == 200
    assert response.json() == []

    response = await app_poblated.get("/potabilidad_diaria/?day=16&month=7&year=2021")
    assert response.status_code == 200
    assert response.json() == [data for data in POINT_DATA if data["Day"] == 16]

    response = await app_poblated.get("/potabilidad_diaria/?day=17&month=7&year=2021")
    assert response.status_code == 200
    assert response.json() == [data for data in POINT_DATA if data["Day"] == 17]