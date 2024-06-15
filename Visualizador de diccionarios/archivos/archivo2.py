import tkinter as tk
from tkinter import filedialog, scrolledtext

def load_and_display_words():
    """Carga palabras desde un archivo de diccionario y las muestra en la interfaz."""
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filepath:
        result_label.config(text="No se seleccionó ningún archivo.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            words_text.delete('1.0', tk.END)  # Limpiar el cuadro de texto
            words_text.insert(tk.END, file.read())
        result_label.config(text=f"Archivo cargado: {os.path.basename(filepath)}")
    except Exception as e:
        result_label.config(text=f"Error al leer el archivo: {e}")

# Creación de la ventana principal de Tkinter
root = tk.Tk()
root.title("Visualizador de Diccionario")

# Dimensiones de la ventana
window_width = 600
window_height = 400

# Configurar colores de fondo de la ventana
root.configure(bg="#343d46")

# Ajustar la ventana
root.geometry(f'{window_width}x{window_height}')

# Botón para cargar el archivo del diccionario
load_button = tk.Button(root, text="Cargar Diccionario", command=load_and_display_words, bg="#4CAF50", fg="#FFFFFF", font="Helvetica 12 bold")
load_button.pack(pady=20)

# Cuadro de texto con barras de desplazamiento para mostrar palabras
words_text = scrolledtext.ScrolledText(root, font="Consolas 10", wrap=tk.WORD, width=70, height=20)
words_text.pack(pady=10)

# Etiqueta para mostrar el resultado
result_label = tk.Label(root, text="", bg="#343d46", fg="#FFFFFF", font="Helvetica 12 bold")
result_label.pack()

# Iniciar el loop principal de Tkinter
root.mainloop()
