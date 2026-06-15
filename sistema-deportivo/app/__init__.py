from datetime import timedelta
from flask import Flask
from config import Config


def create_app():
    """Construye y configura la aplicación Flask (patrón app factory)."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Asegurar UTF-8 en respuestas
    app.config['JSON_AS_ASCII'] = False

    @app.template_filter("formatear_hora")
    def formatear_hora(valor):
        """Devuelve una hora en formato HH:MM para templates."""
        if valor is None:
            return ""
        if isinstance(valor, timedelta):
            total_seconds = int(valor.total_seconds())
            horas = total_seconds // 3600
            minutos = (total_seconds % 3600) // 60
            return f"{horas:02d}:{minutos:02d}"
        texto = str(valor)
        return texto[:5]

    # --- Registro de blueprints (se irán agregando en cada fase) ---
    from app.routes.disciplinas import bp as disciplinas_bp
    from app.routes.espacios import bp as espacios_bp
    from app.routes.actividades import bp as actividades_bp
    from app.routes.facultades import bp as facultades_bp
    from app.routes.carreras import bp as carreras_bp
    from app.routes.estudiantes import bp as estudiantes_bp
    from app.routes.inscripciones import bp as inscripciones_bp
    app.register_blueprint(disciplinas_bp)
    app.register_blueprint(espacios_bp)
    app.register_blueprint(actividades_bp)
    app.register_blueprint(facultades_bp)
    app.register_blueprint(carreras_bp)
    app.register_blueprint(estudiantes_bp)
    app.register_blueprint(inscripciones_bp)

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
