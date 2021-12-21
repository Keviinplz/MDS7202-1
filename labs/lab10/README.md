# Laboratorio 10

## Datos Personales

```
Kevin Pinochet Hernández
https://github.com/Keviinplz/MDS7202-1
```

## How to run
Los archivos y directorios están dispuestos de la siguiente forma
```bash
├── Lab10.ipynb        ---------------> Jupyter del Laboratorio
├── README.md          ---------------> Ésta documentación
├── api                ---------------> Carpeta con el código de la API
├── data               ---------------> Data del Laboratorio
├── main.py            ---------------> Archivo principal de la app
├── super_model.joblib ---------------> Modelo de SKLearn
├── owo_database.json  ---------------> Base de datos que usará la aplicación
├── poetry.lock        ---------------> Archivos de poetry, ignorar
├── pyproject.toml     ---------------> Archivos de poetry, ignorar
└── tests              ---------------> Tests de la aplicación
```

Para correr la aplicación, primero se debe instalar los requerimientos que están en `requirements.txt`, la aplicación se programó usando `Python 3.6.9`.

```bash
python3 -m pip install -r requirements.txt
```

Luego se debe definir el nombre del modelo (en este ejemplo es `super_model.joblib`) y de la base de datos (en este ejemplo es `owo_database.json`), estas deben estar en la raíz de la aplicación, como se ve en la lista de ficheros del ejemplo anterior.

Luego, se debe dirigir a `api/config.py` y modificar lo siguiente:

```py
class ApplicationConfig(BaseSettings):
    model: str = os.getenv("MODEL_NAME", "super_model.joblib") # modificar por su modelo
    database: str = os.getenv("DATABASE_NAME", "owo_database.json") # modificar por su db
```

Si su modelo se llama `my_model.joblib` y su base de datos es `my_database.json`, entonces lo anterior se ve de la siguiente forma:

```py
class ApplicationConfig(BaseSettings):
    model: str = os.getenv("MODEL_NAME", "my_model.joblib")
    database: str = os.getenv("DATABASE_NAME", "my_database.json")
```

Y listo, ya puede correr la aplicación
```bash
uvicorn main:api
```

## Tests

La aplicación está testeada con todas las funcionalidades requeridas en el laboratorio, para correr los tests, ejecute lo siguiente:

```bash
pytest
```

Los tests crean una base de datos de prueba llamada `db_testing.json` por lo que no interfiere con la base de datos original (a menos que se use el mismo nombre para producción).