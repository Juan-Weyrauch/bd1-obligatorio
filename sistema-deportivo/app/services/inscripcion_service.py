"""Capa de negocio para Inscripcion."""
from app.repositories import inscripcion_repo, estudiante_repo, actividad_repo


class ReglaNegocioError(Exception):
    """Error de validacion con un mensaje apto para mostrar al usuario."""
    pass


def _normalizar_entero(valor):
    return (valor or "").strip()


def _validar_estudiante(id_estudiante):
    if not id_estudiante:
        raise ReglaNegocioError("El estudiante es obligatorio.")
    estudiante = estudiante_repo.obtener_por_id(id_estudiante)
    if estudiante is None:
        raise ReglaNegocioError("El estudiante seleccionado no existe.")


def _validar_actividad(id_actividad):
    if not id_actividad:
        raise ReglaNegocioError("La actividad es obligatoria.")
    actividad = actividad_repo.obtener_por_id(id_actividad)
    if actividad is None:
        raise ReglaNegocioError("La actividad seleccionada no existe.")
    if actividad["estado"] != "abierta":
        raise ReglaNegocioError("Solo se puede inscribir en actividades abiertas.")


def listar_inscripciones():
    return inscripcion_repo.listar()


def obtener_inscripcion(id_inscripcion):
    inscripcion = inscripcion_repo.obtener_por_id(id_inscripcion)
    if inscripcion is None:
        raise ReglaNegocioError("La inscripcion no existe.")
    return inscripcion


def listar_estudiantes_para_formulario():
    return estudiante_repo.listar_para_formulario()


def listar_actividades_para_formulario():
    return actividad_repo.listar_para_inscripciones()


def crear_inscripcion(id_estudiante, id_actividad):
    id_estudiante = _normalizar_entero(id_estudiante)
    id_actividad = _normalizar_entero(id_actividad)

    _validar_estudiante(id_estudiante)
    _validar_actividad(id_actividad)

    if inscripcion_repo.existe_para_estudiante_actividad(id_estudiante, id_actividad):
        raise ReglaNegocioError(
            "El estudiante ya tiene una inscripcion para esa actividad."
        )

    try:
        resultado = inscripcion_repo.crear_con_logica_cupo(
            id_estudiante, id_actividad
        )
    except ValueError as e:
        if str(e) == "duplicada":
            raise ReglaNegocioError(
                "El estudiante ya tiene una inscripcion para esa actividad."
            )
        raise

    if resultado["estado"] == "confirmada":
        return "Inscripcion confirmada correctamente."
    return (
        "La actividad ya alcanzo el cupo maximo. "
        f"El estudiante quedo en lista de espera (posicion {resultado['posicion_espera']})."
    )


def cancelar_inscripcion(id_inscripcion):
    obtener_inscripcion(id_inscripcion)
    try:
        resultado = inscripcion_repo.cancelar(id_inscripcion)
    except ValueError as e:
        if str(e) == "ya_cancelada":
            raise ReglaNegocioError("La inscripcion ya estaba cancelada.")
        raise

    if resultado["promovida"]:
        return (
            "Inscripcion cancelada. "
            "Se promovio automaticamente a la primera persona en espera."
        )
    return "Inscripcion cancelada correctamente."
