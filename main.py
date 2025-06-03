import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import os
import re
from address_parser import parse_address 
from historial import cargar_historial, guardar_en_historial, ARCHIVO_HISTORIAL
import json
from mojo import procesar_archivo

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


# Funcion para cargar y limpiar el archivo seleccionado
def cargar_y_limpiar():
    ruta = filedialog.askopenfilename(filetypes=[("Csv files or Excel", " *.csv *.xlsx")])
    if ruta: 
        limpiar_archivo(ruta)



# Limpiar headers automaticamente
def limpiar_headers(headers):
    original = list(headers)
    limpio = []
    for h in headers:
        
        h_limpio = h.strip().lower()  # quitar espacios y pasar a minúsculas
        h_limpio = re.sub(r'[\s\-]+', "_", h_limpio)  # reemplaza espacios y guiones por "_"
        h_limpio = re.sub(r"[^\w]", "", h_limpio)  # elimina todo lo que no sea letra, número o "_"
        limpio.append(h_limpio)
    return original, limpio



# Guardar CSV limpio
def guardar_csv(headers_finales=None):
    global df_actual, ruta_archivo
    if df_actual is None:
        messagebox.showerror("Error", "No hay archivo cargado para guardar.")
        return

    if headers_finales:
        df_actual.columns = headers_finales

    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    nueva_ruta = os.path.join(os.path.dirname(ruta_archivo), f"{nombre_base}_limpio.csv")

    df_actual.to_csv(nueva_ruta, index=False)
    etiqueta_resultado.config(text=f"¡Archivo limpio guardado como: {os.path.basename(nueva_ruta)}!")

def editar_headers(headers_actuales):

    if not headers_actuales:
        messagebox.showwarning("Sin headers", "No hay headers para editar.")
      
        return

    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Headers Manualmente")
    ventana_edicion.geometry("420x500")   

    # 🔹 Canvas con Scrollbar
    canvas = tk.Canvas(ventana_edicion)
    scrollbar = tk.Scrollbar(ventana_edicion, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # frame se desplaza
    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")
     
   
    

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    contenido_centrado = tk.Frame(scroll_frame)
    contenido_centrado.pack(anchor='center', expand=True)

    entradas = []

    # 🔹 Entradas dinámicas
    for i, header in enumerate(headers_actuales):
        tk.Label(contenido_centrado, text=f"Header {i + 1}:").pack(anchor="center")
        entrada = tk.Entry(contenido_centrado, width=40)
        entrada.insert(0, header)
        entrada.pack(pady=10)
        entradas.append(entrada)

    # 🔹 Botón fuera del scroll frame
    def aplicar_cambios():
      nuevos_headers = [e.get() for e in entradas]
      df_actual.columns = nuevos_headers  # ✅ Actualiza el DataFrame global
      guardar_csv(nuevos_headers)
      ventana_edicion.destroy()
 
    tk.Button(ventana_edicion, text="Aplicar Cambios", command=aplicar_cambios, bg=BOTON_COLOR, fg="WHITE").pack(pady=20)

   


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
        
        
        if 'DROP' not in df_actual.columns:
            df_actual['DROP'] = "" #Asegurarse de que la columna DROP exista
            df_actual = procesar_archivo(df_actual, ruta_archivo) 
        
        
        headers_actualizados = list(df_actual.columns)
        
        guardar_csv(headers_actualizados)

        guardar_en_historial(ruta_archivo)     

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

def mostrar_historial():
    rutas_historial = cargar_historial()
    if not rutas_historial:
        messagebox.showinfo("Historial", "No hay archivos recientes.")
        return

    ventana_historial = tk.Toplevel()
    ventana_historial.title("Historial Reciente")
    ventana_historial.geometry("800x800")
    ventana_historial.configure(bg=FONDO_COLOR)

    tk.Label(ventana_historial, text="Archivos limpiados recientemente:", font=FUENTE_TITULO, bg=FONDO_COLOR).pack(pady=15)

    lista = tk.Listbox(ventana_historial, font=FUENTE, width=70, height=10)
    lista.pack(pady=10)

    # Llenar el Listbox
    for ruta in rutas_historial:
        lista.insert(tk.END, ruta)

    def abrir_archivo_seleccionado():
        seleccion = lista.curselection()
        if seleccion:
            ruta = lista.get(seleccion[0])
            if os.path.exists(ruta):
                os.startfile(ruta)
            else:
                messagebox.showerror("Archivo no encontrado", f"No se encontró:\n{ruta}")
        else:
            messagebox.showwarning("Selecciona un archivo", "Debes seleccionar un archivo de la lista.")

    def eliminar_archivo():
        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showwarning("Ninguna selección", "Por favor, selecciona un archivo para eliminar.")
            return

        index = seleccion[0]
        archivo_seleccionado = lista.get(index)

        confirmar = messagebox.askyesno("Eliminar", f"¿Estás seguro de que quieres eliminar del historial:\n{archivo_seleccionado}?")
        if confirmar:
            with open(ARCHIVO_HISTORIAL, "r") as f:
                lineas = f.readlines()

            if 0 <= index < len(lineas):
                del lineas[index]
                with open(ARCHIVO_HISTORIAL, "w") as f:
                    f.writelines(lineas)

                lista.delete(index)  # Actualiza la lista sin recargar la ventana
                messagebox.showinfo("Eliminado", f"Archivo eliminado del historial:\n{archivo_seleccionado}")

    def borrar_todo():
        confirmar = messagebox.askyesno("Borrar todo", "¿Estás seguro de que quieres borrar todo el historial?")
        if confirmar:
            with open(ARCHIVO_HISTORIAL, "w") as f:
                json.dump([], f) #Borra todo el historial
                messagebox.showinfo("Historial borrado", "Todo el historial ha sido eliminado.")
            
            lista.delete(0, tk.END)  # Limpia el Listbox
            ventana_historial.destroy()
    

    # Botones
    botones = tk.Frame(ventana_historial, bg=FONDO_COLOR)
    botones.pack(pady=10)
    
    tk.Button(botones, text="📂 Abrir archivo", font=FUENTE, bg="#4CAF50", fg="white", command=abrir_archivo_seleccionado).pack(side="left", padx=5)
    tk.Button(botones, text="🗑️ Eliminar seleccionado", font=FUENTE, bg="#F44336", fg="white", command=eliminar_archivo).pack(side="left", padx=5)
    tk.Button(botones, text="🧹 Borrar todo", font=FUENTE, bg="red", fg="white", command=borrar_todo).pack(side="left", padx=5)


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

tk.Button(frame_contenido, text="🕘 Ver historial reciente", font=FUENTE, bg="#FF9800", fg="white", command=mostrar_historial).pack(pady=5, fill="x")
etiqueta_resultado = tk.Label(frame_contenido, text="", font=FUENTE, fg="green", bg=FONDO_COLOR, wraplength=400)
etiqueta_resultado.pack(pady=15)

ventana.mainloop()