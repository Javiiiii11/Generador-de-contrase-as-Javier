import sys
import tkinter as tk
import random
import string
import os
import math
import threading
from PIL import Image, ImageTk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
        
        # Determinar la longitud de las contraseñas basado en los checkboxes
        use_uppercase = uppercase_var.get()
        use_lowercase = lowercase_var.get()
        use_numbers = numbers_var.get()
        use_specials = specials_var.get()

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
            result_label.config(text="Selecciona al menos un tipo de carácter.")
            return

        filename = "passwords.txt"
        file_counter = 1
        while os.path.exists(filename):
            filename = f"passwords{file_counter}.txt"
            file_counter += 1

        with open(filename, "w") as file:
            if random_length_var.get():
                lengths = [random.randint(7, 10) for _ in range(num_passwords)]
            elif random_length_var2.get():
                lengths = [random.randint(10, 20) for _ in range(num_passwords)]
            else:
                length = int(length_entry.get())
                lengths = [length for _ in range(num_passwords)]

            for length in lengths:
                password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_specials)
                file.write(password + "\n")

        file_size = os.path.getsize(filename)
        readable_size = convert_size(file_size)
        result_label.config(text=f"{num_passwords} contraseñas guardadas en '{filename}'\nTamaño del archivo: {readable_size}")
    except ValueError:
        result_label.config(text="Por favor, ingresa valores válidos.")

def save_passwords_thread():
    threading.Thread(target=save_passwords).start()

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def toggle_all():
    a_state = select_all_var.get()
    uppercase_var.set(a_state)
    lowercase_var.set(a_state)
    numbers_var.set(a_state)
    specials_var.set(a_state)

def update_select_all():
    if all([uppercase_var.get(), lowercase_var.get(), numbers_var.get(), specials_var.get()]):
        select_all_var.set(True)
    else:
        select_all_var.set(False)

def toggle_random_length():
    if random_length_var.get():
        # Desactivar el otro checkbox
        random_length_var2.set(False)

        # Deshabilitar la entrada para que el usuario no pueda editarla
        length_entry.config(state='normal')
        length_entry.delete(0, tk.END)
        length_entry.insert(0, "entre 7 y 10")
        length_entry.config(state='disabled')
    elif not random_length_var2.get():  # Si el otro checkbox también está desactivado
        length_entry.config(state='normal')
        length_entry.delete(0, tk.END)

def toggle_random_length2():
    if random_length_var2.get():
        # Desactivar el otro checkbox
        random_length_var.set(False)

        # Deshabilitar la entrada para que el usuario no pueda editarla
        length_entry.config(state='normal')
        length_entry.delete(0, tk.END)
        length_entry.insert(0, "entre 10 y 20")
        length_entry.config(state='disabled')
    elif not random_length_var.get():  # Si el otro checkbox también está desactivado
        length_entry.config(state='normal')
        length_entry.delete(0, tk.END)


root = tk.Tk()
root.title("@javier - Generador de Contraseñas")
root.configure(bg="#343d46")
window_width = 800
window_height = 550
root.geometry(f'{window_width}x{window_height}')
root.iconbitmap(resource_path('icono.ico'))

# Variables for checkboxes
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
specials_var = tk.BooleanVar()
select_all_var = tk.BooleanVar()  # Variable for the "Select All" checkbox
random_length_var = tk.BooleanVar()  # Variable for "Random Length" checkbox
random_length_var2 = tk.BooleanVar()  # Variable for "Random Length" checkbox

# Logo setup
try:
    original_image = Image.open(resource_path('logo.png'))
    resized_image = original_image.resize((150, 100), Image.ANTIALIAS)
    logo_image = ImageTk.PhotoImage(resized_image)
    logo_label = tk.Label(root, image=logo_image, bg="#343d46")
    logo_label.pack(pady=(10, 0))
except IOError:
    print("Error: El archivo 'logo.png' no se pudo encontrar o abrir.")

# Interface setup
text_color = "#FFFFFF"
button_color = "#4CAF50"
font_type = "Helvetica 12 bold"

# Frame a la derecha
otro_frame = tk.Frame(root, bg="#343d46")
otro_frame.pack(side='right', fill='y', padx=20)
tk.Checkbutton(otro_frame, text="Aleatorias entre 7 - 10", var=random_length_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=toggle_random_length, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(otro_frame, text="Aleatorias entre 10 - 20", var=random_length_var2, bg="#343d46", fg=text_color, selectcolor="#343d46", command=toggle_random_length2, font=font_type).pack(anchor=tk.W)

# Frame a la izquierda
checkbox_frame = tk.Frame(root, bg="#343d46")
checkbox_frame.pack(side='left', fill='both', expand=True, padx=20)
tk.Label(checkbox_frame, text="Número de contraseñas:", bg="#343d46", fg=text_color, font=font_type).pack()
number_entry = tk.Entry(checkbox_frame, font=font_type)
number_entry.pack(pady=5)
tk.Label(checkbox_frame, text="Longitud de la contraseña:", bg="#343d46", fg=text_color, font=font_type).pack()
length_entry = tk.Entry(checkbox_frame, font=font_type)
length_entry.pack(pady=5)

# Checkboxes
tk.Checkbutton(checkbox_frame, text="Seleccionar Todos", var=select_all_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=toggle_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir mayúsculas", var=uppercase_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir minúsculas", var=lowercase_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir números", var=numbers_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir caracteres especiales", var=specials_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)

# Botón de generar y etiqueta de resultado
boton_frame = tk.Frame(root, bg="#343d46")
boton_frame.pack(fill='x', pady=20)
generate_button = tk.Button(boton_frame, text="Generar y Guardar Contraseñas", command=save_passwords_thread, bg=button_color, fg=text_color, font=font_type)
generate_button.pack(side='left', padx=10)
result_label = tk.Label(boton_frame, text="", bg="#343d46", fg=text_color, font=font_type)
result_label.pack(side='left', padx=10)

root.mainloop()