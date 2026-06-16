"""Capa de datos para la entidad Asistencia."""
from app.db import get_cursor


def crear(id_inscripcion, fecha, presente):
    """Inserta una asistencia y devuelve su id autogenerado.
    Puede lanzar IntegrityError si ya existe (UNIQUE id_inscripcion + fecha)."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO asistencia (id_inscripcion, fecha, presente)
            VALUES (%s, %s, %s)
            """,
            (id_inscripcion, fecha, presente),
        )
        return cur.lastrowid
