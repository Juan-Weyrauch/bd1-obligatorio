# config.py: lee el .env y deja la configuración lista. 
# Ningún otro archivo vuelve a leer variables de entorno.

import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env
load_dotenv()


class Config:
    """Configuración general de la app Flask."""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-inseguro")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"


# Parámetros de conexión a MySQL (los usa app/db.py)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "deportes_db"),
}