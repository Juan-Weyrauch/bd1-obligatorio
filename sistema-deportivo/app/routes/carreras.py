"""Capa de presentacion para Carrera (ABM)."""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from app.services import carrera_service
from app.services.carrera_service import ReglaNegocioError

bp = Blueprint("carreras", __name__, url_prefix="/carreras")


def _render_formulario(carrera, modo):
    facultades = carrera_service.listar_facultades_para_formulario()
    return render_template(
        "carreras/form.html",
        carrera=carrera,
        facultades=facultades,
        modo=modo,
    )


@bp.route("/")
def listar():
    carreras = carrera_service.listar_carreras()
    return render_template("carreras/listar.html", carreras=carreras)


@bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        carrera = {
            "nombre": request.form.get("nombre", ""),
            "id_facultad": request.form.get("id_facultad", ""),
        }
        try:
            carrera_service.crear_carrera(
                carrera["nombre"], carrera["id_facultad"]
            )
            flash("Carrera creada correctamente.", "success")
            return redirect(url_for("carreras.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return _render_formulario(carrera, "crear")
    return _render_formulario(None, "crear")


@bp.route("/<int:id_carrera>/editar", methods=["GET", "POST"])
def editar(id_carrera):
    if request.method == "POST":
        carrera = {
            "id_carrera": id_carrera,
            "nombre": request.form.get("nombre", ""),
            "id_facultad": request.form.get("id_facultad", ""),
        }
        try:
            carrera_service.actualizar_carrera(
                id_carrera, carrera["nombre"], carrera["id_facultad"]
            )
            flash("Carrera actualizada correctamente.", "success")
            return redirect(url_for("carreras.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return _render_formulario(carrera, "editar")
    try:
        carrera = carrera_service.obtener_carrera(id_carrera)
    except ReglaNegocioError as e:
        flash(str(e), "danger")
        return redirect(url_for("carreras.listar"))
    return _render_formulario(carrera, "editar")


@bp.route("/<int:id_carrera>/eliminar", methods=["POST"])
def eliminar(id_carrera):
    try:
        carrera_service.eliminar_carrera(id_carrera)
        flash("Carrera eliminada.", "success")
    except ReglaNegocioError as e:
        flash(str(e), "danger")
    return redirect(url_for("carreras.listar"))
