import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget, QLabel, QFrame)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

class RichterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Richter Management Tools")
        self.resize(1280, 800)
        
        # Dark Mode Styling für die gesamte App
        self.setStyleSheet("background-color: #121212; color: #e5e7eb;")

        # Zentrales Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-right: 1px solid #2d2d2d;
            }
            QPushButton {
                background-color: transparent;
                color: #a0a0a0;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
                border-left: 3px solid transparent;
            }
            QPushButton:hover {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QPushButton[active="true"] {
                background-color: #2d2d2d;
                color: #dc2626;
                border-left: 4px solid #dc2626;
            }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        sidebar_layout.setSpacing(5)

        # Titel / Logo Bereich
        title_label = QLabel("RICHTER TOOLS")
        title_label.setStyleSheet("color: #dc2626; font-size: 18px; font-weight: bold; padding: 20px;")
        sidebar_layout.addWidget(title_label)

        # Buttons definieren
        self.btn_personal = QPushButton(" Personalkosten")
        self.btn_ker = QPushButton(" KER Analyse")
        
        self.nav_buttons = [self.btn_personal, self.btn_ker]
        
        for btn in self.nav_buttons:
            sidebar_layout.addWidget(btn)
            btn.clicked.connect(self.display_tool)

        sidebar_layout.addStretch()
        
        # Footer
        version_label = QLabel("v1.0.1")
        version_label.setStyleSheet("color: #404040; padding: 10px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(self.sidebar)

        # --- Content Bereich ---
        self.content_stack = QStackedWidget()
        
        # View 1: Personalkosten
        self.web_personal = QWebEngineView()
        self.load_html_into_view(self.web_personal, "Personalkosten Richter.html")
        self.content_stack.addWidget(self.web_personal)

        # View 2: KER Analyse
        self.web_ker = QWebEngineView()
        self.load_html_into_view(self.web_ker, "KER Analyse Tool.html")
        self.content_stack.addWidget(self.web_ker)

        main_layout.addWidget(self.content_stack)
        
        # Ersten Button aktivieren
        self.set_active_button(self.btn_personal)

    def load_html_into_view(self, view, filename):
        """Sucht die Datei im lokalen Pfad und lädt sie in die WebEngine."""
        # Prüfen ob Datei im aktuellen Verzeichnis existiert
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, filename)
        
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            view.setHtml(html)
        else:
            # Platzhalter falls Datei fehlt
            error_html = f"""
            <body style='background:#121212; color:white; font-family:sans-serif; 
                         display:flex; flex-direction:column; justify-content:center; 
                         align-items:center; height:100vh;'>
                <h2 style='color:#dc2626;'>Datei nicht gefunden</h2>
                <p>Bitte stelle sicher, dass <b>{filename}</b> im selben Ordner wie die .py Datei liegt.</p>
            </body>
            """
            view.setHtml(error_html)

    def display_tool(self):
        btn = self.sender()
        self.set_active_button(btn)
        
        if btn == self.btn_personal:
            self.content_stack.setCurrentIndex(0)
        elif btn == self.btn_ker:
            self.content_stack.setCurrentIndex(1)

    def set_active_button(self, active_btn):
        for btn in self.nav_buttons:
            btn.setProperty("active", btn == active_btn)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RichterApp()
    window.show()
    sys.exit(app.exec())
