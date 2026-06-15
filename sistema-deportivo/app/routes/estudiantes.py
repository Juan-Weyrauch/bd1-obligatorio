"""Capa de presentacion para Estudiante (ABM)."""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from app.services import estudiante_service
from app.services.estudiante_service import ReglaNegocioError

bp = Blueprint("estudiantes", __name__, url_prefix="/estudiantes")


def _render_formulario(estudiante, modo):
    carreras = estudiante_service.listar_carreras_para_formulario()
    return render_template(
        "estudiantes/form.html",
        estudiante=estudiante,
        carreras=carreras,
        modo=modo,
    )


@bp.route("/")
def listar():
    estudiantes = estudiante_service.listar_estudiantes()
    return render_template("estudiantes/listar.html", estudiantes=estudiantes)


@bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        estudiante = {
            "documento": request.form.get("documento", ""),
            "nombre": request.form.get("nombre", ""),
            "apellido": request.form.get("apellido", ""),
            "email": request.form.get("email", ""),
            "id_carrera": request.form.get("id_carrera", ""),
        }
        try:
            estudiante_service.crear_estudiante(
                estudiante["documento"],
                estudiante["nombre"],
                estudiante["apellido"],
                estudiante["email"],
                estudiante["id_carrera"],
            )
            flash("Estudiante creado correctamente.", "success")
            return redirect(url_for("estudiantes.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return _render_formulario(estudiante, "crear")
    return _render_formulario(None, "crear")


@bp.route("/<int:id_estudiante>/editar", methods=["GET", "POST"])
def editar(id_estudiante):
    if request.method == "POST":
        estudiante = {
            "id_estudiante": id_estudiante,
            "documento": request.form.get("documento", ""),
            "nombre": request.form.get("nombre", ""),
            "apellido": request.form.get("apellido", ""),
            "email": request.form.get("email", ""),
            "id_carrera": request.form.get("id_carrera", ""),
        }
        try:
            estudiante_service.actualizar_estudiante(
                id_estudiante,
                estudiante["documento"],
                estudiante["nombre"],
                estudiante["apellido"],
                estudiante["email"],
                estudiante["id_carrera"],
            )
            flash("Estudiante actualizado correctamente.", "success")
            return redirect(url_for("estudiantes.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return _render_formulario(estudiante, "editar")
    try:
        estudiante = estudiante_service.obtener_estudiante(id_estudiante)
    except ReglaNegocioError as e:
        flash(str(e), "danger")
        return redirect(url_for("estudiantes.listar"))
    return _render_formulario(estudiante, "editar")


@bp.route("/<int:id_estudiante>/eliminar", methods=["POST"])
def eliminar(id_estudiante):
    try:
        estudiante_service.eliminar_estudiante(id_estudiante)
        flash("Estudiante eliminado.", "success")
    except ReglaNegocioError as e:
        flash(str(e), "danger")
    return redirect(url_for("estudiantes.listar"))
