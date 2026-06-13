"""Capa de negocio para Estudiante."""
from mysql.connector.errors import IntegrityError
from app.repositories import estudiante_repo, carrera_repo


class ReglaNegocioError(Exception):
    """Error de validacion con un mensaje apto para mostrar al usuario."""
    pass


def _normalizar_texto(valor):
    return (valor or "").strip()


def _normalizar_email(email):
    return (email or "").strip().lower()


def _validar_documento(documento):
    if not documento:
        raise ReglaNegocioError("El documento es obligatorio.")
    if len(documento) > 20:
        raise ReglaNegocioError("El documento no puede superar los 20 caracteres.")


def _validar_nombre(nombre):
    if not nombre:
        raise ReglaNegocioError("El nombre es obligatorio.")
    if len(nombre) > 100:
        raise ReglaNegocioError("El nombre no puede superar los 100 caracteres.")


def _validar_apellido(apellido):
    if not apellido:
        raise ReglaNegocioError("El apellido es obligatorio.")
    if len(apellido) > 100:
        raise ReglaNegocioError("El apellido no puede superar los 100 caracteres.")


def _validar_email(email):
    if not email:
        raise ReglaNegocioError("El email es obligatorio.")
    if len(email) > 150:
        raise ReglaNegocioError("El email no puede superar los 150 caracteres.")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ReglaNegocioError("El email no tiene un formato valido.")


def _validar_carrera(id_carrera):
    if not id_carrera:
        raise ReglaNegocioError("La carrera es obligatoria.")
    carrera = carrera_repo.obtener_por_id(id_carrera)
    if carrera is None:
        raise ReglaNegocioError("La carrera seleccionada no existe.")


def listar_estudiantes():
    return estudiante_repo.listar()


def obtener_estudiante(id_estudiante):
    estudiante = estudiante_repo.obtener_por_id(id_estudiante)
    if estudiante is None:
        raise ReglaNegocioError("El estudiante no existe.")
    return estudiante


def listar_carreras_para_formulario():
    return carrera_repo.listar()


def crear_estudiante(documento, nombre, apellido, email, id_carrera):
    documento = _normalizar_texto(documento)
    nombre = _normalizar_texto(nombre)
    apellido = _normalizar_texto(apellido)
    email = _normalizar_email(email)

    _validar_documento(documento)
    _validar_nombre(nombre)
    _validar_apellido(apellido)
    _validar_email(email)
    _validar_carrera(id_carrera)

    if estudiante_repo.existe_documento(documento):
        raise ReglaNegocioError(
            f"Ya existe un estudiante con el documento '{documento}'."
        )
    if estudiante_repo.existe_email(email):
        raise ReglaNegocioError(
            f"Ya existe un estudiante con el email '{email}'."
        )

    try:
        return estudiante_repo.crear(
            documento, nombre, apellido, email, id_carrera
        )
    except IntegrityError:
        raise ReglaNegocioError(
            "No se pudo crear el estudiante por datos duplicados o invalidos."
        )


def actualizar_estudiante(
    id_estudiante, documento, nombre, apellido, email, id_carrera
):
    obtener_estudiante(id_estudiante)
    documento = _normalizar_texto(documento)
    nombre = _normalizar_texto(nombre)
    apellido = _normalizar_texto(apellido)
    email = _normalizar_email(email)

    _validar_documento(documento)
    _validar_nombre(nombre)
    _validar_apellido(apellido)
    _validar_email(email)
    _validar_carrera(id_carrera)

    if estudiante_repo.existe_documento(documento, excluir_id=id_estudiante):
        raise ReglaNegocioError(
            f"Ya existe otro estudiante con el documento '{documento}'."
        )
    if estudiante_repo.existe_email(email, excluir_id=id_estudiante):
        raise ReglaNegocioError(
            f"Ya existe otro estudiante con el email '{email}'."
        )

    try:
        estudiante_repo.actualizar(
            id_estudiante, documento, nombre, apellido, email, id_carrera
        )
    except IntegrityError:
        raise ReglaNegocioError(
            "No se pudo actualizar el estudiante por datos duplicados o invalidos."
        )


def eliminar_estudiante(id_estudiante):
    obtener_estudiante(id_estudiante)
    try:
        estudiante_repo.eliminar(id_estudiante)
    except IntegrityError:
        raise ReglaNegocioError(
            "No se puede eliminar: el estudiante tiene inscripciones asociadas."
        )
