import sys
import sqlite3
import pandas as pd
import socket
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QMessageBox, QScrollArea, QDialog, QComboBox, QTabWidget
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap


class LoadingPage(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Loading...")
        self.setFixedSize(300, 150)

        self.loading_label = QLabel("Iltimos, tizimni tekshirish...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        layout = QVBoxLayout()
        layout.addWidget(self.loading_label)
        self.setLayout(layout)

        self.show()

    def check_system_info(self):
        """IP manzil va fayl tizimini tekshiradi"""
        ip_address = socket.gethostbyname(socket.gethostname())
        file_path = os.path.expanduser("~")
        return ip_address, file_path


class ParametrlarDasturi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("REV Parametrlari Dasturi")
        self.showMaximized()

        self.loading_page = LoadingPage()
        ip_address, file_path = self.loading_page.check_system_info()
        self.loading_page.loading_label.setText(f"IP: {ip_address}\nFayl Katalogi: {file_path}")
        QTimer.singleShot(3000, self.loading_page.accept)

        self.init_ui()
        self.create_database()

    def create_database(self):
        """SQLite bazasini yaratish"""
        conn = sqlite3.connect("rev_data.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rev_name TEXT,
            serial_number TEXT,
            frequency REAL, frequency_unit TEXT,
            signal_level REAL, signal_unit TEXT,
            frequency_stability REAL,
            modulation_type TEXT,
            bandwidth REAL, bandwidth_unit TEXT,
            measured_location_lat TEXT, measured_location_lon TEXT,
            installed_location_lat TEXT, installed_location_lon TEXT,
            protocol_number TEXT,
            engineer_name TEXT,
            measurement_date TEXT,
            created_at TEXT
        )
        """)
        conn.commit()
        conn.close()

    def init_ui(self):
        """UI komponentlarini yaratish"""
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Bosh sahifa
        self.main_tab = QWidget()
        self.init_main_tab()
        self.tab_widget.addTab(self.main_tab, "REV Parametrlari")

        # Dastur haqida sahifa
        self.about_tab = QWidget()
        self.init_about_tab()
        self.tab_widget.addTab(self.about_tab, "Dastur haqida")

    def init_main_tab(self):
        """Asosiy sahifa komponentlari"""
        self.inputs = []
        self.units = []
        self.labels = [
            ("REV nomi", []),
            ("Seriya raqami", []),
            ("Chastotasi", ["Hz", "kHz", "MHz", "GHz"]),
            ("Signal sathi darajasi", ["dBm", "dB", "Vt"]),
            ("Chastota barqarorligi", ["Hz"]),
            ("Modulyatsiya turi", ["AM", "CHM", "FM", "QPSK", "GMSK", "QAM", "4QAM", "16QAM", "64QAM", "256QAM"]),
            ("Polasa kengligi", ["Hz", "kHz", "MHz", "GHz"]),
            ("O’lchangan joyi (E)", []),
            ("O’lchangan joyi (N)", []),
            ("O’rnatilgan joyi (E)", []),
            ("O’rnatilgan joyi (N)", []),
            ("O’lchov bayonnoma raqami", []),
            ("O’lchovni o’tkazgan muhandis F.I.SH.", []),
            ("O’lchov o’tkazilgan sana", []),
        ]

        self.main_layout = QVBoxLayout()
        header_label = QLabel("Radiochastotalarni qayd etish dasturi")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(header_label)

        for label_text, unit_options in self.labels:
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"{label_text} ni kiriting")
            input_field.setStyleSheet("padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px;")

            row_layout = QHBoxLayout()
            row_layout.addWidget(label)
            row_layout.addWidget(input_field)

            if unit_options:
                unit_selector = QComboBox()
                unit_selector.addItems(unit_options)
                unit_selector.setStyleSheet("padding: 8px; font-size: 14px;")
                row_layout.addWidget(unit_selector)
                self.units.append(unit_selector)
            else:
                self.units.append(None)

            self.main_layout.addLayout(row_layout)
            self.inputs.append(input_field)

        self.save_button = QPushButton("Saqlash", self)
        self.save_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")
        self.save_button.clicked.connect(self.save_data)

        self.export_button = QPushButton("Excel Yuklab Olish", self)
        self.export_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; font-size: 14px;")
        self.export_button.clicked.connect(self.export_to_excel)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.export_button)

        scroll_area = QScrollArea()
        container = QWidget()
        container.setLayout(self.main_layout)
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)

        root_layout = QVBoxLayout()
        root_layout.addWidget(scroll_area)
        root_layout.addLayout(button_layout)

        self.main_tab.setLayout(root_layout)

    def init_about_tab(self):
        """Dastur haqida sahifa"""
        layout = QVBoxLayout()

        about_label = QLabel("Radiochastotalarni Qayd etish dasturi\nDasturchi: Behruz Goffarov\n")
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(about_label)

        image_label = QLabel()
        pixmap = QPixmap("avatar.png")
        image_label.setPixmap(pixmap.scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        self.about_tab.setLayout(layout)

    def save_data(self):
        """Ma'lumotni bazaga saqlash"""
        values = []
        units = []

        try:
            for input_field, unit_selector in zip(self.inputs, self.units):
                value = input_field.text()
                unit = unit_selector.currentText() if unit_selector else None
                values.append(value if value else None)
                units.append(unit if unit else None)

        # Agar barcha parametrlar kiritilgan bo'lsa, 'None' o'rniga qiymatni kiritish
        # Qo'shimcha qiymatlarni to'ldirish
            values.extend([None] * (18 - len(values)))  # Agar kamroq parametr bo'lsa, 'None' qo'shiladi

            conn = sqlite3.connect("rev_data.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO parameters (
                rev_name, serial_number, frequency, frequency_unit, signal_level, signal_unit,
                frequency_stability, modulation_type, bandwidth, bandwidth_unit,
                measured_location_lat, measured_location_lon, installed_location_lat,
                installed_location_lon, protocol_number, engineer_name,
                measurement_date, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, values)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Ma'lumot saqlandi", "Ma'lumot muvaffaqiyatli saqlandi!")
            for input_field in self.inputs:
             input_field.clear()
        except Exception as e:
            QMessageBox.warning(self, "Xatolik", f"Saqlashda xatolik: {e}")

    def export_to_excel(self):
        """Ma'lumotlarni Excel faylga eksport qilish"""
        try:
            conn = sqlite3.connect("rev_data.db")
            query = "SELECT * FROM parameters"
            df = pd.read_sql_query(query, conn)
            conn.close()

            # Faylga o'lchov birliklarini ham qo'shish
            df.columns = ['ID', 'REV nomi', 'Seriya raqami', 'Chastota', 'Chastota birligi',
                          'Signal sathi', 'Signal birligi', 'Chastota barqarorligi',
                          'Modulyatsiya turi', 'Polasa kengligi', 'Polasa kengligi birligi',
                          'O’lchangan joyi (E)', 'O’lchangan joyi (N)', 'O’rnatilgan joyi (E)',
                          'O’rnatilgan joyi (N)', 'O’lchov bayonnoma raqami', 'O’lchovni o’tkazgan muhandis',
                          'O’lchov o’tkazilgan sana', 'Yaratilgan vaqt']
            # Excel faylga yozish
            df.to_excel("rev_data.xlsx", index=False)
            QMessageBox.information(self, "Excel eksporti", "Ma'lumotlar muvaffaqiyatli Excelga eksport qilindi!")
        except Exception as e:
            QMessageBox.warning(self, "Xatolik", f"Excelga eksport qilishda xatolik: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParametrlarDasturi()
    window.show()
    sys.exit(app.exec_())
