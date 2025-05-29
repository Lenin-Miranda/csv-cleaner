import os
import json

ARCHIVO_HISTORIAL = "historial.json"
MAX_ENTRADAS = 10

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
      try:
         with open(ARCHIVO_HISTORIAL, "r") as f:
            return json.load(f)
      except json.JSONDecodeError:
            return []
    return []


def guardar_en_historial(ruta):
    historial = cargar_historial()
    if ruta in historial:
        historial.remove(ruta) # Eliminar si ya existe
    historial.insert(0, ruta) # Insertar al inicio
    historial = historial[:MAX_ENTRADAS] 
    with open(ARCHIVO_HISTORIAL, "w") as f:
        json.dump(historial, f)


def limpiar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        os.remove(ARCHIVO_HISTORIAL)