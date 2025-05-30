from tkinter import messagebox
from mojo_util import (
    detectar_mojo,
    preguntar_si_mojo,
    obtener_datos_division,
    funcion_1_agregar_drop,
    funcion_3_dividir,
    funcion_4_nombrar_partes
)

def procesar_archivo(df):
    headers = df.columns.tolist()

    if detectar_mojo(headers):
        es_mojo = preguntar_si_mojo()
        if es_mojo:
            opcion, cantidad = obtener_datos_division()
            if not opcion or not cantidad:
                messagebox.showwarning("Cancelado", "Proceso cancelado por el usuario.")
                return

            # Aplicar funciones MOJO
            df = funcion_1_agregar_drop(df)
            partes = funcion_3_dividir(df, opcion, cantidad)
            partes = funcion_4_nombrar_partes(partes)

            messagebox.showinfo("MOJO Completado", f"Trabajo MOJO procesado en {len(partes)} partes.")
            return partes  # Devuelve las partes si es necesario
        else:
            messagebox.showinfo("No MOJO", "El archivo no será tratado como MOJO.")
            return df
    else:
        messagebox.showinfo("No MOJO Detectado", "No se detectaron columnas típicas de MOJO.")
        return df
