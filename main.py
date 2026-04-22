import sys
import os
import time
import ctypes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QCheckBox, QLineEdit, QPushButton, QGridLayout, 
                             QMessageBox, QDialog)
from PyQt6.QtGui import QIntValidator, QPixmap, QAction, QColor, QPalette
from PyQt6.QtCore import Qt

class DropArea(QLabel):
    def __init__(self):
        super().__init__("Arrastra imágenes\nmáximo 10\n.bmp")
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setStyleSheet("background-color: #2b2b2b; color: white; padding: 10px; border: 1px solid #555;")
        self.setAcceptDrops(True)
        self.setMinimumSize(300, 200)
        self.image_paths = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            path = url.toLocalFile()
            if path.lower().endswith(".bmp"):
                if path not in self.image_paths:
                    if len(self.image_paths) < 10:
                        self.image_paths.append(path)
                    else:
                        QMessageBox.warning(self, "Límite alcanzado", "No puedes subir más de 10 imágenes.")
                        break
        
        self.update_display()

    def update_display(self):
        if not self.image_paths:
            self.setText("Arrastra imágenes\nmáximo 10\n.bmp")
        else:
            text = "Archivos cargados:\n"
            for p in self.image_paths:
                text += f"- {os.path.basename(p)}\n"
            self.setText(text)

class OddIntValidator(QIntValidator):
    def validate(self, input_str, pos):
        # Allow empty or partial
        if not input_str:
            return QIntValidator.State.Intermediate, input_str, pos
        try:
            val = int(input_str)
            if val > 0 and val % 2 != 0:
                return QIntValidator.State.Acceptable, input_str, pos
            else:
                return QIntValidator.State.Invalid, input_str, pos
        except ValueError:
            return QIntValidator.State.Invalid, input_str, pos

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #323232; color: white;")
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(
            "TC3003\n"
            "Tecnológico de Monterrey\n"
            "Campus Puebla\n"
            "Mayo 2026\n\n"
            "Equipo:\n"
            "1- Emmanuel Torres Rios\n"
            "2- Daniel Flores Rojas\n"
            "3-"
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        info_label.setStyleSheet("padding: 20px;")
        layout.addWidget(info_label)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap("./img/tec_logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        layout.addWidget(logo_label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procesamiento de imágenes")
        self.setFixedSize(700, 500)
        self.setStyleSheet("background-color: #323232; color: #E0E0E0;")
        
        # Determine the shared library extension
        lib_ext = '.dylib' if sys.platform == 'darwin' else '.so'
        self.lib = ctypes.CDLL(f"./libprocesamiento{lib_ext}")
        
        # Setup C signatures
        self.lib.inv_img.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.inv_img_color.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.inv_img_grey_horizontal.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.inv_img_color_horizontal.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.desenfoque.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        self.lib.desenfoque_grey.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        
        self.init_ui()
        self.init_menu()

    def init_menu(self):
        menubar = self.menuBar()
        # macOS specific fixes for menubar colors in dark mode is native, but we can set it explicitly
        menubar.setStyleSheet("background-color: #2b2b2b; color: white;")
        
        acerca_action = QAction("Acerca de", self)
        acerca_action.triggered.connect(self.show_about)
        
        help_menu = menubar.addMenu("Menu")
        help_menu.addAction(acerca_action)

    def show_about(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left side
        left_layout = QVBoxLayout()
        
        self.drop_area = DropArea()
        left_layout.addWidget(self.drop_area)
        
        tiempo_label = QLabel("Tiempo de ejecución")
        self.tiempo_entry = QLineEdit()
        self.tiempo_entry.setReadOnly(True)
        self.tiempo_entry.setStyleSheet("background-color: #2b2b2b; color: white; border: none;")
        
        ruta_label = QLabel("Ruta de archivos")
        self.ruta_entry = QLineEdit()
        self.ruta_entry.setReadOnly(True)
        self.ruta_entry.setStyleSheet("background-color: #2b2b2b; color: white; border: none;")
        
        left_layout.addSpacing(20)
        left_layout.addWidget(tiempo_label)
        left_layout.addWidget(self.tiempo_entry)
        left_layout.addWidget(ruta_label)
        left_layout.addWidget(self.ruta_entry)
        left_layout.addStretch()
        
        # Right side
        right_layout = QVBoxLayout()
        right_layout.addSpacing(20)
        
        self.cb1 = QCheckBox("1- Vertical escala de grises")
        self.cb2 = QCheckBox("2- Vertical escala a colores")
        self.cb3 = QCheckBox("3- Horizontal escala de grises")
        self.cb4 = QCheckBox("4- Horizontal escala a colores")
        self.cb5 = QCheckBox("5- Desenfoque escala de grises")
        self.cb6 = QCheckBox("6- Desenfoque escala a colores")
        
        self.checkboxes = [self.cb1, self.cb2, self.cb3, self.cb4, self.cb5, self.cb6]
        for cb in self.checkboxes:
            right_layout.addWidget(cb)
            
        # Add Kernels using a grid layout to position them next to cb5/cb6
        # Actually it's easier to put them in QHBoxLayouts
        
        kernel1_layout = QHBoxLayout()
        kernel1_layout.addWidget(QLabel("     ")) # Indent
        self.kernel1_entry = QLineEdit()
        self.kernel1_entry.setFixedWidth(50)
        self.kernel1_entry.setValidator(OddIntValidator())
        kernel1_layout.addWidget(self.kernel1_entry)
        kernel1_layout.addWidget(QLabel("Kernel"))
        kernel1_layout.addStretch()
        
        right_layout.insertLayout(right_layout.indexOf(self.cb5) + 1, kernel1_layout)
        
        kernel2_layout = QHBoxLayout()
        kernel2_layout.addWidget(QLabel("     ")) # Indent
        self.kernel2_entry = QLineEdit()
        self.kernel2_entry.setFixedWidth(50)
        self.kernel2_entry.setValidator(OddIntValidator())
        kernel2_layout.addWidget(self.kernel2_entry)
        kernel2_layout.addWidget(QLabel("Kernel"))
        kernel2_layout.addStretch()
        
        right_layout.insertLayout(right_layout.indexOf(self.cb6) + 1, kernel2_layout)
        
        right_layout.addSpacing(20)
        
        todas_layout = QHBoxLayout()
        self.btn_todas = QPushButton("Todas")
        self.btn_todas.clicked.connect(self.select_all)
        self.btn_todas.setStyleSheet("background-color: #555; border-radius: 5px; padding: 5px 20px;")
        todas_layout.addWidget(self.btn_todas)
        todas_layout.addWidget(QLabel("Se seleccionan todas las\ntransformaciones de imágenes"))
        todas_layout.addStretch()
        right_layout.addLayout(todas_layout)
        
        right_layout.addSpacing(30)
        
        self.btn_ejecutar = QPushButton("Ejecutar")
        self.btn_ejecutar.clicked.connect(self.ejecutar)
        self.btn_ejecutar.setStyleSheet("background-color: #555; border-radius: 5px; padding: 5px 30px;")
        
        ejecutar_layout = QHBoxLayout()
        ejecutar_layout.addWidget(self.btn_ejecutar)
        ejecutar_layout.addStretch()
        
        right_layout.addLayout(ejecutar_layout)
        right_layout.addStretch()
        
        # Logo bottom right
        logo_layout = QHBoxLayout()
        logo_layout.addStretch()
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("./img/tec_logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(logo_pixmap)
            # Add a white background to the standard blue label if it lacks one?
            self.logo_label.setStyleSheet("background-color: white; padding: 5px; border-radius: 5px;")
        logo_layout.addWidget(self.logo_label)
        
        right_layout.addLayout(logo_layout)
        
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addSpacing(30)
        main_layout.addLayout(right_layout, stretch=2)

    def select_all(self):
        all_checked = all(cb.isChecked() for cb in self.checkboxes)
        for cb in self.checkboxes:
            cb.setChecked(not all_checked)

    def ejecutar(self):
        if not self.drop_area.image_paths:
            QMessageBox.warning(self, "Advertencia", "No hay imágenes para procesar.")
            return
            
        any_selected = any(cb.isChecked() for cb in self.checkboxes)
        if not any_selected:
            QMessageBox.warning(self, "Advertencia", "Selecciona al menos una transformación.")
            return
            
        if self.cb5.isChecked() and not self.kernel1_entry.text():
            QMessageBox.warning(self, "Advertencia", "Ingresa un kernel válido para el desenfoque en grises.")
            return
            
        if self.cb6.isChecked() and not self.kernel2_entry.text():
            QMessageBox.warning(self, "Advertencia", "Ingresa un kernel válido para el desenfoque a color.")
            return
            
        # Make sure output directory exists
        if not os.path.exists("./img"):
            os.makedirs("./img")

        start_time = time.time()
        
        for path in self.drop_area.image_paths:
            base_filename = os.path.basename(path)
            name_without_ext = os.path.splitext(base_filename)[0]
            
            c_path = path.encode('utf-8')
            
            if self.cb1.isChecked():
                mask = f"{name_without_ext}_vg".encode('utf-8')
                self.lib.inv_img(mask, c_path)
            
            if self.cb2.isChecked():
                mask = f"{name_without_ext}_vc".encode('utf-8')
                self.lib.inv_img_color(mask, c_path)
                
            if self.cb3.isChecked():
                mask = f"{name_without_ext}_hg".encode('utf-8')
                self.lib.inv_img_grey_horizontal(mask, c_path)
                
            if self.cb4.isChecked():
                mask = f"{name_without_ext}_hc".encode('utf-8')
                self.lib.inv_img_color_horizontal(mask, c_path)
                
            if self.cb5.isChecked():
                mask = f"{name_without_ext}_dg".encode('utf-8')
                kernel_size = int(self.kernel1_entry.text())
                self.lib.desenfoque_grey(c_path, mask, kernel_size)
                
            if self.cb6.isChecked():
                mask = f"{name_without_ext}_dc".encode('utf-8')
                kernel_size = int(self.kernel2_entry.text())
                self.lib.desenfoque(c_path, mask, kernel_size)
                
        end_time = time.time()
        elapsed = end_time - start_time
        
        self.tiempo_entry.setText(f"{elapsed:.4f} segundos")
        self.ruta_entry.setText(os.path.abspath("./img/"))
        
        # Clear paths
        self.drop_area.image_paths.clear()
        self.drop_area.update_display()
        QMessageBox.information(self, "Procesamiento Terminado", f"Las imágenes se han guardado en ./img/\nTiempo: {elapsed:.4f} seg")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Force dark theme style slightly
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(50, 50, 50))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(85, 85, 85))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
