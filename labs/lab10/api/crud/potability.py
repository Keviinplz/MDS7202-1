from datetime import datetime
from typing import List, Optional

import pandas as pd
from tinydb import TinyDB, Query
from tinydb.operations import set
from fastapi.encoders import jsonable_encoder
from sklearn.ensemble import BaggingClassifier

from ..schemas.potability import (
    DeletePredictionResponse,
    PotabilityPrediction,
    PotabilityToPredict,
    PredictionInDB,
    UpdatePredictionResponse,
)


async def make_prediction(
    data: PotabilityToPredict, model: BaggingClassifier, database: TinyDB
) -> PotabilityPrediction:
    predict: List[int] = int(
        model.predict(pd.DataFrame(jsonable_encoder([data.dict()])))[0]
    )
    now = datetime.now()

    inserted_id: int = database.insert(
        {
            **data.dict(),
            "Prediction": predict,
            "Day": now.day,
            "Month": now.month,
            "Year": now.year,
        }
    )
    return PotabilityPrediction(id=inserted_id, prediction=predict)


async def get_predictions(
    database: TinyDB,
    day: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
) -> List[PredictionInDB]:
    data: List[dict] = []
    if day is not None and month is not None and year is not None:
        q = Query()
        data = database.search((q.Day == day) & (q.Month == month) & (q.Year == year))
    else:
        data = database.all()

    return [PredictionInDB(**db_data) for db_data in data]


async def update_prediction(
    database: TinyDB, day: int, month: int, year: int, new_prediction: int
) -> UpdatePredictionResponse:
    q = Query()
    updated_elements: List[int] = database.update(
        set("Prediction", new_prediction),
        (q.Day == day) & (q.Month == month) & (q.Year == year),
    )
    return UpdatePredictionResponse(
        success=True, updated_elements=sorted(updated_elements)
    )


async def delete_prediction(
    database: TinyDB, day: int, month: int, year: int
) -> DeletePredictionResponse:
    q = Query()
    deleted_elements: List[int] = database.remove(
        (q.Day == day) & (q.Month == month) & (q.Year == year)
    )
    return DeletePredictionResponse(
        success=True, deleted_elements=sorted(deleted_elements)
    )
