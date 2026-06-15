"""Capa de datos para la entidad Carrera."""
from app.db import get_cursor


def listar():
    """Todas las carreras, con su facultad, ordenadas por nombre."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT c.id_carrera, c.nombre, c.id_facultad, f.nombre AS facultad_nombre
            FROM carrera c
            JOIN facultad f ON f.id_facultad = c.id_facultad
            ORDER BY c.nombre
            """
        )
        return cur.fetchall()


def obtener_por_id(id_carrera):
    """Una carrera por su PK, o None si no existe."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT id_carrera, nombre, id_facultad
            FROM carrera
            WHERE id_carrera = %s
            """,
            (id_carrera,),
        )
        return cur.fetchone()


def existe_nombre(nombre, excluir_id=None):
    """True si ya hay una carrera con ese nombre."""
    with get_cursor() as cur:
        if excluir_id is None:
            cur.execute(
                "SELECT 1 FROM carrera WHERE nombre = %s",
                (nombre,),
            )
        else:
            cur.execute(
                "SELECT 1 FROM carrera WHERE nombre = %s AND id_carrera <> %s",
                (nombre, excluir_id),
            )
        return cur.fetchone() is not None


def crear(nombre, id_facultad):
    """Inserta una carrera y devuelve su id autogenerado."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "INSERT INTO carrera (nombre, id_facultad) VALUES (%s, %s)",
            (nombre, id_facultad),
        )
        return cur.lastrowid


def actualizar(id_carrera, nombre, id_facultad):
    """Actualiza nombre y facultad. Devuelve filas afectadas."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            UPDATE carrera
            SET nombre = %s, id_facultad = %s
            WHERE id_carrera = %s
            """,
            (nombre, id_facultad, id_carrera),
        )
        return cur.rowcount


def eliminar(id_carrera):
    """Elimina una carrera. Puede lanzar IntegrityError por FK."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "DELETE FROM carrera WHERE id_carrera = %s",
            (id_carrera,),
        )
        return cur.rowcount
