-- Sistema de Gestión de Actividades Deportivas Universitarias
-- Creación de base de datos y tablas

CREATE DATABASE IF NOT EXISTS deportes_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE deportes_db;

-- Borrado en orden inverso a las dependencias
DROP TABLE IF EXISTS asistencia;
DROP TABLE IF EXISTS inscripcion;
DROP TABLE IF EXISTS actividad;
DROP TABLE IF EXISTS espacio;
DROP TABLE IF EXISTS disciplina;
DROP TABLE IF EXISTS estudiante;
DROP TABLE IF EXISTS carrera;
DROP TABLE IF EXISTS facultad;

-- FACULTAD
CREATE TABLE facultad (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT uq_facultad_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

-- CARRERA (1 facultad, N carreras)
CREATE TABLE carrera (
    id_carrera  INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_facultad INT NOT NULL,
    -- Si dos facultades pudieran tener una carrera con el mismo nombre,
    -- cambiar por: UNIQUE (nombre, id_facultad)
    CONSTRAINT uq_carrera_nombre UNIQUE (nombre),
    CONSTRAINT fk_carrera_facultad FOREIGN KEY (id_facultad)
        REFERENCES facultad (id_facultad)
) ENGINE=InnoDB;

-- ESTUDIANTE (1 carrera, N estudiantes)
-- documento y email son claves candidatas -> UNIQUE
CREATE TABLE estudiante (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    documento VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    id_carrera INT NOT NULL,
    CONSTRAINT uq_estudiante_documento UNIQUE (documento),
    CONSTRAINT uq_estudiante_email UNIQUE (email),
    CONSTRAINT fk_estudiante_carrera FOREIGN KEY (id_carrera)
        REFERENCES carrera (id_carrera)
) ENGINE=InnoDB;

-- DISCIPLINA
CREATE TABLE disciplina (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT uq_disciplina_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

-- ESPACIO
-- clave candidata: combinación nombre + ubicacion
CREATE TABLE espacio (
    id_espacio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(150) NOT NULL,
    CONSTRAINT uq_espacio UNIQUE (nombre, ubicacion)
) ENGINE=InnoDB;

-- ACTIVIDAD (1 disciplina : N actividades / 1 espacio : N actividades)
-- estado controlado por ENUM, cupo positivo por CHECK
CREATE TABLE actividad (
    id_actividad  INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    id_disciplina INT NOT NULL,
    id_espacio INT NOT NULL,
    cupo_maximo INT NOT NULL,
    dia_semana ENUM('lunes','martes','miercoles','jueves',
                       'viernes','sabado','domingo') NOT NULL,
    horario TIME NOT NULL,
    estado ENUM('abierta','cerrada','finalizada','cancelada')
                       NOT NULL DEFAULT 'abierta',
    CONSTRAINT fk_actividad_disciplina FOREIGN KEY (id_disciplina)
        REFERENCES disciplina (id_disciplina),
    CONSTRAINT fk_actividad_espacio FOREIGN KEY (id_espacio)
        REFERENCES espacio (id_espacio),
    CONSTRAINT chk_actividad_cupo CHECK (cupo_maximo > 0)
) ENGINE=InnoDB;

-- INSCRIPCION (resuelve el M:N estudiante-actividad)
-- UNIQUE compuesto = regla "no inscribirse dos veces"
CREATE TABLE inscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_actividad INT NOT NULL,
    fecha_inscripcion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('confirmada','en_espera','cancelada') NOT NULL,
    posicion_espera INT NULL,
    CONSTRAINT uq_inscripcion UNIQUE (id_estudiante, id_actividad),
    CONSTRAINT fk_inscripcion_estudiante FOREIGN KEY (id_estudiante)
        REFERENCES estudiante (id_estudiante),
    CONSTRAINT fk_inscripcion_actividad FOREIGN KEY (id_actividad)
        REFERENCES actividad (id_actividad),
    CONSTRAINT chk_inscripcion_posicion
        CHECK (posicion_espera IS NULL OR posicion_espera > 0)
) ENGINE=InnoDB;

-- ASISTENCIA (depende de una inscripción)
-- UNIQUE (id_inscripcion, fecha) = una asistencia por día
CREATE TABLE asistencia (
    id_asistencia  INT AUTO_INCREMENT PRIMARY KEY,
    id_inscripcion INT NOT NULL,
    fecha DATE NOT NULL,
    presente BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT uq_asistencia UNIQUE (id_inscripcion, fecha),
    CONSTRAINT fk_asistencia_inscripcion FOREIGN KEY (id_inscripcion)
        REFERENCES inscripcion (id_inscripcion)
) ENGINE=InnoDB;

-- ÍNDICES adicionales (acelerar reportes pedidos en el enunciado)
-- Las FK ya crean su índice, estos son para filtros frecuentes
CREATE INDEX idx_actividad_estado
    ON actividad (estado);
CREATE INDEX idx_inscripcion_actividad_estado
    ON inscripcion (id_actividad, estado);
CREATE INDEX idx_asistencia_presente
    ON asistencia (presente);