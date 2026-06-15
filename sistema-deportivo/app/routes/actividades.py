"""Capa de presentacion para Actividad (ABM)."""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from app.services import actividad_service
from app.services.actividad_service import (
    ReglaNegocioError, DIAS_SEMANA, ESTADOS_ACTIVIDAD
)

bp = Blueprint("actividades", __name__, url_prefix="/actividades")


def _render_formulario(actividad, modo):
    disciplinas = actividad_service.listar_disciplinas_para_formulario()
    espacios = actividad_service.listar_espacios_para_formulario()
    return render_template(
        "actividades/form.html",
        actividad=actividad,
        disciplinas=disciplinas,
        espacios=espacios,
        dias_semana=DIAS_SEMANA,
        estados=ESTADOS_ACTIVIDAD,
        modo=modo,
    )


@bp.route("/")
def listar():
    actividades = actividad_service.listar_actividades()
    return render_template("actividades/listar.html", actividades=actividades)


@bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        actividad = {
            "nombre": request.form.get("nombre", ""),
            "id_disciplina": request.form.get("id_disciplina", ""),
            "id_espacio": request.form.get("id_espacio", ""),
            "cupo_maximo": request.form.get("cupo_maximo", ""),
            "dia_semana": request.form.get("dia_semana", ""),
            "horario": request.form.get("horario", ""),
            "estado": request.form.get("estado", ""),
        }
        try:
            actividad_service.crear_actividad(
                actividad["nombre"],
                actividad["id_disciplina"],
                actividad["id_espacio"],
                actividad["cupo_maximo"],
                actividad["dia_semana"],
                actividad["horario"],
                actividad["estado"],
            )
            flash("Actividad creada correctamente.", "success")
            return redirect(url_for("actividades.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return _render_formulario(actividad, "crear")
    return _render_formulario(None, "crear")


@bp.route("/<int:id_actividad>/editar", methods=["GET", "POST"])
def editar(id_actividad):
    if request.method == "POST":
        actividad = {
            "id_actividad": id_actividad,
            "nombre": request.form.get("nombre", ""),
            "id_disciplina": request.form.get("id_disciplina", ""),
            "id_espacio": request.form.get("id_espacio", ""),
            "cupo_maximo": request.form.get("cupo_maximo", ""),
            "dia_semana": request.form.get("dia_semana", ""),
            "horario": request.form.get("horario", ""),
            "estado": request.form.get("estado", ""),
        }
        try:
            actividad_service.actualizar_actividad(
                id_actividad,
                actividad["nombre"],
                actividad["id_disciplina"],
                actividad["id_espacio"],
                actividad["cupo_maximo"],
                actividad["dia_semana"],
                actividad["horario"],
                actividad["estado"],
            )
            flash("Actividad actualizada correctamente.", "success")
            return redirect(url_for("actividades.listar"))
        except ReglaNegocioError as e:
            flash(str(e), "danger")
            return _render_formulario(actividad, "editar")
    try:
        actividad = actividad_service.obtener_actividad(id_actividad)
    except ReglaNegocioError as e:
        flash(str(e), "danger")
        return redirect(url_for("actividades.listar"))
    return _render_formulario(actividad, "editar")


@bp.route("/<int:id_actividad>/eliminar", methods=["POST"])
def eliminar(id_actividad):
    try:
        actividad_service.eliminar_actividad(id_actividad)
        flash("Actividad eliminada.", "success")
    except ReglaNegocioError as e:
        flash(str(e), "danger")
    return redirect(url_for("actividades.listar"))
