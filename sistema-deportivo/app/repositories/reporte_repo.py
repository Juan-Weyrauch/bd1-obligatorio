"""Consultas de reportes (solo lectura).

Cada clave del diccionario coincide con el nombre que pide la SPA en
GET /reportes/<nombre>. Son las consultas obligatorias de la letra.
'confirmada' es el estado que cuenta como inscripto efectivo.
"""
from app.db import get_cursor

CONSULTAS = {
    # 1) Actividades con mayor cantidad de inscriptos confirmados
    "inscriptos-por-actividad": """
        SELECT a.nombre AS actividad,
               COUNT(i.id_inscripcion) AS inscriptos_confirmados
        FROM actividad a
        LEFT JOIN inscripcion i
               ON i.id_actividad = a.id_actividad AND i.estado = 'confirmada'
        GROUP BY a.id_actividad, a.nombre
        ORDER BY inscriptos_confirmados DESC, a.nombre
    """,

    # 2) Actividades con cupos disponibles
    "cupos-disponibles": """
        SELECT a.nombre AS actividad,
               a.cupo_maximo,
               COUNT(i.id_inscripcion) AS confirmados,
               (a.cupo_maximo - COUNT(i.id_inscripcion)) AS cupos_disponibles
        FROM actividad a
        LEFT JOIN inscripcion i
               ON i.id_actividad = a.id_actividad AND i.estado = 'confirmada'
        GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
        HAVING cupos_disponibles > 0
        ORDER BY cupos_disponibles DESC, a.nombre
    """,

    # 3) Cantidad de inscriptos por disciplina
    "inscriptos-por-disciplina": """
        SELECT d.nombre AS disciplina,
               COUNT(i.id_inscripcion) AS inscriptos
        FROM disciplina d
        LEFT JOIN actividad a ON a.id_disciplina = d.id_disciplina
        LEFT JOIN inscripcion i
               ON i.id_actividad = a.id_actividad AND i.estado = 'confirmada'
        GROUP BY d.id_disciplina, d.nombre
        ORDER BY inscriptos DESC, d.nombre
    """,

    # 4) Cantidad de inscriptos por carrera (y su facultad)
    "inscriptos-por-carrera": """
        SELECT c.nombre AS carrera,
               f.nombre AS facultad,
               COUNT(i.id_inscripcion) AS inscriptos
        FROM carrera c
        JOIN facultad f ON f.id_facultad = c.id_facultad
        LEFT JOIN estudiante e ON e.id_carrera = c.id_carrera
        LEFT JOIN inscripcion i
               ON i.id_estudiante = e.id_estudiante AND i.estado = 'confirmada'
        GROUP BY c.id_carrera, c.nombre, f.nombre
        ORDER BY inscriptos DESC, c.nombre
    """,

    # 5) Porcentaje de ocupacion de cada actividad
    "ocupacion": """
        SELECT a.nombre AS actividad,
               a.cupo_maximo,
               COUNT(i.id_inscripcion) AS confirmados,
               ROUND(COUNT(i.id_inscripcion) / a.cupo_maximo * 100, 1)
                   AS porcentaje_ocupacion
        FROM actividad a
        LEFT JOIN inscripcion i
               ON i.id_actividad = a.id_actividad AND i.estado = 'confirmada'
        GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
        ORDER BY porcentaje_ocupacion DESC, a.nombre
    """,

    # 6) Porcentaje de asistencia por actividad
    "asistencia": """
        SELECT a.nombre AS actividad,
               COUNT(asi.id_asistencia) AS registros,
               COALESCE(SUM(asi.presente), 0) AS presentes,
               ROUND(
                   CASE WHEN COUNT(asi.id_asistencia) = 0 THEN 0
                        ELSE SUM(asi.presente) / COUNT(asi.id_asistencia) * 100
                   END, 1) AS porcentaje_asistencia
        FROM actividad a
        LEFT JOIN inscripcion i ON i.id_actividad = a.id_actividad
        LEFT JOIN asistencia asi ON asi.id_inscripcion = i.id_inscripcion
        GROUP BY a.id_actividad, a.nombre
        ORDER BY porcentaje_asistencia DESC, a.nombre
    """,

    # 7) Estudiantes con tres o mas inasistencias registradas
    "inasistencias": """
        SELECT e.documento, e.nombre, e.apellido,
               COUNT(asi.id_asistencia) AS inasistencias
        FROM estudiante e
        JOIN inscripcion i ON i.id_estudiante = e.id_estudiante
        JOIN asistencia asi
             ON asi.id_inscripcion = i.id_inscripcion AND asi.presente = FALSE
        GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido
        HAVING inasistencias >= 3
        ORDER BY inasistencias DESC, e.apellido
    """,
}


def obtener(nombre):
    """Ejecuta el reporte pedido. Lanza KeyError si el nombre no existe."""
    sql = CONSULTAS.get(nombre)
    if sql is None:
        raise KeyError(nombre)
    with get_cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()
