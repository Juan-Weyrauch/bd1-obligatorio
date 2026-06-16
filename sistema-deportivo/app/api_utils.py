"""Utilidades chicas para la capa API.

Los repositorios devuelven columnas con alias tipo 'carrera_nombre'.
La SPA del frontend espera nombres mas cortos ('carrera'). Esta funcion
hace ese mapeo en un solo lugar, sin tocar el SQL de los repositorios.
"""


def renombrar(filas, mapeo):
    """Devuelve las filas con algunas claves renombradas.

    filas: lista de dicts (filas del cursor)
    mapeo: dict {clave_origen: clave_destino}
    """
    resultado = []
    for fila in filas:
        nueva = dict(fila)
        for origen, destino in mapeo.items():
            if origen in nueva:
                nueva[destino] = nueva.pop(origen)
        resultado.append(nueva)
    return resultado
