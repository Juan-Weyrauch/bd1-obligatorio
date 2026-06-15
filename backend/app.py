from flask import Flask, request, jsonify
from flask_cors import CORS
from db import obtener_conexion

app = Flask(__name__)
CORS(app)  # Permite que el frontend pueda conectarse al backend

# ESTUDIANTES

@app.route("/estudiantes", methods=["GET"])
def listar_estudiantes():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id_estudiante, e.documento, e.nombre, e.apellido, e.email,
               c.nombre AS carrera, f.nombre AS facultad
        FROM estudiante e
        JOIN carrera c ON e.id_carrera = c.id_carrera
        JOIN facultad f ON c.id_facultad = f.id_facultad
        ORDER BY e.apellido, e.nombre
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/estudiantes", methods=["POST"])
def agregar_estudiante():
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO estudiante (documento, nombre, apellido, email, id_carrera)
        VALUES (%s, %s, %s, %s, %s)
    """, (datos["documento"], datos["nombre"], datos["apellido"], datos["email"], datos["id_carrera"]))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Estudiante agregado correctamente"}), 201

@app.route("/estudiantes/<int:id>", methods=["PUT"])
def editar_estudiante(id):
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE estudiante
        SET documento=%s, nombre=%s, apellido=%s, email=%s, id_carrera=%s
        WHERE id_estudiante=%s
    """, (datos["documento"], datos["nombre"], datos["apellido"], datos["email"], datos["id_carrera"], id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Estudiante actualizado correctamente"})

@app.route("/estudiantes/<int:id>", methods=["DELETE"])
def borrar_estudiante(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM estudiante WHERE id_estudiante=%s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Estudiante eliminado correctamente"})

# DISCIPLINAS

@app.route("/disciplinas", methods=["GET"])
def listar_disciplinas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM disciplina ORDER BY nombre")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/disciplinas", methods=["POST"])
def agregar_disciplina():
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO disciplina (nombre) VALUES (%s)", (datos["nombre"],))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Disciplina agregada correctamente"}), 201

@app.route("/disciplinas/<int:id>", methods=["PUT"])
def editar_disciplina(id):
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE disciplina SET nombre=%s WHERE id_disciplina=%s", (datos["nombre"], id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Disciplina actualizada correctamente"})

@app.route("/disciplinas/<int:id>", methods=["DELETE"])
def borrar_disciplina(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM disciplina WHERE id_disciplina=%s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Disciplina eliminada correctamente"})

# ESPACIOS

@app.route("/espacios", methods=["GET"])
def listar_espacios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM espacio ORDER BY nombre")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/espacios", methods=["POST"])
def agregar_espacio():
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO espacio (nombre, ubicacion) VALUES (%s, %s)", (datos["nombre"], datos["ubicacion"]))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Espacio agregado correctamente"}), 201

@app.route("/espacios/<int:id>", methods=["PUT"])
def editar_espacio(id):
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE espacio SET nombre=%s, ubicacion=%s WHERE id_espacio=%s", (datos["nombre"], datos["ubicacion"], id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Espacio actualizado correctamente"})

@app.route("/espacios/<int:id>", methods=["DELETE"])
def borrar_espacio(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM espacio WHERE id_espacio=%s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Espacio eliminado correctamente"})

# ACTIVIDADES

@app.route("/actividades", methods=["GET"])
def listar_actividades():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id_actividad, a.nombre, a.cupo_maximo, a.dia_semana, a.horario, a.estado,
               d.nombre AS disciplina, e.nombre AS espacio
        FROM actividad a
        JOIN disciplina d ON a.id_disciplina = d.id_disciplina
        JOIN espacio e ON a.id_espacio = e.id_espacio
        ORDER BY a.nombre
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/actividades", methods=["POST"])
def agregar_actividad():
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO actividad (nombre, id_disciplina, id_espacio, cupo_maximo, dia_semana, horario, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (datos["nombre"], datos["id_disciplina"], datos["id_espacio"], datos["cupo_maximo"], datos["dia_semana"], datos["horario"], datos["estado"]))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Actividad agregada correctamente"}), 201

@app.route("/actividades/<int:id>", methods=["PUT"])
def editar_actividad(id):
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE actividad
        SET nombre=%s, id_disciplina=%s, id_espacio=%s, cupo_maximo=%s, dia_semana=%s, horario=%s, estado=%s
        WHERE id_actividad=%s
    """, (datos["nombre"], datos["id_disciplina"], datos["id_espacio"], datos["cupo_maximo"], datos["dia_semana"], datos["horario"], datos["estado"], id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Actividad actualizada correctamente"})

@app.route("/actividades/<int:id>", methods=["DELETE"])
def borrar_actividad(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM actividad WHERE id_actividad=%s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Actividad eliminada correctamente"})

# INSCRIPCIONES

@app.route("/inscripciones", methods=["GET"])
def listar_inscripciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.id_inscripcion, i.estado, i.fecha_inscripcion, i.posicion_espera,
               e.nombre AS estudiante, e.apellido,
               a.nombre AS actividad
        FROM inscripcion i
        JOIN estudiante e ON i.id_estudiante = e.id_estudiante
        JOIN actividad a ON i.id_actividad = a.id_actividad
        ORDER BY a.nombre, e.apellido
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/inscripciones", methods=["POST"])
def inscribir_estudiante():
    datos = request.json
    id_estudiante = datos["id_estudiante"]
    id_actividad = datos["id_actividad"]

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Verificar que la actividad esté abierta
    cursor.execute("SELECT estado, cupo_maximo FROM actividad WHERE id_actividad=%s", (id_actividad,))
    actividad = cursor.fetchone()
    if actividad["estado"] != "abierta":
        cursor.close()
        conexion.close()
        return jsonify({"error": "La actividad no está abierta"}), 400

    # Verificar que el estudiante no esté ya inscripto
    cursor.execute("SELECT id_inscripcion FROM inscripcion WHERE id_estudiante=%s AND id_actividad=%s", (id_estudiante, id_actividad))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return jsonify({"error": "El estudiante ya está inscripto en esta actividad"}), 400

    # Contar confirmados para ver si hay cupo
    cursor.execute("SELECT COUNT(*) AS confirmados FROM inscripcion WHERE id_actividad=%s AND estado='confirmada'", (id_actividad,))
    confirmados = cursor.fetchone()["confirmados"]

    if confirmados < actividad["cupo_maximo"]:
        estado = "confirmada"
        posicion_espera = None
    else:
        estado = "en_espera"
        cursor.execute("SELECT COALESCE(MAX(posicion_espera), 0) + 1 AS proxima FROM inscripcion WHERE id_actividad=%s AND estado='en_espera'", (id_actividad,))
        posicion_espera = cursor.fetchone()["proxima"]

    cursor2 = conexion.cursor()
    cursor2.execute("""
        INSERT INTO inscripcion (id_estudiante, id_actividad, estado, posicion_espera)
        VALUES (%s, %s, %s, %s)
    """, (id_estudiante, id_actividad, estado, posicion_espera))
    conexion.commit()
    cursor.close()
    cursor2.close()
    conexion.close()
    return jsonify({"mensaje": f"Inscripción {estado} correctamente"}), 201

@app.route("/inscripciones/<int:id>", methods=["DELETE"])
def cancelar_inscripcion(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE inscripcion SET estado='cancelada' WHERE id_inscripcion=%s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Inscripción cancelada correctamente"})

# ASISTENCIAS

@app.route("/asistencias", methods=["POST"])
def registrar_asistencia():
    datos = request.json
    id_inscripcion = datos["id_inscripcion"]
    fecha = datos["fecha"]
    presente = datos["presente"]

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Verificar que la inscripción esté confirmada
    cursor.execute("SELECT estado FROM inscripcion WHERE id_inscripcion=%s", (id_inscripcion,))
    inscripcion = cursor.fetchone()
    if inscripcion["estado"] != "confirmada":
        cursor.close()
        conexion.close()
        return jsonify({"error": "El estudiante no tiene inscripción confirmada"}), 400

    cursor2 = conexion.cursor()
    cursor2.execute("""
        INSERT INTO asistencia (id_inscripcion, fecha, presente)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE presente=%s
    """, (id_inscripcion, fecha, presente, presente))
    conexion.commit()
    cursor.close()
    cursor2.close()
    conexion.close()
    return jsonify({"mensaje": "Asistencia registrada correctamente"}), 201

# REPORTES

@app.route("/reportes/inscriptos-por-actividad", methods=["GET"])
def inscriptos_por_actividad():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.nombre AS actividad, COUNT(i.id_inscripcion) AS total_confirmados
        FROM actividad a
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        GROUP BY a.id_actividad, a.nombre
        ORDER BY total_confirmados DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/reportes/cupos-disponibles", methods=["GET"])
def cupos_disponibles():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.nombre AS actividad, a.cupo_maximo,
               COUNT(i.id_inscripcion) AS confirmados,
               a.cupo_maximo - COUNT(i.id_inscripcion) AS cupos_disponibles
        FROM actividad a
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        WHERE a.estado = 'abierta'
        GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
        HAVING cupos_disponibles > 0
        ORDER BY cupos_disponibles DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/reportes/inscriptos-por-disciplina", methods=["GET"])
def inscriptos_por_disciplina():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.nombre AS disciplina, COUNT(i.id_inscripcion) AS total_inscriptos
        FROM disciplina d
        LEFT JOIN actividad a ON d.id_disciplina = a.id_disciplina
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        GROUP BY d.id_disciplina, d.nombre
        ORDER BY total_inscriptos DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/reportes/inscriptos-por-carrera", methods=["GET"])
def inscriptos_por_carrera():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.nombre AS facultad, c.nombre AS carrera,
               COUNT(DISTINCT i.id_estudiante) AS total_inscriptos
        FROM facultad f
        JOIN carrera c ON f.id_facultad = c.id_facultad
        JOIN estudiante e ON c.id_carrera = e.id_carrera
        LEFT JOIN inscripcion i ON e.id_estudiante = i.id_estudiante AND i.estado = 'confirmada'
        GROUP BY f.id_facultad, f.nombre, c.id_carrera, c.nombre
        ORDER BY total_inscriptos DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/reportes/ocupacion", methods=["GET"])
def porcentaje_ocupacion():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.nombre AS actividad, a.cupo_maximo,
               COUNT(i.id_inscripcion) AS confirmados,
               ROUND(COUNT(i.id_inscripcion) * 100.0 / a.cupo_maximo, 1) AS porcentaje_ocupacion
        FROM actividad a
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
        ORDER BY porcentaje_ocupacion DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/reportes/asistencia", methods=["GET"])
def porcentaje_asistencia():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.nombre AS actividad,
               COUNT(ast.id_asistencia) AS total_registros,
               SUM(CASE WHEN ast.presente = TRUE THEN 1 ELSE 0 END) AS presentes,
               ROUND(SUM(CASE WHEN ast.presente = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(ast.id_asistencia), 1) AS porcentaje_asistencia
        FROM actividad a
        JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
        JOIN asistencia ast ON i.id_inscripcion = ast.id_inscripcion
        GROUP BY a.id_actividad, a.nombre
        ORDER BY porcentaje_asistencia DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/reportes/inasistencias", methods=["GET"])
def estudiantes_con_inasistencias():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.documento, e.nombre, e.apellido, a.nombre AS actividad,
               COUNT(ast.id_asistencia) AS inasistencias
        FROM estudiante e
        JOIN inscripcion i ON e.id_estudiante = i.id_estudiante AND i.estado = 'confirmada'
        JOIN actividad a ON i.id_actividad = a.id_actividad
        JOIN asistencia ast ON i.id_inscripcion = ast.id_inscripcion AND ast.presente = FALSE
        GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido, a.id_actividad, a.nombre
        HAVING inasistencias >= 3
        ORDER BY inasistencias DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

# DATOS AUXILIARES

@app.route("/carreras", methods=["GET"])
def listar_carreras():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id_carrera, c.nombre, f.nombre AS facultad
        FROM carrera c
        JOIN facultad f ON c.id_facultad = f.id_facultad
        ORDER BY c.nombre
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/facultades", methods=["GET"])
def listar_facultades():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM facultad ORDER BY nombre")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

# ARRANCAR EL SERVIDOR

if __name__ == "__main__":
    app.run(debug=True)