import random
from typing import List, Tuple

import pytest
from tinydb import TinyDB
from httpx import AsyncClient

from api.schemas.potability import PotabilityToPredict
from tests.utils import complement

# Esto marca todos los tests para que pytest los corra usando el backend de asyncio
# una librería de asyncronía de python.
pytestmark = pytest.mark.asyncio

async def test_make_prediction_with_no_data(app: Tuple[AsyncClient, TinyDB]):
    response = await app[0].post("/potabilidad/")
    assert response.status_code == 422
    assert response.json() == {"message": "No se ha proporcionado datos."}

    response = await app[0].post("/potabilidad/", json={})
    assert response.status_code == 422
    assert response.json() == {"message": "No se ha proporcionado datos."}


async def test_make_prediction_with_fields_that_are_not_exists(app: Tuple[AsyncClient, TinyDB]):
    fields: List[str] = PotabilityToPredict.schema()["required"]
    fields.sort()

    # Debe retornar que faltan todos los campos
    response = await app[0].post("/potabilidad/", json={"uwu": "owo"})
    assert response.status_code == 400
    assert response.json() == {
        "message": "Faltan campos obligatorios.",
        "missing": fields,
    }


async def test_make_prediction_with_missing_fields(app: Tuple[AsyncClient, TinyDB]):
    fields: List[str] = PotabilityToPredict.schema()["required"]
    fields.sort()

    for fieldset in [
        random.sample(fields, random.randint(1, len(fields) - 1)) for _ in range(100)
    ]:
        missing = complement(fields, fieldset)
        missing.sort()

        response = await app[0].post(
            "/potabilidad/", json={field: random.random() for field in fieldset}
        )
        assert response.status_code == 400
        assert response.json() == {
            "message": "Faltan campos obligatorios.",
            "missing": missing,
        }


async def test_make_prediction_with_valid_data(app: Tuple[AsyncClient, TinyDB]):
    response = await app[0].post(
        "/potabilidad/",
        json={
            "ph": 10.316400384553162,
            "Hardness": 217.2668424334475,
            "Solids": 10676.508475429378,
            "Chloramines": 3.445514571005745,
            "Sulfate": 397.7549459751925,
            "Conductivity": 492.20647361771086,
            "Organic_carbon": 12.812732207582542,
            "Trihalomethanes": 72.28192021570328,
            "Turbidity": 3.4073494284238364,
        },
    )
    assert response.status_code == 200
    point_id = response.json()["id"]
    point = app[1].get(doc_id=point_id)

    assert point is not None
    assert response.json() == {"id": point_id, "prediction": 0}
