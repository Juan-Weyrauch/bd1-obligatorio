"""Capa de negocio para Espacio.
Reglas y validaciones. No escribe SQL: delega en el repositorio."""
from mysql.connector.errors import IntegrityError
from app.repositories import espacio_repo


class ReglaNegocioError(Exception):
    """Error de validación con un mensaje apto para mostrar al usuario."""
    pass


def _normalizar_nombre(nombre):
    """Recorta espacios. Evita guardar '  Gimnasio  ' o cadenas en blanco."""
    return (nombre or "").strip()


def _normalizar_ubicacion(ubicacion):
    """Recorta espacios para ubicación."""
    return (ubicacion or "").strip()


def _validar_nombre(nombre):
    if not nombre:
        raise ReglaNegocioError("El nombre es obligatorio.")
    if len(nombre) > 100:
        raise ReglaNegocioError("El nombre no puede superar los 100 caracteres.")


def _validar_ubicacion(ubicacion):
    if not ubicacion:
        raise ReglaNegocioError("La ubicación es obligatoria.")
    if len(ubicacion) > 150:
        raise ReglaNegocioError("La ubicación no puede superar los 150 caracteres.")


def listar_espacios():
    return espacio_repo.listar()


def obtener_espacio(id_espacio):
    espacio = espacio_repo.obtener_por_id(id_espacio)
    if espacio is None:
        raise ReglaNegocioError("Espacio no encontrado.")
    return espacio


def crear_espacio(nombre, ubicacion):
    nombre = _normalizar_nombre(nombre)
    ubicacion = _normalizar_ubicacion(ubicacion)
    
    _validar_nombre(nombre)
    _validar_ubicacion(ubicacion)
    
    if espacio_repo.existe(nombre, ubicacion):
        raise ReglaNegocioError(
            f"Ya existe un espacio con el nombre '{nombre}' en esa ubicación."
        )
    
    return espacio_repo.crear(nombre, ubicacion)


def actualizar_espacio(id_espacio, nombre, ubicacion):
    nombre = _normalizar_nombre(nombre)
    ubicacion = _normalizar_ubicacion(ubicacion)
    
    _validar_nombre(nombre)
    _validar_ubicacion(ubicacion)
    
    # Verificar que el espacio actual existe
    try:
        obtener_espacio(id_espacio)
    except ReglaNegocioError:
        raise
    
    # Verificar duplicados (permitiendo cambiar el actual)
    if espacio_repo.existe(nombre, ubicacion, excluir_id=id_espacio):
        raise ReglaNegocioError(
            f"Ya existe otro espacio con el nombre '{nombre}' en esa ubicación."
        )
    
    filas = espacio_repo.actualizar(id_espacio, nombre, ubicacion)
    if filas == 0:
        raise ReglaNegocioError("No se pudo actualizar el espacio.")


def eliminar_espacio(id_espacio):
    # Verificar que existe
    try:
        obtener_espacio(id_espacio)
    except ReglaNegocioError:
        raise
    
    try:
        filas = espacio_repo.eliminar(id_espacio)
        if filas == 0:
            raise ReglaNegocioError("No se pudo eliminar el espacio.")
    except IntegrityError as e:
        # Si hay actividades usando este espacio, MySQL lanza IntegrityError
        if "FOREIGN KEY" in str(e):
            raise ReglaNegocioError(
                "No se puede eliminar este espacio porque hay actividades asociadas."
            )
        raise
