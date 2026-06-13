-- ============================================================
-- 03_seed.sql  --  Datos iniciales
-- Ejecutar DESPUÉS de 01_schema.sql
-- ============================================================
USE deportes_db;
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Facultades
INSERT INTO facultad (nombre) VALUES
    ('Facultad de Ingeniería'),
    ('Facultad de Ciencias Económicas');

-- Carreras
INSERT INTO carrera (nombre, id_facultad) VALUES
    ('Ingeniería en Sistemas', 1),
    ('Ingeniería Civil',       1),
    ('Contador Público',       2);

-- Disciplinas (del enunciado)
INSERT INTO disciplina (nombre) VALUES
    ('Fútbol'), ('Básquetbol'), ('Atletismo'),
    ('Volleyball'), ('Yoga'), ('Funcional'), ('Gimnasio');

-- Espacios
INSERT INTO espacio (nombre, ubicacion) VALUES
    ('Cancha principal', 'Sede central'),
    ('Gimnasio cubierto', 'Sede central'),
    ('Pista de atletismo', 'Anexo deportivo');

-- ---- Datos de ejemplo para pruebas (podés borrarlos luego) ----
INSERT INTO estudiante (documento, nombre, apellido, email, id_carrera) VALUES
    ('50001001', 'Ana',  'Pérez',    'ana.perez@uni.edu',  1),
    ('50001002', 'Luis', 'Gómez',    'luis.gomez@uni.edu', 2);

INSERT INTO actividad (nombre, id_disciplina, id_espacio, cupo_maximo, dia_semana, horario, estado) VALUES
    ('Fútbol recreativo mixto', 1, 1, 20, 'lunes',     '18:00:00', 'abierta'),
    ('Atletismo inicial',       3, 3, 15, 'miercoles', '08:00:00', 'abierta');
