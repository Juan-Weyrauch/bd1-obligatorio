"""API JSON para Disciplina (ABM)."""
from flask import Blueprint, request, jsonify
from app.services import disciplina_service

bp = Blueprint("disciplinas", __name__)


@bp.route("/disciplinas", methods=["GET"])
def listar():
    return jsonify(disciplina_service.listar_disciplinas())


@bp.route("/disciplinas", methods=["POST"])
def crear():
    d = request.get_json(silent=True) or {}
    try:
        nuevo_id = disciplina_service.crear_disciplina(d.get("nombre"))
        return jsonify({"id_disciplina": nuevo_id, "mensaje": "Disciplina creada."}), 201
    except disciplina_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/disciplinas/<int:id_disciplina>", methods=["PUT"])
def actualizar(id_disciplina):
    d = request.get_json(silent=True) or {}
    try:
        disciplina_service.actualizar_disciplina(id_disciplina, d.get("nombre"))
        return jsonify({"mensaje": "Disciplina actualizada."})
    except disciplina_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/disciplinas/<int:id_disciplina>", methods=["DELETE"])
def eliminar(id_disciplina):
    try:
        disciplina_service.eliminar_disciplina(id_disciplina)
        return jsonify({"mensaje": "Disciplina eliminada."})
    except disciplina_service.ReglaNegocioError as e:
        return jsonify({"error": str(e)}), 400
