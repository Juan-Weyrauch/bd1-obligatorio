"""API JSON para Estudiante (ABM)."""
from flask import Blueprint, request, jsonify
from app.services import estudiante_service
from app.api_utils import renombrar

bp = Blueprint("estudiantes", __name__)

# El repo trae 'carrera_nombre'/'facultad_nombre'; la SPA usa 'carrera'/'facultad'.
MAPEO = {"carrera_nombre": "carrera", "facultad_nombre": "facultad"}


@bp.route("/estudiantes", methods=["GET"])
def listar():
    return jsonify(renombrar(estudiante_service.listar_estudiantes(), MAPEO))


@bp.route("/estudiantes", methods=["POST"])
def crear():
    datos = request.get_json(silent=True) or {}
    try:
        nuevo_id = estudiante_service.crear_estudiante(
            datos.get("documento"), datos.get("nombre"), datos.get("apellido"),
            datos.get("email"), datos.get("id_carrera"),
        )
        return jsonify({"id_estudiante": nuevo_id, "mensaje": "Estudiante creado."}), 201
    except estudiante_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/estudiantes/<int:id_estudiante>", methods=["PUT"])
def actualizar(id_estudiante):
    datos = request.get_json(silent=True) or {}
    try:
        estudiante_service.actualizar_estudiante(
            id_estudiante, datos.get("documento"), datos.get("nombre"),
            datos.get("apellido"), datos.get("email"), datos.get("id_carrera"),
        )
        return jsonify({"mensaje": "Estudiante actualizado."})
    except estudiante_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/estudiantes/<int:id_estudiante>", methods=["DELETE"])
def eliminar(id_estudiante):
    try:
        estudiante_service.eliminar_estudiante(id_estudiante)
        return jsonify({"mensaje": "Estudiante eliminado."})
    except estudiante_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400
