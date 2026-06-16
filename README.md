# Sistema de Gestión de Actividades Deportivas Universitarias

Obligatorio de **Bases de Datos 1**. Sistema para administrar inscripciones de
estudiantes a actividades deportivas universitarias: control de cupos, lista de
espera, registro de asistencias y reportes.

## Stack

- **Base de datos:** MySQL 8.0
- **Backend:** Python + Flask
- **Frontend:** SPA en HTML/CSS/JavaScript (servida por el propio Flask)
- **Driver:** `mysql-connector-python`

La arquitectura del backend está separada en capas: 
`routes` (API JSON) ->
`services` (reglas de negocio) -> 
`repositories` (único lugar con SQL) -> MySQL.
La validación ocurre en tres niveles: frontend (formato), backend (reglas de
negocio) y base de datos (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, ENUM).


## Requisitos previos

- Python 3.13
- MySQL 8.0 (local o vía Docker — ver `docs/setup-base-de-datos.md`)


## Puesta en marcha

```bash
# 1. Entorno virtual
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Dependencias
cd sistema-deportivo
python -m pip install -r requirements.txt

# 3. Configuración: copiar el ejemplo y completar credenciales
copy .env.example .env        # Windows  (cp en Linux/Mac)

# 4. Base de datos: crear la base y cargar esquema + datos maestros
#    (guía detallada con Docker en docs/setup-base-de-datos.md)
mysql -u root -p deportes_db < sql/schema.sql
mysql -u root -p deportes_db < sql/datos.sql

# 5. Correr la aplicación
python run.py
```

Luego abrir **http://127.0.0.1:5000/** en el navegador.

Prueba rápida de que todo conecta: **http://127.0.0.1:5000/health** debe
responder `{"estado": "ok"}`.

## Estructura

```
sistema-deportivo/
├── app/
│   ├── routes/         # API JSON (un archivo por recurso)
│   ├── services/       # reglas de negocio y validaciones
│   ├── repositories/   # acceso a datos (único lugar con SQL)
│   ├── db.py           # conexión a MySQL
│   └── __init__.py     # app factory + serialización JSON
├── frontend/           # SPA (index.html, script.js, style.css)
├── sql/
│   ├── schema.sql      # DDL: 8 tablas con todas las restricciones
│   ├── datos.sql       # datos maestros de ejemplo
│   └── consultas.sql   # las 10 consultas pedidas por la letra
├── config.py           # lee el .env
└── run.py              # punto de entrada (sirve API + SPA en :5000)
```
