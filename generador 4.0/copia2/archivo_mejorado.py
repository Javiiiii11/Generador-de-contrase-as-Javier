import sys
import tkinter as tk
import random
import string
import os
import math
import threading
from PIL import Image, ImageTk

def resource_path(relative_path):
    return os.path.join(os.path.abspath("."), relative_path)

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_specials):
    characters = "ñÑ"
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_specials:
        characters += string.punctuation
    if not characters:
        return None
    return ''.join(random.choice(characters) for i in range(length))

def save_passwords():
    try:
        num_passwords = int(number_entry.get())
        use_uppercase = uppercase_var.get()
        use_lowercase = lowercase_var.get()
        use_numbers = numbers_var.get()
        use_specials = specials_var.get()

        if not (use_uppercase or use_lowercase or use_numbers or use_specials):
            result_label.config(text="Selecciona al menos un tipo de carácter.")
            return

        filename = "passwords.txt"
        file_counter = 1
        while os.path.exists(filename):
            filename = f"passwords{file_counter}.txt"
            file_counter += 1

        with open(filename, "w") as file:
            for _ in range(num_passwords):
                if random_length_var.get():
                    length = random.randint(7, 10)
                elif random_length_var2.get():
                    length = random.randint(10, 20)
                elif random_length_var3.get():
                    length = random.randint(5, 10)
                elif random_length_var4.get():
                    length = random.randint(8, 12)
                elif random_length_var5.get():
                    length = random.randint(12, 16)
                else:
                    length = int(length_entry.get())
                password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_specials)
                file.write(password + "\n")

        file_size = os.path.getsize(filename)
        result_label.config(text=f"{num_passwords} contraseñas guardadas en '{filename}'")
    except ValueError:
        result_label.config(text="Por favor, ingresa valores válidos.")

def save_passwords_thread():
    """Ejecutar la generación de contraseñas en un hilo separado para evitar bloquear la GUI."""
    threading.Thread(target=save_passwords).start()

def convert_size(size_bytes):
    """Convertir el tamaño del archivo en un formato legible."""
    if size_bytes == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def toggle_all():
    """Activar o desactivar todas las opciones de caracteres al mismo tiempo."""
    a_state = select_all_var.get()
    uppercase_var.set(a_state)
    lowercase_var.set(a_state)
    numbers_var.set(a_state)
    specials_var.set(a_state)

def update_select_all():
    """Actualizar el estado del checkbox 'Seleccionar todos' basado en otros checkboxes."""
    if all([uppercase_var.get(), lowercase_var.get(), numbers_var.get(), specials_var.get()]):
        select_all_var.set(True)
    else:
        select_all_var.set(False)
def random_length():
    if random_length_var.get():
        return random.randint(5, 10)
    elif random_length_var2.get():
        return random.randint(7, 10)
    elif random_length_var3.get():
        return random.randint(8, 12)
    elif random_length_var4.get():
        return random.randint(10, 20)
    elif random_length_var5.get():
        return random.randint(12, 16)
    return 10  # Default length if nothing is set

def toggle_random_length(selected_var, other_vars):
    """Activar una opción y desactivar todas las demás opciones de longitud aleatoria."""
    if selected_var.get():
        # Desactivar todas las otras opciones de longitud aleatoria
        for var in other_vars:
            var.set(False)
        length_entry.config(state='normal')
        if selected_var == random_length_var:
            random_length_var.set(False)
            length_entry.delete(0, tk.END)
            length_entry.insert(0, "entre 5 y 10")
            length_entry.config(state='disabled')
        elif selected_var == random_length_var2:
            random_length_var.set(False)
            length_entry.delete(0, tk.END)
            length_entry.insert(0, "entre 7 y 10")
            length_entry.config(state='disabled')
        elif selected_var == random_length_var3:
            random_length_var.set(False)
            length_entry.delete(0, tk.END)
            length_entry.insert(0, "entre 8 y 12")
            length_entry.config(state='disabled')
        elif selected_var == random_length_var4:
            length_entry.delete(0, tk.END)
            random_length_var.set(False)
            length_entry.insert(0, "entre 10 y 20")
            length_entry.config(state='disabled')
        elif selected_var == random_length_var5:
            length_entry.delete(0, tk.END)
            random_length_var.set(False)
            length_entry.insert(0, "entre 12 y 16")
        length_entry.config(state='disabled')
    else:
        length_entry.config(state='normal')
        length_entry.delete(0, tk.END)

# Configuración inicial de la GUI
root = tk.Tk()
root.title("@javier - Generador de Contraseñas")
root.configure(bg="#343d46")
window_width = 1000
window_height = 450
root.geometry(f'{window_width}x{window_height}')
root.iconbitmap(resource_path('icono.ico'))

# Crear frames para organizar la interfaz
left_frame = tk.Frame(root, bg="#343d46")
center_frame = tk.Frame(root, bg="#343d46")
right_frame = tk.Frame(root, bg="#343d46")
right_frame.pack(side='right', fill='y', padx=20, pady=120)
left_frame.pack(side='right', fill='y', padx=20, pady=130)
center_frame.pack(side="left", fill='both', expand=True, padx=20, pady=20)



# Variables for checkboxes
select_all_var = tk.BooleanVar()
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
specials_var = tk.BooleanVar()
random_length_var = tk.BooleanVar()  # 5 - 10
random_length_var2 = tk.BooleanVar()  # 7 - 10
random_length_var3 = tk.BooleanVar()  # 8 - 12
random_length_var4 = tk.BooleanVar()  # 10 - 20
random_length_var5 = tk.BooleanVar()  # 12 - 16

# Interface setup
text_color = "#FFFFFF"
button_color = "#4CAF50"
font_type = "Helvetica 12 bold"


# Checkbox frame
checkbox_frame = tk.Frame(root, bg="#343d46")
checkbox_frame.pack(fill='both', expand=True, padx=20, pady=10)

# Additional checkboxes for new random length options
random_frame = tk.Frame(right_frame, bg="#343d46")
random_frame.pack(side='right', fill='y', padx=20, pady=20)
random_vars = [random_length_var, random_length_var2, random_length_var3, random_length_var4, random_length_var5]
random_texts = ["entre 5 y 10", "entre 7 y 10", "entre 8 y 12","entre 10 y 20", "entre 12 y 16"]
for var, text in zip(random_vars, random_texts):
    tk.Checkbutton(random_frame, text=f"Aleatorias {text}", var=var, bg="#343d46", fg=text_color, selectcolor="#343d46", 
                   command=lambda var=var: toggle_random_length(var, random_vars), font=font_type).pack(anchor=tk.W)

# Logo setup
try:
    logo_image = ImageTk.PhotoImage(Image.open(resource_path('logo.png')).resize((150, 100), Image.ANTIALIAS))
    logo_label = tk.Label(center_frame, image=logo_image, bg="#343d46")
    logo_label.pack(pady=(10, 0))
except IOError:
    print("Error: El archivo 'logo.png' no se pudo encontrar o abrir.")
tk.Label(center_frame, text="Número de contraseñas:", bg="#343d46", fg=text_color, font=font_type).pack()
number_entry = tk.Entry(center_frame, font=font_type)
number_entry.pack(pady=5)
tk.Label(center_frame, text="Longitud de la contraseña:", bg="#343d46", fg=text_color, font=font_type).pack()
length_entry = tk.Entry(center_frame, font=font_type)
length_entry.pack(pady=5)


# Frame for checkboxes
checkbox_frame = tk.Frame(left_frame, bg="#343d46")
checkbox_frame.pack(fill='both', expand=True, padx=20, pady=10)



# Input fields and checkboxes

tk.Checkbutton(checkbox_frame, text="Seleccionar Todos", var=select_all_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=toggle_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir mayúsculas", var=uppercase_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir minúsculas", var=lowercase_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir números", var=numbers_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir caracteres especiales", var=specials_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)

# Button for generating and result label
boton_frame = tk.Frame(center_frame, bg="#343d46")
boton_frame.pack(fill='x', pady=20, side="bottom")
generate_button = tk.Button(boton_frame, text="Generar y Guardar Contraseñas", command=save_passwords_thread, bg=button_color, fg=text_color, font=font_type)
generate_button.pack(pady=(0, 10))  # Padding vertical para espacio entre botón y etiqueta de resultado
result_label = tk.Label(boton_frame, text="", bg="#343d46", fg=text_color, font=font_type)
result_label.pack()  # Empaquetado por defecto sin especificar lado para que aparezca debajo del botón


root.mainloop()
