"""Capa de datos para la entidad Facultad.
Unica capa autorizada a escribir SQL para esta entidad."""
from app.db import get_cursor


def listar():
    """Todas las facultades, ordenadas por nombre."""
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_facultad, nombre FROM facultad ORDER BY nombre"
        )
        return cur.fetchall()


def obtener_por_id(id_facultad):
    """Una facultad por su PK, o None si no existe."""
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_facultad, nombre FROM facultad WHERE id_facultad = %s",
            (id_facultad,),
        )
        return cur.fetchone()


def existe_nombre(nombre, excluir_id=None):
    """True si ya hay una facultad con ese nombre."""
    with get_cursor() as cur:
        if excluir_id is None:
            cur.execute(
                "SELECT 1 FROM facultad WHERE nombre = %s",
                (nombre,),
            )
        else:
            cur.execute(
                "SELECT 1 FROM facultad WHERE nombre = %s AND id_facultad <> %s",
                (nombre, excluir_id),
            )
        return cur.fetchone() is not None


def crear(nombre):
    """Inserta una facultad y devuelve su id autogenerado."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "INSERT INTO facultad (nombre) VALUES (%s)",
            (nombre,),
        )
        return cur.lastrowid


def actualizar(id_facultad, nombre):
    """Actualiza el nombre. Devuelve cantidad de filas afectadas."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "UPDATE facultad SET nombre = %s WHERE id_facultad = %s",
            (nombre, id_facultad),
        )
        return cur.rowcount


def eliminar(id_facultad):
    """Elimina una facultad. Puede lanzar IntegrityError por FK."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "DELETE FROM facultad WHERE id_facultad = %s",
            (id_facultad,),
        )
        return cur.rowcount
