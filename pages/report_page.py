from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import pyqtgraph as pg

class ReportPage(QDialog):
    def __init__(self):
        super().__init__()
        
        #Set up the report page
        self.setWindowTitle("Simulation Results Report")
        self.setMinimumSize(600, 400)

        self.browser = QWebEngineView()
        self.browser.load("https://www.google.com")

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.browser)

        self.setLayout(layout)
        self.browser.setUrl(QUrl("https://www.example.com"))

        self.browser.loadFinished.connect(self.on_load_finished)
    
    def on_load_finished(self, ok):
        if ok:
            print("Page loaded successfully")
        else:
            print("Failed to load page")

        
        
