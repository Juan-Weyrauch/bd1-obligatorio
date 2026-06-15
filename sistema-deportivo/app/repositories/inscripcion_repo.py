"""Capa de datos para la entidad Inscripcion."""
from app.db import get_cursor, get_connection


def listar():
    """Todas las inscripciones con estudiante y actividad."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                i.id_inscripcion,
                i.id_estudiante,
                i.id_actividad,
                i.fecha_inscripcion,
                i.estado,
                i.posicion_espera,
                e.documento AS estudiante_documento,
                e.nombre AS estudiante_nombre,
                e.apellido AS estudiante_apellido,
                a.nombre AS actividad_nombre
            FROM inscripcion i
            JOIN estudiante e ON e.id_estudiante = i.id_estudiante
            JOIN actividad a ON a.id_actividad = i.id_actividad
            ORDER BY i.fecha_inscripcion DESC, i.id_inscripcion DESC
            """
        )
        return cur.fetchall()


def obtener_por_id(id_inscripcion):
    """Una inscripcion por su PK, o None si no existe."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                id_inscripcion,
                id_estudiante,
                id_actividad,
                fecha_inscripcion,
                estado,
                posicion_espera
            FROM inscripcion
            WHERE id_inscripcion = %s
            """,
            (id_inscripcion,),
        )
        return cur.fetchone()


def existe_para_estudiante_actividad(id_estudiante, id_actividad):
    """True si ya existe una inscripcion para ese estudiante y actividad."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT 1
            FROM inscripcion
            WHERE id_estudiante = %s AND id_actividad = %s
            """,
            (id_estudiante, id_actividad),
        )
        return cur.fetchone() is not None


def crear(id_estudiante, id_actividad, estado, posicion_espera=None):
    """Inserta una inscripcion y devuelve su id autogenerado."""
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO inscripcion (
                id_estudiante, id_actividad, estado, posicion_espera
            )
            VALUES (%s, %s, %s, %s)
            """,
            (id_estudiante, id_actividad, estado, posicion_espera),
        )
        return cur.lastrowid


def crear_con_logica_cupo(id_estudiante, id_actividad):
    """Crea una inscripcion resolviendo cupo y lista de espera en una transaccion."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT id_actividad, cupo_maximo, estado
            FROM actividad
            WHERE id_actividad = %s
            FOR UPDATE
            """,
            (id_actividad,),
        )
        actividad = cur.fetchone()

        cur.execute(
            """
            SELECT 1
            FROM inscripcion
            WHERE id_estudiante = %s AND id_actividad = %s
            """,
            (id_estudiante, id_actividad),
        )
        ya_existe = cur.fetchone() is not None
        if ya_existe:
            raise ValueError("duplicada")

        cur.execute(
            """
            SELECT COUNT(*) AS cantidad
            FROM inscripcion
            WHERE id_actividad = %s AND estado = 'confirmada'
            """,
            (id_actividad,),
        )
        confirmadas = cur.fetchone()["cantidad"]

        if confirmadas < actividad["cupo_maximo"]:
            estado = "confirmada"
            posicion_espera = None
        else:
            cur.execute(
                """
                SELECT COALESCE(MAX(posicion_espera), 0) AS ultima_posicion
                FROM inscripcion
                WHERE id_actividad = %s AND estado = 'en_espera'
                """,
                (id_actividad,),
            )
            posicion_espera = cur.fetchone()["ultima_posicion"] + 1
            estado = "en_espera"

        cur.execute(
            """
            INSERT INTO inscripcion (
                id_estudiante, id_actividad, estado, posicion_espera
            )
            VALUES (%s, %s, %s, %s)
            """,
            (id_estudiante, id_actividad, estado, posicion_espera),
        )
        id_inscripcion = cur.lastrowid
        conn.commit()
        return {
            "id_inscripcion": id_inscripcion,
            "estado": estado,
            "posicion_espera": posicion_espera,
            "actividad_estado": actividad["estado"],
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def cancelar(id_inscripcion):
    """Cancela una inscripcion y promueve lista de espera si corresponde."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT id_inscripcion, id_actividad, estado, posicion_espera
            FROM inscripcion
            WHERE id_inscripcion = %s
            FOR UPDATE
            """,
            (id_inscripcion,),
        )
        inscripcion = cur.fetchone()
        if inscripcion is None:
            raise ValueError("no_existe")
        if inscripcion["estado"] == "cancelada":
            raise ValueError("ya_cancelada")

        cur.execute(
            """
            UPDATE inscripcion
            SET estado = 'cancelada', posicion_espera = NULL
            WHERE id_inscripcion = %s
            """,
            (id_inscripcion,),
        )

        promovida = None

        if inscripcion["estado"] == "confirmada":
            cur.execute(
                """
                SELECT id_inscripcion, posicion_espera
                FROM inscripcion
                WHERE id_actividad = %s AND estado = 'en_espera'
                ORDER BY posicion_espera
                LIMIT 1
                FOR UPDATE
                """,
                (inscripcion["id_actividad"],),
            )
            promovida = cur.fetchone()
            if promovida is not None:
                cur.execute(
                    """
                    UPDATE inscripcion
                    SET estado = 'confirmada', posicion_espera = NULL
                    WHERE id_inscripcion = %s
                    """,
                    (promovida["id_inscripcion"],),
                )
                cur.execute(
                    """
                    UPDATE inscripcion
                    SET posicion_espera = posicion_espera - 1
                    WHERE id_actividad = %s
                      AND estado = 'en_espera'
                      AND posicion_espera > %s
                    """,
                    (inscripcion["id_actividad"], promovida["posicion_espera"]),
                )
        elif inscripcion["estado"] == "en_espera":
            cur.execute(
                """
                UPDATE inscripcion
                SET posicion_espera = posicion_espera - 1
                WHERE id_actividad = %s
                  AND estado = 'en_espera'
                  AND posicion_espera > %s
                """,
                (inscripcion["id_actividad"], inscripcion["posicion_espera"]),
            )

        conn.commit()
        return {"promovida": promovida is not None}
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
