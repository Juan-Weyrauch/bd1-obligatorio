"""API JSON para Espacio (ABM)."""
from flask import Blueprint, request, jsonify
from app.services import espacio_service

bp = Blueprint("espacios", __name__)


@bp.route("/espacios", methods=["GET"])
def listar():
    return jsonify(espacio_service.listar_espacios())


@bp.route("/espacios", methods=["POST"])
def crear():
    d = request.get_json(silent=True) or {}
    try:
        nuevo_id = espacio_service.crear_espacio(d.get("nombre"), d.get("ubicacion"))
        return jsonify({"id_espacio": nuevo_id, "mensaje": "Espacio creado."}), 201
    except espacio_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/espacios/<int:id_espacio>", methods=["PUT"])
def actualizar(id_espacio):
    d = request.get_json(silent=True) or {}
    try:
        espacio_service.actualizar_espacio(id_espacio, d.get("nombre"), d.get("ubicacion"))
        return jsonify({"mensaje": "Espacio actualizado."})
    except espacio_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/espacios/<int:id_espacio>", methods=["DELETE"])
def eliminar(id_espacio):
    try:
        espacio_service.eliminar_espacio(id_espacio)
        return jsonify({"mensaje": "Espacio eliminado."})
    except espacio_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400
