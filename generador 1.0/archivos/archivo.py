import tkinter as tk
import random
import string
import os

def generate_password(length):
    """Genera una contraseña aleatoria con la longitud especificada."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def convert_size(size_bytes):
    """Convierte un tamaño en bytes a un formato legible (KB, MB, GB)."""
    if size_bytes == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def save_passwords():
    """Genera contraseñas y las guarda en un archivo, asegurándose de no sobrescribir un archivo existente."""
    try:
        num_passwords = int(number_entry.get())
        length = int(length_entry.get())
        passwords = [generate_password(length) for i in range(num_passwords)]

        # Verificar si el archivo existe y crear un nuevo nombre de archivo si es necesario
        filename = "passwords.txt"
        file_counter = 1
        while os.path.exists(filename):
            filename = f"passwords{file_counter}.txt"
            file_counter += 1

        with open(filename, "w") as file:
            for password in passwords:
                file.write(password + "\n")

        # Obtener el tamaño del archivo y convertirlo a un formato legible
        file_size = os.path.getsize(filename)
        readable_size = convert_size(file_size)

        result_label.config(text=f"{num_passwords} contraseñas guardadas en '{filename}'\nTamaño del archivo: {readable_size}")
    except ValueError:
        result_label.config(text="Por favor, ingresa valores válidos.")

import math  # Importar math para cálculos en convert_size

# Creación de la ventana principal de Tkinter
root = tk.Tk()
root.title("@javier - Generador de Contraseñas")

# Dimensiones de la ventana
window_width = 400
window_height = 200

# Colores y fuentes
background_color = "#343d46"
text_color = "#FFFFFF"
button_color = "#4CAF50"
font_type = "Helvetica 12 bold"

# Configurar colores de fondo de la ventana
root.configure(bg=background_color)

# Obtener las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular la posición x e y para centrar la ventana
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Establecer el tamaño inicial de la ventana y centrarlo
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Entrada para número de contraseñas
tk.Label(root, text="Número de contraseñas:", bg=background_color, fg=text_color, font=font_type).pack()
number_entry = tk.Entry(root, font=font_type)
number_entry.pack(pady=5)

# Entrada para longitud de la contraseña
tk.Label(root, text="Longitud de la contraseña:", bg=background_color, fg=text_color, font=font_type).pack()
length_entry = tk.Entry(root, font=font_type)
length_entry.pack(pady=5)

# Botón para generar y guardar contraseñas
generate_button = tk.Button(root, text="Generar y Guardar Contraseñas", command=save_passwords, bg=button_color, fg=text_color, font=font_type)
generate_button.pack(pady=10)

# Etiqueta para mostrar el resultado y el tamaño del archivo
result_label = tk.Label(root, text="", bg=background_color, fg=text_color, font=font_type)
result_label.pack()

# Iniciar el loop principal de Tkinter
root.mainloop()
