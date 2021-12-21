from typing import List
from pydantic import BaseModel

class PotabilityToPredict(BaseModel):
    """ Información que representa un punto de potabilidad a predecir. """

    # no me gusta escribir los atributos partiendo con mayuscula uwu
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

class PotabilityPrediction(BaseModel):
    """ Información que representa la predicción de potabilidad entregada por el modelo. """
    
    id: int
    prediction: int

class PredictionInDB(PotabilityToPredict):
    """ Información que representa una predicción almacenada en la base de datos. """

    Day: int
    Month: int
    Year: int
    Prediction: int

class UpdatePredictionResponse(BaseModel):
    """ Información que representa una respuesta al actualizar una predicción. """

    success: bool = True
    updated_elements: List[int]

class DeletePredictionResponse(BaseModel):
    """ Información que representa una respuesta al eliminar una predicción. """

    success: bool = True
    deleted_elements: List[int]