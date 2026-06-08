"""Capa de negocio para Disciplina.
Reglas y validaciones. No escribe SQL: delega en el repositorio."""
from mysql.connector.errors import IntegrityError
from app.repositories import disciplina_repo


class ReglaNegocioError(Exception):
    """Error de validación con un mensaje apto para mostrar al usuario."""
    pass


def _normalizar_nombre(nombre):
    """Recorta espacios. Evita guardar '  Yoga  ' o cadenas en blanco."""
    return (nombre or "").strip()


def _validar_nombre(nombre):
    if not nombre:
        raise ReglaNegocioError("El nombre es obligatorio.")
    if len(nombre) > 100:
        raise ReglaNegocioError("El nombre no puede superar los 100 caracteres.")


def listar_disciplinas():
    return disciplina_repo.listar()


def obtener_disciplina(id_disciplina):
    disciplina = disciplina_repo.obtener_por_id(id_disciplina)
    if disciplina is None:
        raise ReglaNegocioError("La disciplina no existe.")
    return disciplina


def crear_disciplina(nombre):
    nombre = _normalizar_nombre(nombre)
    _validar_nombre(nombre)
    if disciplina_repo.existe_nombre(nombre):
        raise ReglaNegocioError(f"Ya existe una disciplina llamada «{nombre}».")
    try:
        return disciplina_repo.crear(nombre)
    except IntegrityError:
        # Red de seguridad: dos requests pasaron el chequeo a la vez
        # y la UNIQUE de la BD frenó al segundo.
        raise ReglaNegocioError(f"Ya existe una disciplina llamada «{nombre}».")


def actualizar_disciplina(id_disciplina, nombre):
    obtener_disciplina(id_disciplina)           # valida que exista
    nombre = _normalizar_nombre(nombre)
    _validar_nombre(nombre)
    if disciplina_repo.existe_nombre(nombre, excluir_id=id_disciplina):
        raise ReglaNegocioError(f"Ya existe otra disciplina llamada «{nombre}».")
    try:
        disciplina_repo.actualizar(id_disciplina, nombre)
    except IntegrityError:
        raise ReglaNegocioError(f"Ya existe otra disciplina llamada «{nombre}».")


def eliminar_disciplina(id_disciplina):
    obtener_disciplina(id_disciplina)           # valida que exista
    try:
        disciplina_repo.eliminar(id_disciplina)
    except IntegrityError:
        raise ReglaNegocioError(
            "No se puede eliminar: la disciplina tiene actividades asociadas."
        )