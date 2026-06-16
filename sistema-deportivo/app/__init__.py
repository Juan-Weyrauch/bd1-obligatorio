"""App factory: API JSON + servidor de la SPA del frontend."""
from datetime import date, datetime, timedelta
from decimal import Decimal
from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider
from config import Config


class ProveedorJSON(DefaultJSONProvider):
    """Serializa los tipos de MySQL que el JSON estandar no entiende.

    - TIME (timedelta) -> "HH:MM"
    - DATE / DATETIME  -> ISO 8601 ("2026-06-15" / "2026-06-15T18:00:00")
    - DECIMAL          -> float (lo devuelven SUM, ROUND, etc.)
    """
    @staticmethod
    def default(o):
        if isinstance(o, timedelta):
            total = int(o.total_seconds())
            return f"{total // 3600:02d}:{(total % 3600) // 60:02d}"
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return float(o)
        return DefaultJSONProvider.default(o)


def create_app():
    """Construye la app Flask. Sirve frontend/ como estatico y expone la API."""
    app = Flask(__name__, static_folder="../frontend", static_url_path="")
    app.config.from_object(Config)
    app.json = ProveedorJSON(app)
    app.url_map.strict_slashes = False

    # --- API JSON (un blueprint por recurso) ---
    from app.routes.estudiantes import bp as estudiantes_bp
    from app.routes.actividades import bp as actividades_bp
    from app.routes.inscripciones import bp as inscripciones_bp
    from app.routes.disciplinas import bp as disciplinas_bp
    from app.routes.espacios import bp as espacios_bp
    from app.routes.carreras import bp as carreras_bp
    from app.routes.asistencias import bp as asistencias_bp
    from app.routes.reportes import bp as reportes_bp

    for bp in (estudiantes_bp, actividades_bp, inscripciones_bp, disciplinas_bp,
               espacios_bp, carreras_bp, asistencias_bp, reportes_bp):
        app.register_blueprint(bp)

    @app.route("/")
    def index():
        """Sirve la aplicacion de una sola pagina (frontend/index.html)."""
        return app.send_static_file("index.html")

    @app.route("/health")
    def health():
        """Prueba de conexion a la base de datos."""
        from app.db import get_connection
        try:
            conn = get_connection()
            conn.close()
            return jsonify({"estado": "ok"})
        except Exception as e:
            return jsonify({"estado": "error", "detalle": str(e)}), 500

    # La SPA siempre hace r.json(): convertimos los errores HTTP a JSON
    # para que el frontend nunca reciba una pagina HTML inesperada.
    @app.errorhandler(404)
    def _404(e):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(405)
    def _405(e):
        return jsonify({"error": "Metodo no permitido"}), 405

    @app.errorhandler(500)
    def _500(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    return app
