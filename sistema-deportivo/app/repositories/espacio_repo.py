"""Capa de datos para la entidad Espacio.
Única capa autorizada a escribir SQL para esta entidad.
Regla de oro: SIEMPRE consultas parametrizadas con %s. Nunca f-strings."""
from app.db import get_cursor


def listar():
    """Todos los espacios, ordenados por nombre."""
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_espacio, nombre, ubicacion FROM espacio ORDER BY nombre"
        )
        return cur.fetchall()


def obtener_por_id(id_espacio):
    """Un espacio por su PK, o None si no existe."""
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_espacio, nombre, ubicacion FROM espacio WHERE id_espacio = %s",
            (id_espacio,),
        )
        return cur.fetchone()


def existe(nombre, ubicacion, excluir_id=None):
    """True si ya hay un espacio con ese nombre y ubicación.
    excluir_id permite ignorar la propia fila al editar.
    La combinación (nombre, ubicacion) es UNIQUE en la BD."""
    with get_cursor() as cur:
        if excluir_id is None:
            cur.execute(
                "SELECT 1 FROM espacio WHERE nombre = %s AND ubicacion = %s",
                (nombre, ubicacion),
            )
        else:
            cur.execute(
                "SELECT 1 FROM espacio WHERE nombre = %s AND ubicacion = %s AND id_espacio <> %s",
                (nombre, ubicacion, excluir_id),
            )
        return cur.fetchone() is not None


def crear(nombre, ubicacion):
    """Inserta un espacio y devuelve su id autogenerado."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "INSERT INTO espacio (nombre, ubicacion) VALUES (%s, %s)",
            (nombre, ubicacion),
        )
        return cur.lastrowid


def actualizar(id_espacio, nombre, ubicacion):
    """Actualiza nombre y ubicación. Devuelve cantidad de filas afectadas."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "UPDATE espacio SET nombre = %s, ubicacion = %s WHERE id_espacio = %s",
            (nombre, ubicacion, id_espacio),
        )
        return cur.rowcount


def eliminar(id_espacio):
    """Elimina un espacio. Devuelve filas afectadas.
    Puede lanzar IntegrityError si tiene actividades asociadas (FK)."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "DELETE FROM espacio WHERE id_espacio = %s",
            (id_espacio,),
        )
        return cur.rowcount
