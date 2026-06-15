"""Capa de negocio para Facultad."""
from mysql.connector.errors import IntegrityError
from app.repositories import facultad_repo


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


def listar_facultades():
    return facultad_repo.listar()


def obtener_facultad(id_facultad):
    facultad = facultad_repo.obtener_por_id(id_facultad)
    if facultad is None:
        raise ReglaNegocioError("La facultad no existe.")
    return facultad


def crear_facultad(nombre):
    nombre = _normalizar_nombre(nombre)
    _validar_nombre(nombre)
    if facultad_repo.existe_nombre(nombre):
        raise ReglaNegocioError(f"Ya existe una facultad llamada '{nombre}'.")
    try:
        return facultad_repo.crear(nombre)
    except IntegrityError:
        raise ReglaNegocioError(f"Ya existe una facultad llamada '{nombre}'.")


def actualizar_facultad(id_facultad, nombre):
    obtener_facultad(id_facultad)
    nombre = _normalizar_nombre(nombre)
    _validar_nombre(nombre)
    if facultad_repo.existe_nombre(nombre, excluir_id=id_facultad):
        raise ReglaNegocioError(
            f"Ya existe otra facultad llamada '{nombre}'."
        )
    try:
        facultad_repo.actualizar(id_facultad, nombre)
    except IntegrityError:
        raise ReglaNegocioError(
            f"Ya existe otra facultad llamada '{nombre}'."
        )


def eliminar_facultad(id_facultad):
    obtener_facultad(id_facultad)
    try:
        facultad_repo.eliminar(id_facultad)
    except IntegrityError:
        raise ReglaNegocioError(
            "No se puede eliminar: la facultad tiene carreras asociadas."
        )
