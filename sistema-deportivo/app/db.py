from contextlib import contextmanager
import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Devuelve una conexión nueva a MySQL.

    Usala directamente cuando necesites controlar la transacción a mano
    (por ejemplo, inscripciones con SELECT ... FOR UPDATE)."""
    conn = mysql.connector.connect(**DB_CONFIG)
    # Forzar UTF-8 en la conexión
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8mb4")
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.close()
    return conn


@contextmanager
def get_cursor(commit=False, dictionary=True):
    """Abre conexión + cursor y los cierra solo.

    - commit=True  -> confirma los cambios (usar en INSERT/UPDATE/DELETE)
    - dictionary=True -> cada fila vuelve como dict {columna: valor}

    Si algo falla, hace rollback y relanza el error."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

# Ejemplo de uso: 
# dentro de disciplina_repo.py podríamos tener algo como esto para listar disciplinas:
# from app.db import get_cursor

# def listar():
#     with get_cursor() as cur:
#         cur.execute("SELECT id_disciplina, nombre FROM disciplina ORDER BY nombre")
#         return cur.fetchall()
