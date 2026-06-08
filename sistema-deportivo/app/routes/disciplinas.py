"""Capa de presentación para Disciplina (ABM).
Solo traduce HTTP <-> servicio y renderiza HTML."""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from app.services import disciplina_service
from app.services.disciplina_service import ReglaNegocioError

bp = Blueprint("disciplinas", __name__, url_prefix="/disciplinas")


@bp.route("/")
def listar():
    disciplinas = disciplina_service.listar_disciplinas()
    return render_template("disciplinas/listar.html", disciplinas=disciplinas)


@bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        try:
            disciplina_service.crear_disciplina(request.form.get("nombre"))
            flash("Disciplina creada correctamente.", "success")
            return redirect(url_for("disciplinas.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            # Re-render conservando lo que escribió el usuario
            return render_template(
                "disciplinas/form.html",
                disciplina={"nombre": request.form.get("nombre", "")},
                modo="crear",
            )
    return render_template("disciplinas/form.html", disciplina=None, modo="crear")


@bp.route("/<int:id_disciplina>/editar", methods=["GET", "POST"])
def editar(id_disciplina):
    if request.method == "POST":
        try:
            disciplina_service.actualizar_disciplina(
                id_disciplina, request.form.get("nombre")
            )
            flash("Disciplina actualizada correctamente.", "success")
            return redirect(url_for("disciplinas.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return render_template(
                "disciplinas/form.html",
                disciplina={"id_disciplina": id_disciplina,
                            "nombre": request.form.get("nombre", "")},
                modo="editar",
            )
    try:
        disciplina = disciplina_service.obtener_disciplina(id_disciplina)
    except ReglaNegocioError as e:
        flash(str(e), "danger")
        return redirect(url_for("disciplinas.listar"))
    return render_template("disciplinas/form.html", disciplina=disciplina, modo="editar")


@bp.route("/<int:id_disciplina>/eliminar", methods=["POST"])
def eliminar(id_disciplina):
    try:
        disciplina_service.eliminar_disciplina(id_disciplina)
        flash("Disciplina eliminada.", "success")
    except ReglaNegocioError as e:
        flash(str(e), "danger")
    return redirect(url_for("disciplinas.listar"))