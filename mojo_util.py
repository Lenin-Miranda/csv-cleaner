import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd

import os
def detectar_mojo(headers):
    return 'zip_code' in headers and 'carrier_route' in headers

def preguntar_si_mojo():
    return messagebox.askyesno("Trabajo MOJO", "Se detectaron columnas ZIP y CRRT.\n¿Es este un trabajo MOJO?")


def obtener_datos_division():
    opcion = simpledialog.askstring("División", "¿Deseas dividir por 'piezas' o por 'partes'? (escribe piezas o partes)")
    if opcion not in ['piezas', 'partes']:
        messagebox.showwarning("Entrada inválida", "Debes escribir 'piezas' o 'partes'.")
        return None, None

    cantidad = simpledialog.askinteger("Cantidad", f"¿Cuántas {opcion}?")
    if not cantidad or cantidad <= 0:
        messagebox.showwarning("Cantidad inválida", "Ingresa un número válido.")
        return None, None
    
    

    return opcion, cantidad

def funcion_1_agregar_drop(df):
    """Ordena por ZIP y CRRT y agrega columna 'DROP' si no existe."""
    if 'zip_code' in df.columns and 'carrier_route' in df.columns:
        df = df.sort_values(by=['zip_code', 'carrier_route']).reset_index(drop=True)
    else:
        raise ValueError("Faltan las columnas 'zip_code' o 'carrier_route'.")

    if 'DROP' not in df.columns:
        df['DROP'] = "" # Inicializar columna 'DROP' vacia
        df = df[[col for col in df.columns if col != 'DROP'] + ['DROP']]
    return df 


def funcion_3_dividir(df, opcion, cantidad):
    import math

    grupos = df.groupby(['zip_code', 'carrier_route'])
    grupos_lista = [(clave, grupo) for clave, grupo in grupos]
    total_filas = sum(len(grupo) for _, grupo in grupos_lista)

    if opcion == 'piezas':
        max_filas_por_parte = cantidad
        num_partes = math.ceil(total_filas / max_filas_por_parte)
    else:  # opcion == 'partes'
        num_partes = cantidad
        max_filas_por_parte = math.ceil(total_filas / num_partes)

    partes = []
    parte_actual = []
    filas_actuales = 0

    for _, grupo in grupos_lista:
        n = len(grupo)

        if opcion == 'partes' and len(partes) == num_partes - 1:
            # Última parte: mete todo lo que queda
            parte_actual.append(grupo)
            continue

        if filas_actuales + n > max_filas_por_parte and parte_actual:
            partes.append(pd.concat(parte_actual).reset_index(drop=True))
            parte_actual = [grupo]
            filas_actuales = n
        else:
            parte_actual.append(grupo)
            filas_actuales += n

    if parte_actual:
        partes.append(pd.concat(parte_actual).reset_index(drop=True))

    return partes


def funcion_4_nombrar_partes(partes):
    total = function_6_preguntar_por_numero()
  
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if total > len(letras):
        raise ValueError("Demasiadas partes para nombrar con letras.")
    
    nombre_base = str(total)
    partes_nuevas = []
    
    for i, parte in enumerate(partes):
        letra = letras[i]
        drop_value = f"{nombre_base}{letra}"
        # Crear una copia explícita y asignar DROP
        parte_modificada = parte.copy()
        parte_modificada['DROP'] = drop_value
        partes_nuevas.append(parte_modificada)
    
    return partes_nuevas



def funcion_5_guardar_partes(partes, ruta_origen):
    carpeta_origen = os.path.dirname(ruta_origen)

    for i, parte in enumerate(partes):
        nombre_drop = parte['DROP'].iloc[0]
        nombre_archivo = f"LVCG_{nombre_drop}.csv"
        ruta_completa = os.path.join(carpeta_origen, nombre_archivo)
        parte.to_csv(ruta_completa, index=False)

def function_6_preguntar_por_numero():
    numero = simpledialog.askinteger("Numero de parte", "Que numero es el trabajo MOJO?")
    if numero is None or numero <= 0:
        messagebox.showwarning("Entrada invalida", "Debes ingresar un numero valido.")
        return None
    return numero