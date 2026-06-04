from flask import Flask
from config import Config


def create_app():
    """Construye y configura la aplicación Flask (patrón app factory)."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Registro de blueprints (se irán agregando en cada fase) ---
    # from app.routes.disciplinas import bp as disciplinas_bp
    # app.register_blueprint(disciplinas_bp)

    @app.route("/")
    def index():
        return "<h1>Sistema de Actividades Deportivas</h1><p>App funcionando.</p>"

    @app.route("/health")
    def health():
        """Prueba de conexión a la base de datos."""
        from app.db import get_connection
        try:
            conn = get_connection()
            conn.close()
            return "OK — conexión a MySQL exitosa"
        except Exception as e:
            return f"ERROR de conexión: {e}", 500

    return app