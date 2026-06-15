from flask import Flask
from config import Config


def create_app():
    """Construye y configura la aplicación Flask (patrón app factory)."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Asegurar UTF-8 en respuestas
    app.config['JSON_AS_ASCII'] = False

    # --- Registro de blueprints (se irán agregando en cada fase) ---
    from app.routes.disciplinas import bp as disciplinas_bp
    from app.routes.espacios import bp as espacios_bp
    from app.routes.actividades import bp as actividades_bp
    app.register_blueprint(disciplinas_bp)
    app.register_blueprint(espacios_bp)
    app.register_blueprint(actividades_bp)

    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")

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
