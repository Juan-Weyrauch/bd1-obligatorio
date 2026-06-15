"""Capa de negocio para Actividad."""
from mysql.connector.errors import IntegrityError
from app.repositories import actividad_repo, disciplina_repo, espacio_repo


class ReglaNegocioError(Exception):
    """Error de validacion con un mensaje apto para mostrar al usuario."""
    pass


DIAS_SEMANA = (
    "lunes", "martes", "miercoles", "jueves",
    "viernes", "sabado", "domingo"
)

ESTADOS_ACTIVIDAD = ("abierta", "cerrada", "finalizada", "cancelada")


def _normalizar_nombre(nombre):
    return (nombre or "").strip()


def _normalizar_entero(valor):
    return (valor or "").strip()


def _validar_nombre(nombre):
    if not nombre:
        raise ReglaNegocioError("El nombre es obligatorio.")
    if len(nombre) > 150:
        raise ReglaNegocioError("El nombre no puede superar los 150 caracteres.")


def _validar_disciplina(id_disciplina):
    if not id_disciplina:
        raise ReglaNegocioError("La disciplina es obligatoria.")
    disciplina = disciplina_repo.obtener_por_id(id_disciplina)
    if disciplina is None:
        raise ReglaNegocioError("La disciplina seleccionada no existe.")


def _validar_espacio(id_espacio):
    if not id_espacio:
        raise ReglaNegocioError("El espacio es obligatorio.")
    espacio = espacio_repo.obtener_por_id(id_espacio)
    if espacio is None:
        raise ReglaNegocioError("El espacio seleccionado no existe.")


def _validar_cupo(cupo_maximo):
    if not cupo_maximo:
        raise ReglaNegocioError("El cupo maximo es obligatorio.")
    try:
        cupo = int(cupo_maximo)
    except ValueError:
        raise ReglaNegocioError("El cupo maximo debe ser un numero entero.")
    if cupo <= 0:
        raise ReglaNegocioError("El cupo maximo debe ser mayor que 0.")
    return cupo


def _validar_dia_semana(dia_semana):
    if dia_semana not in DIAS_SEMANA:
        raise ReglaNegocioError("El dia de la semana es invalido.")


def _validar_horario(horario):
    if not horario:
        raise ReglaNegocioError("El horario es obligatorio.")


def _validar_estado(estado):
    if estado not in ESTADOS_ACTIVIDAD:
        raise ReglaNegocioError("El estado es invalido.")


def listar_actividades():
    return actividad_repo.listar()


def obtener_actividad(id_actividad):
    actividad = actividad_repo.obtener_por_id(id_actividad)
    if actividad is None:
        raise ReglaNegocioError("La actividad no existe.")
    return actividad


def listar_disciplinas_para_formulario():
    return disciplina_repo.listar()


def listar_espacios_para_formulario():
    return espacio_repo.listar()


def crear_actividad(
    nombre, id_disciplina, id_espacio, cupo_maximo, dia_semana, horario, estado
):
    nombre = _normalizar_nombre(nombre)
    id_disciplina = _normalizar_entero(id_disciplina)
    id_espacio = _normalizar_entero(id_espacio)
    cupo = _validar_cupo(cupo_maximo)

    _validar_nombre(nombre)
    _validar_disciplina(id_disciplina)
    _validar_espacio(id_espacio)
    _validar_dia_semana(dia_semana)
    _validar_horario(horario)
    _validar_estado(estado)

    try:
        return actividad_repo.crear(
            nombre, id_disciplina, id_espacio, cupo, dia_semana, horario, estado
        )
    except IntegrityError:
        raise ReglaNegocioError("No se pudo crear la actividad por datos invalidos.")


def actualizar_actividad(
    id_actividad, nombre, id_disciplina, id_espacio, cupo_maximo,
    dia_semana, horario, estado
):
    obtener_actividad(id_actividad)
    nombre = _normalizar_nombre(nombre)
    id_disciplina = _normalizar_entero(id_disciplina)
    id_espacio = _normalizar_entero(id_espacio)
    cupo = _validar_cupo(cupo_maximo)

    _validar_nombre(nombre)
    _validar_disciplina(id_disciplina)
    _validar_espacio(id_espacio)
    _validar_dia_semana(dia_semana)
    _validar_horario(horario)
    _validar_estado(estado)

    try:
        actividad_repo.actualizar(
            id_actividad, nombre, id_disciplina, id_espacio,
            cupo, dia_semana, horario, estado
        )
    except IntegrityError:
        raise ReglaNegocioError(
            "No se pudo actualizar la actividad por datos invalidos."
        )


def eliminar_actividad(id_actividad):
    obtener_actividad(id_actividad)
    try:
        actividad_repo.eliminar(id_actividad)
    except IntegrityError:
        raise ReglaNegocioError(
            "No se puede eliminar: la actividad tiene inscripciones asociadas."
        )
