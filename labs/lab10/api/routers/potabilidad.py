from typing import List

from tinydb import TinyDB
from fastapi import APIRouter
from fastapi import Depends
from sklearn.ensemble import BaggingClassifier

from ..dependencies.database import get_database
from ..dependencies.model import get_model
from ..crud.potability import (
    make_prediction,
    get_predictions,
    update_prediction,
    delete_prediction,
)
from ..schemas.potability import (
    PotabilityPrediction,
    PotabilityToPredict,
    PredictionInDB,
    UpdatePredictionResponse,
    DeletePredictionResponse,
)

router = APIRouter(prefix="/potabilidad", tags=["Predicciones de Potabilidad"])


@router.get("/", response_model=List[PredictionInDB])
async def read_all(db: TinyDB = Depends(get_database)):
    data: List[PredictionInDB] = await get_predictions(database=db)
    return data


@router.post("/", response_model=PotabilityPrediction)
async def predict_and_save(
    data: PotabilityToPredict,
    model: BaggingClassifier = Depends(get_model),
    db: TinyDB = Depends(get_database),
):
    prediction: PotabilityPrediction = await make_prediction(data, model, db)
    return prediction


@router.put("/", response_model=UpdatePredictionResponse)
async def update_by_day(
    day: int,
    month: int,
    year: int,
    new_prediction: int,
    db: TinyDB = Depends(get_database),
):
    response: UpdatePredictionResponse = await update_prediction(
        db, day, month, year, new_prediction
    )
    return response


@router.delete("/", response_model=DeletePredictionResponse)
async def delete_by_day(
    day: int,
    month: int,
    year: int,
    db: TinyDB = Depends(get_database),
):
    response: UpdatePredictionResponse = await delete_prediction(db, day, month, year)
    return response
