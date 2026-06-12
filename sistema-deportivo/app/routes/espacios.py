"""Capa de presentación para Espacio (ABM).
Solo traduce HTTP <-> servicio y renderiza HTML."""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from app.services import espacio_service
from app.services.espacio_service import ReglaNegocioError

bp = Blueprint("espacios", __name__, url_prefix="/espacios")


@bp.route("/")
def listar():
    espacios = espacio_service.listar_espacios()
    return render_template("espacios/listar.html", espacios=espacios)


@bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        try:
            espacio_service.crear_espacio(
                request.form.get("nombre"),
                request.form.get("ubicacion")
            )
            flash("Espacio creado correctamente.", "success")
            return redirect(url_for("espacios.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return render_template(
                "espacios/form.html",
                espacio={
                    "nombre": request.form.get("nombre", ""),
                    "ubicacion": request.form.get("ubicacion", "")
                },
                modo="crear",
            )
    return render_template("espacios/form.html", espacio=None, modo="crear")


@bp.route("/<int:id_espacio>/editar", methods=["GET", "POST"])
def editar(id_espacio):
    if request.method == "POST":
        try:
            espacio_service.actualizar_espacio(
                id_espacio,
                request.form.get("nombre"),
                request.form.get("ubicacion")
            )
            flash("Espacio actualizado correctamente.", "success")
            return redirect(url_for("espacios.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return render_template(
                "espacios/form.html",
                espacio={
                    "id_espacio": id_espacio,
                    "nombre": request.form.get("nombre", ""),
                    "ubicacion": request.form.get("ubicacion", "")
                },
                modo="editar",
            )
    try:
        espacio = espacio_service.obtener_espacio(id_espacio)
    except ReglaNegocioError as e:
        flash(str(e), "danger")
        return redirect(url_for("espacios.listar"))
    return render_template("espacios/form.html", espacio=espacio, modo="editar")


@bp.route("/<int:id_espacio>/eliminar", methods=["POST"])
def eliminar(id_espacio):
    try:
        espacio_service.eliminar_espacio(id_espacio)
        flash("Espacio eliminado.", "success")
    except ReglaNegocioError as e:
        flash(str(e), "danger")
    return redirect(url_for("espacios.listar"))
