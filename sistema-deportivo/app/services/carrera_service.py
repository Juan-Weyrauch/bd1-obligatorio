"""Capa de negocio para Carrera."""
from mysql.connector.errors import IntegrityError
from app.repositories import carrera_repo, facultad_repo


class ReglaNegocioError(Exception):
    """Error de validacion con un mensaje apto para mostrar al usuario."""
    pass


def _normalizar_nombre(nombre):
    return (nombre or "").strip()


def _validar_nombre(nombre):
    if not nombre:
        raise ReglaNegocioError("El nombre es obligatorio.")
    if len(nombre) > 100:
        raise ReglaNegocioError("El nombre no puede superar los 100 caracteres.")


def _validar_facultad(id_facultad):
    if not id_facultad:
        raise ReglaNegocioError("La facultad es obligatoria.")
    facultad = facultad_repo.obtener_por_id(id_facultad)
    if facultad is None:
        raise ReglaNegocioError("La facultad seleccionada no existe.")


def listar_carreras():
    return carrera_repo.listar()


def obtener_carrera(id_carrera):
    carrera = carrera_repo.obtener_por_id(id_carrera)
    if carrera is None:
        raise ReglaNegocioError("La carrera no existe.")
    return carrera


def listar_facultades_para_formulario():
    return facultad_repo.listar()


def crear_carrera(nombre, id_facultad):
    nombre = _normalizar_nombre(nombre)
    _validar_nombre(nombre)
    _validar_facultad(id_facultad)
    if carrera_repo.existe_nombre(nombre):
        raise ReglaNegocioError(f"Ya existe una carrera llamada '{nombre}'.")
    try:
        return carrera_repo.crear(nombre, id_facultad)
    except IntegrityError:
        raise ReglaNegocioError(f"Ya existe una carrera llamada '{nombre}'.")


def actualizar_carrera(id_carrera, nombre, id_facultad):
    obtener_carrera(id_carrera)
    nombre = _normalizar_nombre(nombre)
    _validar_nombre(nombre)
    _validar_facultad(id_facultad)
    if carrera_repo.existe_nombre(nombre, excluir_id=id_carrera):
        raise ReglaNegocioError(
            f"Ya existe otra carrera llamada '{nombre}'."
        )
    try:
        carrera_repo.actualizar(id_carrera, nombre, id_facultad)
    except IntegrityError:
        raise ReglaNegocioError(
            f"Ya existe otra carrera llamada '{nombre}'."
        )


def eliminar_carrera(id_carrera):
    obtener_carrera(id_carrera)
    try:
        carrera_repo.eliminar(id_carrera)
    except IntegrityError:
        raise ReglaNegocioError(
            "No se puede eliminar: la carrera tiene estudiantes asociados."
        )
