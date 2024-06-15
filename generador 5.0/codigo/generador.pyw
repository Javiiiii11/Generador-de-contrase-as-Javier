import sys
import random
import string
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QSlider,
                             QLineEdit, QProgressBar, QFileDialog, QSpinBox, QMessageBox)
from PyQt5.QtCore import Qt

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Generador de Contraseñas')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Configuración de opciones de contraseña
        self.chk_numbers = QCheckBox('Incluir Números')
        self.chk_uppercase = QCheckBox('Incluir Mayúsculas')
        self.chk_lowercase = QCheckBox('Incluir Minúsculas')
        self.chk_special = QCheckBox('Incluir Caracteres Especiales')
        self.chk_custom_path = QCheckBox('Guardar en ruta personalizada')

        # Sliders para longitud de la contraseña
        self.slider_min = QSlider(Qt.Horizontal)
        self.slider_min.setMinimum(4)
        self.slider_min.setMaximum(20)
        self.slider_min.setValue(8)
        self.slider_min.valueChanged.connect(self.update_labels)

        self.slider_max = QSlider(Qt.Horizontal)
        self.slider_max.setMinimum(4)
        self.slider_max.setMaximum(20)
        self.slider_max.setValue(10)
        self.slider_max.valueChanged.connect(self.update_labels)

        self.label_min = QLabel('Longitud Mínima: 8')
        self.label_max = QLabel('Longitud Máxima: 10')

        # Entrada para cantidad de contraseñas
        self.spinbox_amount = QSpinBox()
        self.spinbox_amount.setMinimum(1)
        self.spinbox_amount.setMaximum(1100000)
        self.spinbox_amount.setValue(1)

        # Botones
        self.btn_generate = QPushButton('Generar y Guardar Contraseñas')
        self.btn_generate.clicked.connect(self.generate_and_save_passwords)
        self.btn_reset = QPushButton('Resetear')
        self.btn_reset.clicked.connect(self.reset)

        # Barra de progreso
        self.progress = QProgressBar()
        self.progress.setMaximum(100)

        # Layout organización
        layout.addWidget(self.chk_numbers)
        layout.addWidget(self.chk_uppercase)
        layout.addWidget(self.chk_lowercase)
        layout.addWidget(self.chk_special)
        layout.addWidget(self.label_min)
        layout.addWidget(self.slider_min)
        layout.addWidget(self.label_max)
        layout.addWidget(self.slider_max)
        layout.addWidget(QLabel('Cantidad de contraseñas:'))
        layout.addWidget(self.spinbox_amount)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.btn_reset)
        layout.addWidget(self.progress)
        layout.addWidget(self.chk_custom_path)

        self.setLayout(layout)

    def update_labels(self):
        self.label_min.setText(f'Longitud Mínima: {self.slider_min.value()}')
        self.label_max.setText(f'Longitud Máxima: {self.slider_max.value()}')

    def generate_and_save_passwords(self):
        num_passwords = self.spinbox_amount.value()
        min_length = self.slider_min.value()
        max_length = self.slider_max.value()

        password_list = []
        for _ in range(num_passwords):
            length = random.randint(min_length, max_length)
            characters = ''
            if self.chk_numbers.isChecked():
                characters += string.digits
            if self.chk_uppercase.isChecked():
                characters += string.ascii_uppercase
            if self.chk_lowercase.isChecked():
                characters += string.ascii_lowercase
            if self.chk_special.isChecked():
                characters += string.punctuation

            if characters:
                password = ''.join(random.choice(characters) for _ in range(length))
                password_list.append(password)

        if password_list:
            self.save_passwords(password_list)

    def save_passwords(self, passwords):
        if self.chk_custom_path.isChecked():
            path, _ = QFileDialog.getSaveFileName(self, "Guardar como", "", "Archivo de texto (*.txt)")
        else:
            path = os.path.join(os.getcwd(), 'passwords.txt')
            if os.path.exists(path):
                base, ext = os.path.splitext(path)
                counter = 1
                while os.path.exists(f"{base}{counter}{ext}"):
                    counter += 1
                path = f"{base}{counter}{ext}"

        if path:
            with open(path, 'w') as file:
                for pwd in passwords:
                    file.write(pwd + '\n')
            QMessageBox.information(self, "Guardado", f"Contraseñas guardadas en: {path}")

    def reset(self):
        self.chk_numbers.setChecked(False)
        self.chk_uppercase.setChecked(False)
        self.chk_lowercase.setChecked(False)
        self.chk_special.setChecked(False)
        self.slider_min.setValue(8)
        self.slider_max.setValue(10)
        self.spinbox_amount.setValue(1)
        self.progress.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec_())
