""" 
Aplicación Principal

Las rutas están definidas en api/routers, 
como veran, son las mismas que las solicitadas en en lab.

Dado el como funciona FastAPI, tuve que separar la ruta `potabilidad_diaria`
puesto que no se pueden crear rutas que no partan com `/` y que terminen con `/` en el
objeto router.

Escribí un README.md con la documentación de la aplicación.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from api.exceptions.pydantic import pydantic_validation_exception_handler
from api.routers.potabilidad import router as potabilidad_router
from api.routers.diaria import router as potabilidad_diaria_router

api: FastAPI = FastAPI(title="Lab 10")

# Incluimos las rutas
api.include_router(potabilidad_router)
api.include_router(potabilidad_diaria_router)

api.add_exception_handler(RequestValidationError, pydantic_validation_exception_handler)