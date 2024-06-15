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
        random_length = random_length_var.get()
        
        if random_length:
            lengths = [random.randint(7, 10) for _ in range(num_passwords)]
        else:
            length = int(length_entry.get())
        
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
            for i in range(num_passwords):
                if random_length:
                    length = lengths[i]
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
        length_entry.config(state='disabled')
    else:
        length_entry.config(state='normal')

root = tk.Tk()
root.title("@javier - Generador de Contraseñas")
root.configure(bg="#343d46")
window_width = 400
window_height = 500
root.geometry(f'{window_width}x{window_height}')
root.iconbitmap(resource_path('icono.ico'))

# Variables for checkboxes
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
specials_var = tk.BooleanVar()
select_all_var = tk.BooleanVar()  # Variable for the "Select All" checkbox
random_length_var = tk.BooleanVar()  # Variable for "Random Length" checkbox

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
tk.Label(root, text="Número de contraseñas:", bg="#343d46", fg=text_color, font=font_type).pack()
number_entry = tk.Entry(root, font=font_type)
number_entry.pack(pady=5)
tk.Label(root, text="Longitud de la contraseña:", bg="#343d46", fg=text_color, font=font_type).pack()
length_entry = tk.Entry(root, font=font_type)
length_entry.pack(pady=5)

# Checkboxes
checkbox_frame = tk.Frame(root, bg="#343d46")
checkbox_frame.pack(fill=tk.X, padx=20)
tk.Checkbutton(checkbox_frame, text="Seleccionar Todos", var=select_all_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=toggle_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir mayúsculas", var=uppercase_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir minúsculas", var=lowercase_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir números", var=numbers_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Incluir caracteres especiales", var=specials_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=update_select_all, font=font_type).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Aleatorias entre 7 - 10", var=random_length_var, bg="#343d46", fg=text_color, selectcolor="#343d46", command=toggle_random_length, font=font_type).pack(anchor=tk.W)

# Generate button and result label
generate_button = tk.Button(root, text="Generar y Guardar Contraseñas", command=save_passwords_thread, bg=button_color, fg=text_color, font=font_type)
generate_button.pack(pady=10)
result_label = tk.Label(root, text="", bg="#343d46", fg=text_color, font=font_type)
result_label.pack()

root.mainloop()
