"""Capa de presentacion para Facultad (ABM)."""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from app.services import facultad_service
from app.services.facultad_service import ReglaNegocioError

bp = Blueprint("facultades", __name__, url_prefix="/facultades")


@bp.route("/")
def listar():
    facultades = facultad_service.listar_facultades()
    return render_template("facultades/listar.html", facultades=facultades)


@bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        try:
            facultad_service.crear_facultad(request.form.get("nombre"))
            flash("Facultad creada correctamente.", "success")
            return redirect(url_for("facultades.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return render_template(
                "facultades/form.html",
                facultad={"nombre": request.form.get("nombre", "")},
                modo="crear",
            )
    return render_template("facultades/form.html", facultad=None, modo="crear")


@bp.route("/<int:id_facultad>/editar", methods=["GET", "POST"])
def editar(id_facultad):
    if request.method == "POST":
        try:
            facultad_service.actualizar_facultad(
                id_facultad, request.form.get("nombre")
            )
            flash("Facultad actualizada correctamente.", "success")
            return redirect(url_for("facultades.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return render_template(
                "facultades/form.html",
                facultad={
                    "id_facultad": id_facultad,
                    "nombre": request.form.get("nombre", ""),
                },
                modo="editar",
            )
    try:
        facultad = facultad_service.obtener_facultad(id_facultad)
    except ReglaNegocioError as e:
        flash(str(e), "danger")
        return redirect(url_for("facultades.listar"))
    return render_template("facultades/form.html", facultad=facultad, modo="editar")


@bp.route("/<int:id_facultad>/eliminar", methods=["POST"])
def eliminar(id_facultad):
    try:
        facultad_service.eliminar_facultad(id_facultad)
        flash("Facultad eliminada.", "success")
    except ReglaNegocioError as e:
        flash(str(e), "danger")
    return redirect(url_for("facultades.listar"))
