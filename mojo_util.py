import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
def detectar_mojo(headers):
    return 'ZIP CODE' in headers and 'CRRT' in headers

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
    if 'ZIP' in df.columns and 'CRRT' in df.columns:
        df = df.sort_values(by=['ZIP', 'CRRT']).reset_index(drop=True)
    else:
        raise ValueError("Faltan las columnas 'ZIP' o 'CRRT'.")

    if 'DROP' not in df.columns:
        df['DROP'] = ''
    else: 
        drop_col = df.pop('DROP')
        df['DROP'] = drop_col

    return df



def funcion_3_dividir(df, opcion, cantidad):
    """Divide el DataFrame por piezas o partes sin cortar CRRTs"""
    from itertools import accumulate
    import math

    # Agrupar por ZIP y CRRT
    grupos = df.groupby(['ZIP', 'CRRT'])
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
        if filas_actuales + n > max_filas_por_parte and parte_actual:
            # Guardar la parte actual
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
    total = len(partes)
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if total > len(letras):
        raise ValueError("Demasiadas partes para nombrar con letras.")
    
    nombre_base = str(total)
    
    for i, parte in enumerate(partes):
        letra = letras[i]
        drop_value = f"{nombre_base}{letra}"
        parte['DROP'] = drop_value
    
    return partes

 