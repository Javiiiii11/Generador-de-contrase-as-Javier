import tkinter as tk
from tkinter import ttk, filedialog
import random
import string
import os

def actualizar_etiquetas(*args):
    if longitud_personalizada.get():
        deslizadores_estado('disabled')
        etiqueta_min.config(text="Longitud Personalizada:")
        etiqueta_max.config(text=longitud_personalizada.get())
    else:
        deslizadores_estado('normal')
        etiqueta_min.config(text=f"Longitud Mínima: {slider_min.get()}")
        etiqueta_max.config(text=f"Longitud Máxima: {slider_max.get()}")

def deslizadores_estado(estado):
    scale_min.config(state=estado)
    scale_max.config(state=estado)

def generar_contrasena():
    contrasenas = []
    cantidad_contrasenas = int(cantidad.get())
    progress_bar['maximum'] = cantidad_contrasenas
    for i in range(cantidad_contrasenas):
        if longitud_personalizada.get():
            try:
                longitud = int(longitud_personalizada.get())
            except ValueError:
                resultado.set("Error: Longitud personalizada inválida.")
                return []
        else:
            longitud = random.randint(slider_min.get(), slider_max.get())

        opciones = {
            'numeros': var_numeros.get(),
            'mayusculas': var_mayusculas.get(),
            'minusculas': var_minusculas.get(),
            'caracteres': var_caracteres.get()
        }

        caracteres = ""
        if opciones['numeros']:
            caracteres += string.digits
        if opciones['mayusculas']:
            caracteres += string.ascii_uppercase
        if opciones['minusculas']:
            caracteres += string.ascii_lowercase
        if opciones['caracteres']:
            caracteres += string.punctuation

        if not caracteres:
            resultado.set("Error: Selecciona al menos un tipo de caracter.")
            return []

        contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
        contrasenas.append(contrasena)
        progress_bar['value'] = i + 1
        root.update_idletasks()

    return contrasenas

def guardar_contrasenas():
    progress_bar['value'] = 0
    contrasenas = generar_contrasena()
    if contrasenas:
        if var_ruta_personalizada.get():
            archivo = filedialog.asksaveasfilename(
                title="Guardar como", 
                filetypes=[("Archivo de texto", "*.txt")],
                defaultextension=".txt"
            )
        else:
            basepath = os.path.dirname(__file__)
            archivo = os.path.join(basepath, "password.txt")
            contador = 1
            while os.path.exists(archivo):
                archivo = os.path.join(basepath, f"password{contador}.txt")
                contador += 1

        if archivo:
            with open(archivo, 'w') as f:
                for contrasena in contrasenas:
                    f.write(contrasena + '\n')
            resultado.set("Contraseñas guardadas en: " + archivo)

    progress_bar['value'] = 0

def resetear():
    var_seleccionar_todos.set(False)
    var_numeros.set(False)
    var_mayusculas.set(False)
    var_minusculas.set(False)
    var_caracteres.set(False)
    var_ruta_personalizada.set(False)
    slider_min.set(7)
    slider_max.set(15)
    longitud_personalizada.set("")
    cantidad.set("1")
    resultado.set("")
    progress_bar['value'] = 0

def seleccionar_todos():
    estado = var_seleccionar_todos.get()
    var_numeros.set(estado)
    var_mayusculas.set(estado)
    var_minusculas.set(estado)
    var_caracteres.set(estado)

# Crear ventana principal
root = tk.Tk()
root.title("@javier - Generador de Contraseñas")
root.configure(bg="#2b2b2b")  # Fondo más oscuro

# Estilo general
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#2b2b2b')
style.configure('TLabel', background='#2b2b2b', foreground='#FFFFFF', font=('Helvetica', 11))
style.configure('TButton', background='#5bba6f', foreground='white', font=('Helvetica', 11), borderwidth=0)
style.map('TButton', background=[('active', '#58d68d')])  # Color cuando el botón es presionado
style.configure('TCheckbutton', background='#2b2b2b', foreground='white', font=('Helvetica', 11), selectcolor='#2b2b2b')
style.configure('Horizontal.TScale', background='#2b2b2b', troughcolor='#555555')

# Variables para las opciones
var_numeros = tk.BooleanVar()
var_mayusculas = tk.BooleanVar()
var_minusculas = tk.BooleanVar()
var_caracteres = tk.BooleanVar()
var_seleccionar_todos = tk.BooleanVar()
var_ruta_personalizada = tk.BooleanVar(value=False)
var_seleccionar_todos.trace('w', lambda *args: seleccionar_todos())
cantidad = tk.StringVar(value="1")
longitud_personalizada = tk.StringVar(value="")
longitud_personalizada.trace("w", actualizar_etiquetas)

# Configurar el rango de longitud
slider_min = tk.IntVar(value=7)
slider_max = tk.IntVar(value=15)
slider_min.trace("w", actualizar_etiquetas)
slider_max.trace("w", actualizar_etiquetas)

# Resultado
resultado = tk.StringVar()

# Widgets
frame = ttk.Frame(root, padding="20", style='TFrame')  # Margen aumentado para mejor visualización
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

etiqueta_min = ttk.Label(frame, text="Longitud Mínima:")
etiqueta_min.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
scale_min = ttk.Scale(frame, from_=4, to_=20, variable=slider_min, orient=tk.HORIZONTAL)
scale_min.grid(column=1, row=0, sticky=tk.EW, padx=10)

etiqueta_max = ttk.Label(frame, text="Longitud Máxima:")
etiqueta_max.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)
scale_max = ttk.Scale(frame, from_=4, to_=20, variable=slider_max, orient=tk.HORIZONTAL)
scale_max.grid(column=1, row=1, sticky=tk.EW, padx=10)

ttk.Label(frame, text="Longitud Personalizada:").grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)
ttk.Entry(frame, textvariable=longitud_personalizada, width=10).grid(column=1, row=2, sticky=tk.W, padx=10)

ttk.Label(frame, text="Cantidad de contraseñas:").grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)
ttk.Entry(frame, textvariable=cantidad, width=10).grid(column=1, row=3, sticky=tk.W, padx=10)

ttk.Checkbutton(frame, text="Seleccionar Todos", variable=var_seleccionar_todos).grid(column=0, row=4, sticky=tk.W, padx=10, pady=5)
ttk.Checkbutton(frame, text="Incluir Números", variable=var_numeros).grid(column=0, row=5, sticky=tk.W, padx=10)
ttk.Checkbutton(frame, text="Incluir Mayúsculas", variable=var_mayusculas).grid(column=0, row=6, sticky=tk.W, padx=10)
ttk.Checkbutton(frame, text="Incluir Minúsculas", variable=var_minusculas).grid(column=0, row=7, sticky=tk.W, padx=10)
ttk.Checkbutton(frame, text="Incluir Caracteres Especiales", variable=var_caracteres).grid(column=0, row=8, sticky=tk.W, padx=10)

ttk.Button(frame, text="Generar y Guardar Contraseñas", command=guardar_contrasenas).grid(column=0, row=9, columnspan=2, pady=20, padx=10)
ttk.Button(frame, text="Resetear", command=resetear).grid(column=0, row=10, columnspan=2, pady=10, padx=10)

ttk.Label(frame, text="Estado:").grid(column=0, row=11, sticky=tk.W, pady=(10,0), padx=10)
ttk.Entry(frame, textvariable=resultado, width=30, state='readonly').grid(column=1, row=11,sticky=tk.EW, padx=10, pady=(10,0))

ttk.Checkbutton(frame, text="Guardar en ruta personalizada", variable=var_ruta_personalizada).grid(column=0, row=12, sticky=tk.W, padx=10, pady=10, columnspan=2)

# Progress bar widget
progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate', length=300)
progress_bar.grid(column=0, row=13, columnspan=2, sticky=tk.EW, padx=10, pady=20)

# Configurar grid de frame
frame.columnconfigure(1, weight=1)  # Asegura que la columna 1 tome el espacio adicional
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
