import os
from tkinter import filedialog, messagebox, simpledialog
def preguntar_sobreescribir(ruta_archivo):
    if os.path.exists(ruta_archivo):
        respuesta = messagebox.askyesno("Confirmacion", f"Deseas sibreescribir {ruta_archivo}")
     

