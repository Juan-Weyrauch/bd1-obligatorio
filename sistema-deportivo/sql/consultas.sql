USE deportes_db;

-- actividades con mayor cantidad de inscriptos confirmados
SELECT
    a.nombre AS actividad,
    d.nombre AS disciplina,
    COUNT(i.id_inscripcion) AS total_confirmados
FROM actividad a
JOIN disciplina d ON a.id_disciplina = d.id_disciplina
LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
GROUP BY a.id_actividad, a.nombre, d.nombre
ORDER BY total_confirmados DESC;

-- actividades con cupos disponibles
SELECT
    a.nombre AS actividad,
    a.cupo_maximo,
    COUNT(i.id_inscripcion) AS confirmados,
    a.cupo_maximo - COUNT(i.id_inscripcion) AS cupos_disponibles
FROM actividad a
LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
WHERE a.estado = 'abierta'
GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
HAVING cupos_disponibles > 0
ORDER BY cupos_disponibles DESC;

-- cantidad de inscriptos por disciplina
SELECT
    d.nombre AS disciplina,
    COUNT(i.id_inscripcion) AS total_inscriptos
FROM disciplina d
LEFT JOIN actividad a ON d.id_disciplina = a.id_disciplina
LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
GROUP BY d.id_disciplina, d.nombre
ORDER BY total_inscriptos DESC;

-- cantidad de inscriptos por carrera y facultad
SELECT
    f.nombre AS facultad,
    c.nombre AS carrera,
    COUNT(DISTINCT i.id_estudiante) AS total_inscriptos
FROM facultad f
JOIN carrera c ON f.id_facultad = c.id_facultad
JOIN estudiante e ON c.id_carrera = e.id_carrera
LEFT JOIN inscripcion i ON e.id_estudiante = i.id_estudiante AND i.estado = 'confirmada'
GROUP BY f.id_facultad, f.nombre, c.id_carrera, c.nombre
ORDER BY f.nombre, total_inscriptos DESC;

-- porcentaje de ocupación de cada actividad
SELECT
    a.nombre AS actividad,
    a.cupo_maximo,
    COUNT(i.id_inscripcion) AS confirmados,
    ROUND(COUNT(i.id_inscripcion) * 100.0 / a.cupo_maximo, 1) AS porcentaje_ocupacion
FROM actividad a
LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
ORDER BY porcentaje_ocupacion DESC;

-- porcentaje de asistencia por actividad
SELECT
    a.nombre AS actividad,
    COUNT(ast.id_asistencia) AS total_registros,
    SUM(CASE WHEN ast.presente = TRUE THEN 1 ELSE 0 END) AS presentes,
    ROUND(SUM(CASE WHEN ast.presente = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(ast.id_asistencia), 1) AS porcentaje_asistencia
FROM actividad a
JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
JOIN asistencia ast ON i.id_inscripcion = ast.id_inscripcion
GROUP BY a.id_actividad, a.nombre
ORDER BY porcentaje_asistencia DESC;

-- estudiantes con 3 o más inasistencias registradas
SELECT
    e.documento,
    e.nombre,
    e.apellido,
    a.nombre AS actividad,
    COUNT(ast.id_asistencia) AS inasistencias
FROM estudiante e
JOIN inscripcion i ON e.id_estudiante = i.id_estudiante AND i.estado = 'confirmada'
JOIN actividad a ON i.id_actividad = a.id_actividad
JOIN asistencia ast ON i.id_inscripcion = ast.id_inscripcion AND ast.presente = FALSE
GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido, a.id_actividad, a.nombre
HAVING inasistencias >= 3
ORDER BY inasistencias DESC;

-- estudiantes que nunca se inscribieron a ninguna actividad
SELECT
    e.documento,
    e.nombre,
    e.apellido,
    c.nombre AS carrera
FROM estudiante e
JOIN carrera c ON e.id_carrera = c.id_carrera
WHERE e.id_estudiante NOT IN (
    SELECT DISTINCT id_estudiante FROM inscripcion
)
ORDER BY e.apellido, e.nombre;

-- disciplina con más inscriptos

SELECT
    d.nombre AS disciplina,
    COUNT(i.id_inscripcion) AS total_inscriptos
FROM disciplina d
JOIN actividad a ON d.id_disciplina = a.id_disciplina
JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada'
GROUP BY d.id_disciplina, d.nombre
ORDER BY total_inscriptos DESC
LIMIT 1;

-- actividades que nunca tuvieron ningún inscripto
SELECT
    a.nombre AS actividad,
    d.nombre AS disciplina,
    a.estado
FROM actividad a
JOIN disciplina d ON a.id_disciplina = d.id_disciplina
WHERE a.id_actividad NOT IN (
    SELECT DISTINCT id_actividad FROM inscripcion
)
ORDER BY a.nombre;