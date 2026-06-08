# Configuración de la base de datos

Guía para levantar la base de datos del **Sistema de Gestión de Actividades
Deportivas Universitarias** desde cero. Al terminar vas a tener la base
`deportes_db` con sus 8 tablas y los datos de ejemplo cargados.

## Requisitos previos

- **Docker Desktop** instalado y corriendo.
- Un cliente SQL: DataGrip, MySQL Workbench o cualquier otro.
- **Python 3.11+** (solo para el paso final que prueba la app).

## Pasos para tener la base con las 8 tablas y datos de ejemplo

### 1. Actualizar el docker-compose

Usar el `docker-compose.yml` del repo (ya actualizado). La imagen pasó de
`mysql:5.7` a `mysql:8.0` porque la 5.7 ignora silenciosamente las
restricciones `CHECK` del esquema (`cupo_maximo > 0`, `posicion_espera > 0`).
Con MySQL 8 esas validaciones de integridad sí se aplican.

### 2. Levantar el contenedor de MySQL

Parado en la carpeta donde está el `docker-compose.yml`, en una terminal:

```bash
docker compose up -d
```

> Si ya habías levantado antes la versión 5.7, primero borrá el volumen viejo
> para que MySQL 8 inicialice limpio:
>
> ```bash
> docker compose down -v
> docker compose up -d
> ```

### 3. Verificar que el contenedor está corriendo

```bash
docker compose ps
```

El servicio `db` debe figurar como `running` / `healthy`. La primera vez,
MySQL tarda unos ~15 segundos en terminar de inicializar.

### 4. Conectarse a la base desde el cliente SQL

Usar las credenciales del `docker-compose.yml`:

| Campo        | Valor          |
| ------------ | -------------- |
| Host         | `localhost`    |
| Puerto       | `3306`         |
| Usuario      | `root`         |
| Contraseña   | `rootpassword` |
| Database     | dejar **vacío** la primera vez |

> El campo Database se deja vacío porque la base todavía no existe: la crea el
> script del paso 5. (En DataGrip, si pide bajar el driver de MySQL, aceptar el
> **Download** antes de hacer Test Connection.)

### 5. Ejecutar el esquema

Abrir y correr **completo** el script `sql/01_schema.sql`. Este crea la base
`deportes_db` y las 8 tablas con todas sus restricciones (PK, FK, UNIQUE,
CHECK, NOT NULL e índices).

### 6. Ejecutar los datos

Abrir y correr **completo** el script `sql/03_seed.sql`. Carga los datos
maestros (facultades, carreras, disciplinas, espacios) y algunos datos de
ejemplo para pruebas.

> **El orden importa: primero `01_schema.sql`, después `03_seed.sql`.** El seed
> inserta datos que dependen de las tablas creadas por el esquema.

### 7. Verificar que quedó todo bien

En una consola SQL:

```sql
USE deportes_db;
SELECT VERSION();          -- debe empezar con 8.0
SHOW TABLES;               -- deben aparecer las 8 tablas
SELECT * FROM disciplina;  -- deben estar las 7 disciplinas
```

Las 8 tablas esperadas son: `facultad`, `carrera`, `estudiante`, `disciplina`,
`espacio`, `actividad`, `inscripcion`, `asistencia`.

### 8. Configurar el `.env` de la app

Copiar `.env.example` a `.env` y completar con las credenciales del contenedor:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=deportes_db
```

> El archivo `.env` está en el `.gitignore` y **no se sube al repo**. Solo se
> versiona `.env.example` como plantilla.

### 9. Probar la conexión desde la app

Con el entorno virtual activo y las dependencias instaladas:

```bash
python -m pip install -r requirements.txt
python run.py
```

Abrir `http://127.0.0.1:5000/health` en el navegador. Si muestra
**"OK — conexión a MySQL exitosa"**, la base quedó lista.

## Notas para Windows 11

- Activar el entorno virtual en PowerShell: `.\venv\Scripts\Activate.ps1`
  (el prompt pasa a mostrar `(venv)`).
- Si Smart App Control bloquea `pip.exe`, invocar pip como módulo:
  `python -m pip ...` en lugar de `pip ...`.
- Docker corre dentro de su propio contenedor, así que MySQL **no** aparece en
  `Get-Service`; para verlo se usa `docker compose ps`.
