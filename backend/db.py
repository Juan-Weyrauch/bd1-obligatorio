# db.py - Conexión a la base de datos MySQL

import mysql.connector

# Configuración de la conexión
CONFIGURACION = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "deportes_db"
}

def obtener_conexion():
    conexion = mysql.connector.connect(**CONFIGURACION)
    return conexion