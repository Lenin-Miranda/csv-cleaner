import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import os
import re
from address_parser import parse_address 

# Estilos globales
FONDO_COLOR = "#f2f2f2"
BOTON_COLOR = "#4CAF50"
TEXTO_COLOR = "#333"
FUENTE = ("Segoe UI", 11)
FUENTE_TITULO = ("Segoe UI", 16, "bold")

# Variables globales
headers_original = []
headers_limpios = []

df_actual = None
ruta_archivo = ""




# Limpiar headers automaticamente
def limpiar_headers(headers):
    original = list(headers)
    limpio = []
    for h in headers:
        h_limpio = h.strip()  # quitar espacios y pasar a minúsculas
        h_limpio = re.sub(r'[\s\-]+', "_", h_limpio)  # reemplaza espacios y guiones por "_"
        h_limpio = re.sub(r"[^\w]", "", h_limpio)  # elimina todo lo que no sea letra, número o "_"
        limpio.append(h_limpio)
    return original, limpio


# Guardar CSV limpio
def guardar_csv(headers_finales):
    global df_actual, ruta_archivo
    df_actual.columns = headers_finales

    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    nueva_ruta = os.path.join(os.path.dirname(ruta_archivo),f"{nombre_base}_limpio.csv")

    df_actual.to_csv(nueva_ruta, index=False)
    etiqueta_resultado.config(text=f"!Archivo limpio guardado como: {os.path.basename(nueva_ruta)}!")


#Ventana editable para headers
def editar_headers(headers_actuales):
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Headers Manualmente")
    ventana_edicion.geometry("420x500")

    # 🔹 Canvas con Scrollbar
    canvas = tk.Canvas(ventana_edicion)
    scrollbar = tk.Scrollbar(ventana_edicion, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    entradas = []

    # 🔹 Entradas dinámicas
    for i, header in enumerate(headers_actuales):
        tk.Label(scroll_frame, text=f"Header {i + 1}:").pack()
        entrada = tk.Entry(scroll_frame)
        entrada.insert(0, header)
        entrada.pack(pady=2)
        entradas.append(entrada)

    # 🔹 Botón fuera del scroll frame
    def aplicar_cambios():
        nuevos_headers = [e.get() for e in entradas]
        guardar_csv(nuevos_headers)
        ventana_edicion.destroy()

    boton_aplicar = tk.Button(scroll_frame, text="Aplicar Cambios", command=aplicar_cambios)
    boton_aplicar.pack(pady=10)



def elegir_columna_direccion(opciones):
    """
    Muestra un diálogo para que el usuario elija una columna de dirección.
    """
    mensaje = "Selecciona la columna que contiene las direcciones:\n"
    mensaje += "Si no quieres separar direcciones, escribe '0' o Cancelar. \n\n"
    mensaje += "\n".join(f"{i+1}. {col}" for i, col in enumerate(opciones))
    mensaje += "\n\nEscribe el número de la opción:"
    
    seleccion = simpledialog.askstring("Seleccionar columna", mensaje)
    
    try:
        indice = int(seleccion) - 1
        if 0 <= indice < len(opciones):
            return opciones[indice]
    except:
        pass  # si el usuario cancela o escribe mal, retornamos None

    return None

#Limpieza principal
def limpiar_archivo(ruta):
    global headers_original, headers_limpios, df_actual, ruta_archivo
    try:
        ruta_archivo = ruta
        ext = os.path.splitext(ruta)[1].lower()
        if ext == ".xlsx":
            df_actual = pd.read_excel(ruta, dtype=str)
        else:
            df_actual = pd.read_csv(ruta, dtype=str)

        

        # Si tiene solo 1 columna y parece no separado:
        if df_actual.shape[1] == 1:
            df_actual = df_actual[df_actual.columns[0]].str.split(',', expand=True)

        # limpiar headers
        headers_original, headers_limpios = limpiar_headers(df_actual.columns)
        df_actual.columns = headers_limpios

        # Separar direcciones si columna existe
    
        posibles = [col for col in df_actual.columns if "address" in col.lower()]
        if len(posibles) > 1:
            columna = elegir_columna_direccion(posibles)  # Función que muestra opciones
        elif len(posibles) == 1:
            columna = posibles[0]
        else:
            columna = None

        if columna:
            df_actual = separar_direcciones(df_actual, columna=columna)


        # ¡ACTUALIZAR lista de headers tras agregar columnas!
        headers_actualizados = list(df_actual.columns)

        guardar_csv(headers_actualizados)

    except Exception as e:
        etiqueta_resultado.config(text=f"Error: {str(e)}")

    

    
# Mostrar cambios en headers
def mostrar_cambios():
    if not headers_original:
        messagebox.showinfo("Sin datos", "Primero debes limpiar un archivo.")
        return
    cambios = "CAMBIOS EN LOS HEADERS:\n\n"
    for o, n in zip(headers_original, headers_limpios):
        cambios += f"{o} → {n}\n"
    messagebox.showinfo("Cambios realizados", cambios)



def cargar_y_limpiar():
    ruta = filedialog.askopenfilename(filetypes=[("Csv files or Excel", " *.csv *.xlsx")])
    if ruta: 
        limpiar_archivo(ruta)



def separar_direcciones(df, columna='mailingaddress'):
    
    def seguro_parsear(valor):
        try:
            partes = parse_address(str(valor))
            if isinstance(partes, (list, tuple)) and len(partes) == 4:
                return partes
            else:
                print(f"¡Error de longitud! Valor parseado: {partes} para input: {valor}")
                return ["", "", "", ""]
        except Exception as e:
            print(f"Excepción parseando '{valor}': {e}")
            return ["", "", "", ""]

    nuevas_columnas = df[columna].apply(seguro_parsear)
    
    print("Ejemplos de resultados parseados:")
    for i, val in enumerate(nuevas_columnas.head(10)):
        print(f"{i}: {val} (len={len(val)})")

    # Aquí chequeamos si alguna fila no tiene exactamente 4 elementos:
    for i, val in enumerate(nuevas_columnas):
        if not isinstance(val, (list, tuple)) or len(val) != 4:
            raise ValueError(f"Fila {i} con longitud incorrecta: {val}")

    # Evitar sobrescribir columnas existentes
    for col in ['address', 'city', 'state', 'zip']:
        if col in df.columns:
            df = df.drop(columns=[col])


    nuevas_df = pd.DataFrame(nuevas_columnas.tolist(), index=df.index)
    print("Shape del nuevo dataframe de direcciones:", nuevas_df.shape)
    print(nuevas_df.head())
    
    if nuevas_df.shape[1] == 4:
        nuevas_df.columns = ['address', 'city', 'state', 'zip']
        df = pd.concat([df.drop(columns=[col for col in ['address', 'city', 'state', 'zip'] if col in df.columns]), nuevas_df], axis=1)
    else:
        raise ValueError(f"Error: el parser devolvió {nuevas_df.shape[1]} columnas en vez de 4.")

    return df




#Crear ventana principal

ventana = tk.Tk()
ventana.title("🧹 Limpiador de Datos CSV/XLSX")
ventana.geometry("500x350")
ventana.configure(bg=FONDO_COLOR)

frame_contenido = tk.Frame(ventana, bg=FONDO_COLOR)
frame_contenido.pack(pady=20, padx=20)

tk.Label(frame_contenido, text="Limpiador de Datos", font=FUENTE_TITULO, fg=TEXTO_COLOR, bg=FONDO_COLOR).pack(pady=(0, 10))

tk.Button(frame_contenido, text="📂 Seleccionar archivo CSV/XLSX", font=FUENTE, bg=BOTON_COLOR, fg="white", command=cargar_y_limpiar).pack(pady=10, fill="x")

tk.Button(frame_contenido, text="🔍 Mostrar cambios en encabezados", font=FUENTE, bg=BOTON_COLOR, fg="white", command=mostrar_cambios).pack(pady=5, fill="x")

tk.Button(frame_contenido, text="✏️ Editar headers manualmente", font=FUENTE, bg="#2196F3", fg="white", command=lambda: editar_headers(headers_limpios)).pack(pady=5, fill="x")

etiqueta_resultado = tk.Label(frame_contenido, text="", font=FUENTE, fg="green", bg=FONDO_COLOR, wraplength=400)
etiqueta_resultado.pack(pady=15)

ventana.mainloop()