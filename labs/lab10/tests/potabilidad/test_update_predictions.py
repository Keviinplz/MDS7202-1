from typing import List, Tuple

import pytest
from tinydb import TinyDB, Query
from httpx import AsyncClient

from tests.utils import get_points_data

pytestmark = pytest.mark.asyncio

async def test_update_predictions_by_day(app: Tuple[AsyncClient, TinyDB]):
    client, db = app
    db.insert_multiple(get_points_data())
    q = Query()
    
    inserted_ids = [d.doc_id for d in db.search((q.Day == 20) & (q.Month == 7) & (q.Year == 2021))]
    response = await client.put(
        "/potabilidad/?day=20&month=7&year=2021&new_prediction=1"
    )
    assert response.status_code == 200
    assert response.json() == {"success": True, "updated_elements": sorted(inserted_ids)}

    documents = db.search(q.id.one_of(inserted_ids))
    for document in documents:
        assert document["Prediction"] == 1
