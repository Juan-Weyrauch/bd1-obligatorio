-- ============================================================
-- consultas.sql
-- Consultas utiles para probar el sistema y para reutilizar en Python
-- ============================================================

USE deportes_db;

-- 1) Listado de estudiantes con su carrera y facultad
SELECT
    e.id_estudiante,
    e.documento,
    e.nombre,
    e.apellido,
    e.email,
    c.nombre AS carrera,
    f.nombre AS facultad
FROM estudiante e
JOIN carrera c ON c.id_carrera = e.id_carrera
JOIN facultad f ON f.id_facultad = c.id_facultad
ORDER BY e.apellido, e.nombre;

-- 2) Carreras agrupadas por facultad
SELECT
    f.nombre AS facultad,
    c.id_carrera,
    c.nombre AS carrera
FROM carrera c
JOIN facultad f ON f.id_facultad = c.id_facultad
ORDER BY f.nombre, c.nombre;

-- 3) Actividades con disciplina, espacio y cupo disponible
SELECT
    a.id_actividad,
    a.nombre,
    d.nombre AS disciplina,
    e.nombre AS espacio,
    e.ubicacion,
    a.cupo_maximo,
    a.dia_semana,
    a.horario,
    a.estado
FROM actividad a
JOIN disciplina d ON d.id_disciplina = a.id_disciplina
JOIN espacio e ON e.id_espacio = a.id_espacio
ORDER BY a.nombre;

-- 4) Cantidad de estudiantes por carrera
SELECT
    c.id_carrera,
    c.nombre AS carrera,
    f.nombre AS facultad,
    COUNT(e.id_estudiante) AS cantidad_estudiantes
FROM carrera c
JOIN facultad f ON f.id_facultad = c.id_facultad
LEFT JOIN estudiante e ON e.id_carrera = c.id_carrera
GROUP BY c.id_carrera, c.nombre, f.nombre
ORDER BY cantidad_estudiantes DESC, c.nombre;
