import tkinter as tk
from tkinter import ttk, filedialog
import random
import string
import os
from PIL import Image, ImageTk
def resource_path(relative_path):
    """Obtiene la ruta absoluta para acceder a los recursos, tanto en desarrollo como en el ejecutable."""
    try:
        # Si el programa es ejecutado por PyInstaller, el atributo _MEIPASS será establecido
        base_path = sys._MEIPASS
    except Exception:
        # De lo contrario, use el directorio donde se encuentra el script
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
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
    caracteres_similares = '0O1lI'
    caracteres_ambiguos = '{}[]()/\'"`~,;:.<>\\'

    for i in range(cantidad_contrasenas):
        if longitud_personalizada.get():
            try:
                longitud = int(longitud_personalizada.get())
            except ValueError:
                resultado.set("Error: Longitud personalizada inválida.")
                return []
        else:
            longitud = random.randint(slider_min.get(), slider_max.get())

        caracteres = ""
        if var_numeros.get():
            caracteres += string.digits
        if var_mayusculas.get():
            caracteres += string.ascii_uppercase
        if var_minusculas.get():
            caracteres += string.ascii_lowercase
        if var_caracteres.get():
            caracteres += string.punctuation

        if var_excluir_similares.get():
            caracteres = ''.join(c for c in caracteres if c not in caracteres_similares)
        if var_excluir_ambiguos.get():
            caracteres = ''.join(c for c in caracteres if c not in caracteres_ambiguos)

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
    # Resetear las variables y estados de los widgets como se requiera
    var_numeros.set(False)
    var_mayusculas.set(False)
    var_minusculas.set(False)
    var_caracteres.set(False)
    var_excluir_similares.set(False)
    var_excluir_ambiguos.set(False)

    slider_min.set(8)
    slider_max.set(12)
    longitud_personalizada.set("")
    cantidad.set("1")
    resultado.set("Estado inicializado.")
    progress_bar['value'] = 0
    actualizar_etiquetas()  # Actualiza las etiquetas según el estado inicial

def seleccionar_todos( ):
    estado = var_seleccionar_todos.get()
    var_numeros.set(estado)
    var_mayusculas.set(estado)
    var_minusculas.set(estado)
    var_caracteres.set(estado)
    var_excluir_similares.set(estado)
    var_excluir_ambiguos.set(estado)
def actualizar(boton:tk.BooleanVar):
    if boton.get() == False:
        var_seleccionar_todos.set(False)
    if var_caracteres.get() == True and var_excluir_ambiguos.get() == True and var_excluir_similares.get() == True and var_minusculas.get() == True and var_numeros.get()  == True and var_mayusculas.get() == True: 
        var_seleccionar_todos.set(True)
    return boton.get()
# Configura el estilo de la barra de progreso

# Crear ventana principal
root = tk.Tk()
root.title("@javier - Generador de Contraseñas")
root.configure(bg="#2b2b2b")
root.iconbitmap(resource_path('icono.ico'))

# Configurar la ventana para que no se pueda redimensionar
root.resizable(False, False)

#con esto desaparece la parte superior de la ventana
#root.overrideredirect(True)

# Estilo general
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#333344')
style.configure('TLabel', background='#333344', foreground='#CCCCCC', font=('Helvetica', 11))
style.configure('TButton', background='#6666FF', foreground='white', font=('Helvetica', 11), borderwidth=1, relief="flat", padding=6)
style.map('TButton', background=[('active', '#8888FF')])
style.configure("TProgressbar", background='#0910F0', troughcolor='#333344', bordercolor='#6666FF', lightcolor='#0910F0', darkcolor='#0910F0')
style.map("TProgressbar", background=[('active', '#0910F0'), ('disabled', '#cccccc')])


# Variables para las opciones
var_numeros = tk.BooleanVar()
var_mayusculas = tk.BooleanVar()
var_minusculas = tk.BooleanVar()
var_caracteres = tk.BooleanVar()
var_seleccionar_todos = tk.BooleanVar()
var_ruta_personalizada = tk.BooleanVar(value=False)
cantidad = tk.StringVar(value="1")
longitud_personalizada = tk.StringVar(value="")
longitud_personalizada.trace("w", actualizar_etiquetas)
var_excluir_similares = tk.BooleanVar(value=False)
var_excluir_ambiguos = tk.BooleanVar(value=False)


# Configurar el rango de longitud
slider_min = tk.IntVar(value=8)
slider_max = tk.IntVar(value=10)
slider_min.trace("w", actualizar_etiquetas)
slider_max.trace("w", actualizar_etiquetas)

# Resultado
resultado = tk.StringVar()

# Widgets
frame = ttk.Frame(root, padding="20", style='TFrame')
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

BarrasDemierda = ttk.Frame(frame, padding="20", style='TFrame')
BarrasDemierda.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
# Cargar y mostrar el logo
logo = tk.PhotoImage(file=resource_path('logo.png'))
logo_resized = logo.subsample(2, 2)
logo_label = ttk.Label(frame, image=logo_resized)
logo_label.grid(column=1, row=0, pady=20, padx=20, sticky='w')
# Agregar Checkbuttons usando tk en lugar de ttk
tk.Checkbutton(frame, text="Seleccionar Todos", variable=var_seleccionar_todos, onvalue=True, offvalue=False, command=seleccionar_todos, bg="#333344", fg="white", selectcolor="#6666FF", activebackground="#333344", activeforeground="white").grid(column=0, row=5, sticky=tk.W, padx=10)
check_excluir_similares = tk.Checkbutton(frame,command=lambda : actualizar(var_excluir_similares), text="Excluir caracteres similares = 0 O 1 l I", variable=var_excluir_similares, onvalue=True, offvalue=False, bg="#333344", fg="white", selectcolor="#6666FF", activebackground="#333344", activeforeground="white")
check_excluir_similares.grid(column=0, row=10, sticky=tk.W, padx=10, pady=0)
check_excluir_ambiguos = tk.Checkbutton(frame,command=lambda : actualizar(var_excluir_ambiguos), text="Excluir caracteres ambiguos = { } [ ] ( ) / \ '  ` ~ ; : . < >", variable=var_excluir_ambiguos, onvalue=True, offvalue=False, bg="#333344", fg="white", selectcolor="#6666FF", activebackground="#333344", activeforeground="white")
check_excluir_ambiguos.grid(column=0, row=11, sticky=tk.W, padx=10, pady=0) 
check_numeros = tk.Checkbutton(frame,command=lambda : actualizar(var_numeros), text="Incluir Números", variable=var_numeros,onvalue=True, offvalue=False, bg="#333344", fg="white", selectcolor="#6666FF", activebackground="#333344", activeforeground="white")
check_numeros.grid(column=0, row=6, sticky=tk.W, padx=10)
check_mayusculas = tk.Checkbutton(frame,command=lambda : actualizar(var_mayusculas), text="Incluir Mayúsculas", variable=var_mayusculas, onvalue=True, offvalue=False, bg="#333344", fg="white", selectcolor="#6666FF", activebackground="#333344", activeforeground="white")
check_mayusculas.grid(column=0, row=7, sticky=tk.W, padx=10)
check_minusculas = tk.Checkbutton(frame,command=lambda : actualizar(var_minusculas), text="Incluir Minúsculas", variable=var_minusculas, onvalue=True, offvalue=False, bg="#333344", fg="white", selectcolor="#6666FF", activebackground="#333344", activeforeground="white")
check_minusculas.grid(column=0, row=8, sticky=tk.W, padx=10)
check_caracteres = tk.Checkbutton(frame,command=lambda : actualizar(var_caracteres), text="Incluir Caracteres Especiales", variable=var_caracteres, onvalue=True, offvalue=False, bg="#333344", fg="white", selectcolor="#6666FF", activebackground="#333344", activeforeground="white")
check_caracteres.grid(column=0, row=9, sticky=tk.W, padx=10)


# Etiquetas y controles de longitud
etiqueta_min = ttk.Label(BarrasDemierda, text="Longitud Mínima: 8")
etiqueta_min.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)
scale_min = ttk.Scale(BarrasDemierda, from_=4, to_=20, variable=slider_min, orient=tk.HORIZONTAL)
scale_min.grid(column=2, row=1, sticky=tk.EW, padx=10)
etiqueta_max = ttk.Label(BarrasDemierda, text="Longitud Máxima: 10")
etiqueta_max.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)
scale_max = ttk.Scale(BarrasDemierda, from_=4, to_=20, variable=slider_max, orient=tk.HORIZONTAL)
scale_max.grid(column=2, row=2, sticky=tk.EW, padx=10)

ttk.Label(BarrasDemierda, text="Longitud Personalizada:").grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)
ttk.Entry(BarrasDemierda, textvariable=longitud_personalizada, width=30).grid(column=2, row=3, sticky=tk.W, padx=10)

# Control para la cantidad de contraseñas a generar
ttk.Label(BarrasDemierda, text="Cantidad de contraseñas:").grid(column=0, row=4, sticky=tk.W, padx=10, pady=10)
ttk.Entry(BarrasDemierda, textvariable=cantidad, width=30).grid(column=2, row=4, sticky=tk.W, padx=10)

# Botones para generar y resetear
ttk.Button(frame, text="Generar y Guardar Contraseñas", command=guardar_contrasenas).grid(column=1, row=12, columnspan=2, pady=20, padx=10)
ttk.Button(frame, text="Resetear", command=resetear).grid(column=1, row=13, columnspan=2, pady=10, padx=10)

# Etiqueta de estado y campo de entrada para mostrar mensajes
estado = ttk.Frame(frame, padding="20", style='TFrame')
estado.grid(column=0, row=12, sticky=tk.W, padx=10, pady=10)

ttk.Label(estado, text="Estado:").grid(column=0, row=12, sticky=tk.W, pady=(10,0), padx=10)
ttk.Entry(estado, textvariable=resultado, width=80, state='readonly').grid(column=2, row=12, sticky=tk.EW, padx=10, pady=(10,0))

# Checkbox para decidir si guardar en ruta personalizada
tk.Checkbutton(frame, text="Guardar en ruta personalizada", variable=var_ruta_personalizada, onvalue=True, offvalue=False, bg="#333344", fg="white", selectcolor="#6666FF", activebackground="#333344", activeforeground="white").grid(column=0, row=13, sticky=tk.W, padx=10, pady=10, columnspan=2)

# Barra de progreso
progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate', length=300)
progress_bar.grid(column=0, row=14, columnspan=2, sticky=tk.EW, padx=10, pady=20)

# Configuración final de la ventana
frame.columnconfigure(1, weight=1)  # Asegura que la columna 1 tome el espacio adicional
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()


#logo_image = ImageTk.PhotoImage(Image.open(resource_path('logo.png')).resize((150, 100), Image.ANTIALIAS)) en otras versiones