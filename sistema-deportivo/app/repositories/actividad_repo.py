"""Capa de datos para la entidad Actividad."""
from app.db import get_cursor


def listar():
    """Todas las actividades con sus relaciones, ordenadas por nombre."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                a.id_actividad,
                a.nombre,
                a.id_disciplina,
                a.id_espacio,
                a.cupo_maximo,
                a.dia_semana,
                a.horario,
                a.estado,
                d.nombre AS disciplina_nombre,
                e.nombre AS espacio_nombre,
                e.ubicacion AS espacio_ubicacion
            FROM actividad a
            JOIN disciplina d ON d.id_disciplina = a.id_disciplina
            JOIN espacio e ON e.id_espacio = a.id_espacio
            ORDER BY a.nombre
            """
        )
        return cur.fetchall()


def obtener_por_id(id_actividad):
    """Una actividad por su PK, o None si no existe."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                id_actividad,
                nombre,
                id_disciplina,
                id_espacio,
                cupo_maximo,
                dia_semana,
                horario,
                estado
            FROM actividad
            WHERE id_actividad = %s
            """,
            (id_actividad,),
        )
        return cur.fetchone()


def crear(
    nombre, id_disciplina, id_espacio, cupo_maximo, dia_semana, horario, estado
):
    """Inserta una actividad y devuelve su id autogenerado."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO actividad (
                nombre, id_disciplina, id_espacio, cupo_maximo,
                dia_semana, horario, estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                nombre, id_disciplina, id_espacio, cupo_maximo,
                dia_semana, horario, estado
            ),
        )
        return cur.lastrowid


def actualizar(
    id_actividad, nombre, id_disciplina, id_espacio, cupo_maximo,
    dia_semana, horario, estado
):
    """Actualiza una actividad. Devuelve filas afectadas."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            UPDATE actividad
            SET nombre = %s,
                id_disciplina = %s,
                id_espacio = %s,
                cupo_maximo = %s,
                dia_semana = %s,
                horario = %s,
                estado = %s
            WHERE id_actividad = %s
            """,
            (
                nombre, id_disciplina, id_espacio, cupo_maximo,
                dia_semana, horario, estado, id_actividad
            ),
        )
        return cur.rowcount


def eliminar(id_actividad):
    """Elimina una actividad. Puede lanzar IntegrityError por FK."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "DELETE FROM actividad WHERE id_actividad = %s",
            (id_actividad,),
        )
        return cur.rowcount
