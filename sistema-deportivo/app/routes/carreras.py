"""API JSON para Carrera (solo lectura: dato maestro para los formularios)."""
from flask import Blueprint, jsonify
from app.services import carrera_service
from app.api_utils import renombrar

bp = Blueprint("carreras", __name__)


@bp.route("/carreras", methods=["GET"])
def listar():
    return jsonify(renombrar(carrera_service.listar_carreras(),
                             {"facultad_nombre": "facultad"}))
