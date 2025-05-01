from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
import pyqtgraph as pg

class ReportPage(QDialog):
    def __init__(self, url, parent=None):
        super().__init__()

        #Set up the report page
        self.setWindowTitle("Simulation Results Report")

        self.browser = QWebEngineView()
        self.browser.load(QUrl(url))
        self.simulation_title = QLabel("Simulation Results Report")
        self.simulation_title.setObjectName('simulation_title')

        layout = QVBoxLayout()
        layout.setContentsMargins(20,60,20,60)
        layout.addWidget(self.simulation_title)
        layout.addWidget(self.browser)

        self.setLayout(layout)
        self.resize(1000, 400)

        self.browser.loadFinished.connect(self.on_load_finished)
    
    def on_load_finished(self, ok):
        if ok:
            print("Page loaded successfully")
        else:
            print("Failed to load page")

        
        
