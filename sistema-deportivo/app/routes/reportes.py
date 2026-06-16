"""API JSON para los reportes/consultas (solo lectura)."""
from flask import Blueprint, jsonify
from app.repositories import reporte_repo

bp = Blueprint("reportes", __name__)


@bp.route("/reportes/<nombre>", methods=["GET"])
def reporte(nombre):
    try:
        return jsonify(reporte_repo.obtener(nombre))
    except KeyError:
        return jsonify({"error": f"Reporte desconocido: {nombre}"}), 404
