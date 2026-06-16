"""Capa de datos para la entidad Estudiante."""
from app.db import get_cursor


def listar():
    """Todos los estudiantes, con su carrera, ordenados por apellido y nombre."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT e.id_estudiante, e.documento, e.nombre, e.apellido, e.email,
                   e.id_carrera, c.nombre AS carrera_nombre,
                   f.nombre AS facultad_nombre
            FROM estudiante e
            JOIN carrera c ON c.id_carrera = e.id_carrera
            JOIN facultad f ON f.id_facultad = c.id_facultad
            ORDER BY e.apellido, e.nombre
            """
        )
        return cur.fetchall()


def listar_para_formulario():
    """Estudiantes para usar en selects de formularios."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                id_estudiante,
                documento,
                nombre,
                apellido
            FROM estudiante
            ORDER BY apellido, nombre
            """
        )
        return cur.fetchall()


def obtener_por_id(id_estudiante):
    """Un estudiante por su PK, o None si no existe."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT id_estudiante, documento, nombre, apellido, email, id_carrera
            FROM estudiante
            WHERE id_estudiante = %s
            """,
            (id_estudiante,),
        )
        return cur.fetchone()


def existe_documento(documento, excluir_id=None):
    """True si ya hay un estudiante con ese documento."""
    with get_cursor() as cur:
        if excluir_id is None:
            cur.execute(
                "SELECT 1 FROM estudiante WHERE documento = %s",
                (documento,),
            )
        else:
            cur.execute(
                """
                SELECT 1
                FROM estudiante
                WHERE documento = %s AND id_estudiante <> %s
                """,
                (documento, excluir_id),
            )
        return cur.fetchone() is not None


def existe_email(email, excluir_id=None):
    """True si ya hay un estudiante con ese email."""
    with get_cursor() as cur:
        if excluir_id is None:
            cur.execute(
                "SELECT 1 FROM estudiante WHERE email = %s",
                (email,),
            )
        else:
            cur.execute(
                """
                SELECT 1
                FROM estudiante
                WHERE email = %s AND id_estudiante <> %s
                """,
                (email, excluir_id),
            )
        return cur.fetchone() is not None


def crear(documento, nombre, apellido, email, id_carrera):
    """Inserta un estudiante y devuelve su id autogenerado."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO estudiante (documento, nombre, apellido, email, id_carrera)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (documento, nombre, apellido, email, id_carrera),
        )
        return cur.lastrowid


def actualizar(id_estudiante, documento, nombre, apellido, email, id_carrera):
    """Actualiza los datos del estudiante. Devuelve filas afectadas."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            UPDATE estudiante
            SET documento = %s, nombre = %s, apellido = %s,
                email = %s, id_carrera = %s
            WHERE id_estudiante = %s
            """,
            (documento, nombre, apellido, email, id_carrera, id_estudiante),
        )
        return cur.rowcount


def eliminar(id_estudiante):
    """Elimina un estudiante. Puede lanzar IntegrityError por FK."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            "DELETE FROM estudiante WHERE id_estudiante = %s",
            (id_estudiante,),
        )
        return cur.rowcount
