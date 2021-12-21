""" Módulo que gestiona las excepciones de pydantic """
from typing import List

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError

from fastapi.responses import JSONResponse

async def pydantic_validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """ Handler para los errores de validación de pydantic capturados por FastAPI """
    fields: List[str] = [field["loc"][-1] for field in exc.errors()]
    fields.sort()

    if not exc.body:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "No se ha proporcionado datos."},
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Faltan campos obligatorios.", "missing": fields},
    )