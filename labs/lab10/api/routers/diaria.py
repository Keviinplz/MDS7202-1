from typing import List

from tinydb import TinyDB
from fastapi import APIRouter, Depends

from ..dependencies.database import get_database
from ..crud.potability import get_predictions
from ..schemas.potability import PredictionInDB

router = APIRouter(prefix="/potabilidad_diaria", tags=["Predicciones de Potabilidad"])

@router.get('/', response_model=List[PredictionInDB])
async def read_by_day(day: int, month: int, year: int, db: TinyDB = Depends(get_database)):
    data: List[PredictionInDB] = await get_predictions(db, day, month, year)
    return data