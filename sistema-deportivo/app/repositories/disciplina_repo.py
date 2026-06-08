"""Capa de datos para la entidad Disciplina.
Única capa autorizada a escribir SQL para esta entidad.
Regla de oro: SIEMPRE consultas parametrizadas con %s. Nunca f-strings."""
from app.db import get_cursor


def listar():
    """Todas las disciplinas, ordenadas por nombre."""
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_disciplina, nombre FROM disciplina ORDER BY nombre"
        )
        return cur.fetchall()


def obtener_por_id(id_disciplina):
    """Una disciplina por su PK, o None si no existe."""
    with get_cursor() as cur:
        cur.execute(
            "SELECT id_disciplina, nombre FROM disciplina WHERE id_disciplina = %s",
            (id_disciplina,),
        )
        return cur.fetchone()


def existe_nombre(nombre, excluir_id=None):
    """True si ya hay una disciplina con ese nombre.
    excluir_id permite ignorar la propia fila al editar."""
    with get_cursor() as cur:
        if excluir_id is None:
            cur.execute(
                "SELECT 1 FROM disciplina WHERE nombre = %s",
                (nombre,),
            )
        else:
            cur.execute(
                "SELECT 1 FROM disciplina WHERE nombre = %s AND id_disciplina <> %s",
                (nombre, excluir_id),
            )
        return cur.fetchone() is not None


def crear(nombre):
    """Inserta una disciplina y devuelve su id autogenerado."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "INSERT INTO disciplina (nombre) VALUES (%s)",
            (nombre,),
        )
        return cur.lastrowid


def actualizar(id_disciplina, nombre):
    """Actualiza el nombre. Devuelve cantidad de filas afectadas."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "UPDATE disciplina SET nombre = %s WHERE id_disciplina = %s",
            (nombre, id_disciplina),
        )
        return cur.rowcount


def eliminar(id_disciplina):
    """Elimina una disciplina. Devuelve filas afectadas.
    Puede lanzar IntegrityError si tiene actividades asociadas (FK)."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "DELETE FROM disciplina WHERE id_disciplina = %s",
            (id_disciplina,),
        )
        return cur.rowcount