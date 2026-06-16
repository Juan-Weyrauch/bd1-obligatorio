"""API JSON para Actividad (ABM)."""
from flask import Blueprint, request, jsonify
from app.services import actividad_service
from app.api_utils import renombrar

bp = Blueprint("actividades", __name__)

MAPEO = {"disciplina_nombre": "disciplina", "espacio_nombre": "espacio"}


@bp.route("/actividades", methods=["GET"])
def listar():
    return jsonify(renombrar(actividad_service.listar_actividades(), MAPEO))


@bp.route("/actividades", methods=["POST"])
def crear():
    d = request.get_json(silent=True) or {}
    try:
        nuevo_id = actividad_service.crear_actividad(
            d.get("nombre"), d.get("id_disciplina"), d.get("id_espacio"),
            d.get("cupo_maximo"), d.get("dia_semana"), d.get("horario"),
            d.get("estado"),
        )
        return jsonify({"id_actividad": nuevo_id, "mensaje": "Actividad creada."}), 201
    except actividad_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/actividades/<int:id_actividad>", methods=["PUT"])
def actualizar(id_actividad):
    d = request.get_json(silent=True) or {}
    try:
        actividad_service.actualizar_actividad(
            id_actividad, d.get("nombre"), d.get("id_disciplina"),
            d.get("id_espacio"), d.get("cupo_maximo"), d.get("dia_semana"),
            d.get("horario"), d.get("estado"),
        )
        return jsonify({"mensaje": "Actividad actualizada."})
    except actividad_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/actividades/<int:id_actividad>", methods=["DELETE"])
def eliminar(id_actividad):
    try:
        actividad_service.eliminar_actividad(id_actividad)
        return jsonify({"mensaje": "Actividad eliminada."})
    except actividad_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400
