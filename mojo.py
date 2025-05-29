import tkinter as tk
from tkinter import messagebox, simpledialog

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

    return df

def funcion_3_dividir(df, opcion, cantidad):
    """Divide el DataFrame en partes segun la opcion y cantidad"""
    if opcion == 'piezas':
     partes = []

def procesar_archivo(df):
    headers = df.columns.tolist()

    if detectar_mojo(headers):
        es_mojo = preguntar_si_mojo()
        if es_mojo:
            opcion, cantidad = obtener_datos_division()
            if not opcion:
                return

        
    

            # 2. Aplicar funciones opcionales
            df = funcion_1_agregar_drop(df)
            partes = funcion_3_dividir(df, opcion, cantidad)
            partes = funcion_4_nombrar_partes(partes)
            funcion_6_guardar_historial(partes)

            messagebox.showinfo("MOJO Completado", f"Trabajo MOJO procesado en {len(partes)} partes.")
            return
