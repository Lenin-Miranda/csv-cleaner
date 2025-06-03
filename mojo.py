from tkinter import messagebox
from mojo_util import (
    detectar_mojo,
    preguntar_si_mojo,
    obtener_datos_division,
    funcion_1_agregar_drop,
    funcion_3_dividir,
    funcion_4_nombrar_partes,
    funcion_5_guardar_partes
)
import pandas as pd

def procesar_archivo(df, ruta_origen):
    headers = df.columns.tolist()

    if detectar_mojo(headers):
        es_mojo = preguntar_si_mojo()
        if es_mojo:
            opcion, cantidad = obtener_datos_division()
            if not opcion or not cantidad:
                messagebox.showwarning("Cancelado", "Proceso cancelado por el usuario.")
                return df  # Devuelve df original en caso de cancelación

            # 1. Ordenar y agregar columna DROP vacía
            df_actual = funcion_1_agregar_drop(df)

            # 2. Dividir en partes según la opción y cantidad
            partes = funcion_3_dividir(df_actual, opcion, cantidad)

            # 3. Asignar valores a la columna DROP en cada parte
            partes = funcion_4_nombrar_partes(partes)
            
            
            

            # 4. Unir todas las partes en un solo DataFrame
            df_final = pd.concat(partes, ignore_index=True)

            # 5. Guardar las partes en archivos separados
            funcion_5_guardar_partes(partes, ruta_origen)
            messagebox.showinfo("MOJO Completado", f"Trabajo MOJO procesado en {len(partes)} partes.")
            return df_final  # Devuelve el DataFrame final con DROP relleno
            
        else:
            messagebox.showinfo("No MOJO", "El archivo no será tratado como MOJO.")
            return df
    else:
        messagebox.showinfo("No MOJO Detectado", "No se detectaron columnas típicas de MOJO.")
        return df
