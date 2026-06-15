"""Capa de presentacion para Inscripcion."""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from app.services import inscripcion_service
from app.services.inscripcion_service import ReglaNegocioError

bp = Blueprint("inscripciones", __name__, url_prefix="/inscripciones")


def _render_formulario(inscripcion):
    estudiantes = inscripcion_service.listar_estudiantes_para_formulario()
    actividades = inscripcion_service.listar_actividades_para_formulario()
    return render_template(
        "inscripciones/form.html",
        inscripcion=inscripcion,
        estudiantes=estudiantes,
        actividades=actividades,
    )


@bp.route("/")
def listar():
    inscripciones = inscripcion_service.listar_inscripciones()
    return render_template(
        "inscripciones/listar.html",
        inscripciones=inscripciones,
    )


@bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        inscripcion = {
            "id_estudiante": request.form.get("id_estudiante", ""),
            "id_actividad": request.form.get("id_actividad", ""),
        }
        try:
            mensaje = inscripcion_service.crear_inscripcion(
                inscripcion["id_estudiante"],
                inscripcion["id_actividad"],
            )
            flash(mensaje, "success")
            return redirect(url_for("inscripciones.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return _render_formulario(inscripcion)
    return _render_formulario(None)


@bp.route("/<int:id_inscripcion>/cancelar", methods=["POST"])
def cancelar(id_inscripcion):
    try:
        mensaje = inscripcion_service.cancelar_inscripcion(id_inscripcion)
        flash(mensaje, "success")
    except ReglaNegocioError as e:
        flash(str(e), "danger")
    return redirect(url_for("inscripciones.listar"))
