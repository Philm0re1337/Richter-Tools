import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget, QLabel, QFrame)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

# HTML Content der Tools (vereinfacht als Strings hinterlegt für die Einzeldatei-Lösung)
# In einer echten Umgebung könnten diese auch aus den .html Dateien gelesen werden.

TOOL_PERSONALKOSTEN = """
<!-- Hier wird der Inhalt von 'Personalkosten Richter.html' eingefügt -->
"""

TOOL_KER_ANALYSE = """
<!-- Hier wird der Inhalt von 'KER Analyse Tool.html' eingefügt -->
"""

class RichterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Richter Management Tools")
        self.resize(1280, 800)
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
                border-left: 3px solid #dc2626;
            }
        """)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        sidebar_layout.setSpacing(5)

        # Logo / Titel
        title_label = QLabel("RICHTER TOOLS")
        title_label.setStyleSheet("color: #dc2626; font-size: 18px; font-weight: bold; padding: 20px;")
        sidebar_layout.addWidget(title_label)

        # Navigation Buttons
        self.btn_personal = QPushButton(" Personalkosten")
        self.btn_ker = QPushButton(" KER Analyse")
        
        self.nav_buttons = [self.btn_personal, self.btn_ker]
        
        for btn in self.nav_buttons:
            sidebar_layout.addWidget(btn)
            btn.clicked.connect(self.display_tool)

        sidebar_layout.addStretch()
        
        # Fußzeile Sidebar
        version_label = QLabel("v1.0")
        version_label.setStyleSheet("color: #404040; padding: 10px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(self.sidebar)

        # --- Content Area (Stacked Widget) ---
        self.content_stack = QStackedWidget()
        
        # Tool 1: Personalkosten
        self.web_personal = QWebEngineView()
        self.load_html_into_view(self.web_personal, "Personalkosten Richter.html")
        self.content_stack.addWidget(self.web_personal)

        # Tool 2: KER Analyse
        self.web_ker = QWebEngineView()
        self.load_html_into_view(self.web_ker, "KER Analyse Tool.html")
        self.content_stack.addWidget(self.web_ker)

        main_layout.addWidget(self.content_stack)
        
        # Initialer Status
        self.set_active_button(self.btn_personal)

    def load_html_into_view(self, view, filename):
        """Lädt die lokale HTML Datei in die Web-Ansicht."""
        path = os.path.abspath(filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            view.setHtml(html)
        else:
            view.setHtml(f"<body style='background:#121212;color:white;display:flex;justify-content:center;align-items:center;height:100vh;'><h1>Datei '{filename}' nicht gefunden.</h1></body>")

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
