"""API JSON para Inscripcion."""
from flask import Blueprint, request, jsonify
from app.services import inscripcion_service
from app.api_utils import renombrar

bp = Blueprint("inscripciones", __name__)

MAPEO = {
    "estudiante_nombre": "nombre",
    "estudiante_apellido": "apellido",
    "actividad_nombre": "actividad",
}


@bp.route("/inscripciones", methods=["GET"])
def listar():
    return jsonify(renombrar(inscripcion_service.listar_inscripciones(), MAPEO))


@bp.route("/inscripciones", methods=["POST"])
def crear():
    d = request.get_json(silent=True) or {}
    try:
        mensaje = inscripcion_service.crear_inscripcion(
            d.get("id_estudiante"), d.get("id_actividad"),
        )
        return jsonify({"mensaje": mensaje}), 201
    except inscripcion_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/inscripciones/<int:id_inscripcion>", methods=["DELETE"])
def cancelar(id_inscripcion):
    try:
        mensaje = inscripcion_service.cancelar_inscripcion(id_inscripcion)
        return jsonify({"mensaje": mensaje})
    except inscripcion_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400
