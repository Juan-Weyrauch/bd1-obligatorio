"""Capa de negocio para Asistencia.

Regla de negocio clave (letra, punto 5): solo se registra asistencia de
estudiantes con inscripcion CONFIRMADA.
"""
from mysql.connector.errors import IntegrityError
from app.repositories import asistencia_repo, inscripcion_repo


class ReglaNegocioError(Exception):
    """Error de validacion con un mensaje apto para mostrar al usuario."""
    pass


def registrar_asistencia(id_inscripcion, fecha, presente):
    if not id_inscripcion:
        raise ReglaNegocioError("La inscripcion es obligatoria.")
    if not fecha:
        raise ReglaNegocioError("La fecha es obligatoria.")

    inscripcion = inscripcion_repo.obtener_por_id(id_inscripcion)
    if inscripcion is None:
        raise ReglaNegocioError("La inscripcion no existe.")
    if inscripcion["estado"] != "confirmada":
        raise ReglaNegocioError(
            "Solo se puede registrar asistencia de inscripciones confirmadas."
        )

    try:
        asistencia_repo.crear(id_inscripcion, fecha, bool(presente))
    except IntegrityError:
        raise ReglaNegocioError(
            "Ya hay una asistencia registrada para esa inscripcion en esa fecha."
        )
    return "Asistencia registrada correctamente."
