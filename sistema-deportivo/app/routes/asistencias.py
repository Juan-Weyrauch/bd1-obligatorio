"""API JSON para Asistencia."""
from flask import Blueprint, request, jsonify
from app.services import asistencia_service

bp = Blueprint("asistencias", __name__)


@bp.route("/asistencias", methods=["POST"])
def registrar():
    d = request.get_json(silent=True) or {}
    try:
        mensaje = asistencia_service.registrar_asistencia(
            d.get("id_inscripcion"), d.get("fecha"), d.get("presente"),
        )
        return jsonify({"mensaje": mensaje}), 201
    except asistencia_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400
