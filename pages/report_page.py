from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from scripts.visualize.plot_table import *
from scripts.visualize.dash_worker import *

class ReportPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Set up the report page
        self.setWindowTitle("Simulation Data Results")
        self.browser = QWebEngineView()
        self.simulation_title = QLabel("Simulation Data Results")
        self.simulation_title.setObjectName('simulation_title')

        layout = QVBoxLayout()
        layout.setContentsMargins(20,60,20,60)
        layout.addWidget(self.simulation_title)
        layout.addWidget(self.browser)

        self.setLayout(layout)

        # Initialize worker thread
        self.init_worker_thread()

        #resize dialog
        self.resize(parent.size() if parent else QSize(800, 600))

    def init_worker_thread(self):
        #Initialize worker thread and connections
        self.worker_thread = QThread()
        self.dash_worker = DashWorker(plot_interactive_table_dash("algorithms/simulation_results/final_simulation(Lucinda).json"), 8050)
        
        # Move worker to thread
        self.dash_worker.moveToThread(self.worker_thread)
        
        # Connect signals and slots
        self.worker_thread.started.connect(self.dash_worker.run_server)
        self.dash_worker.finished.connect(self.worker_thread.quit)
        self.dash_worker.finished.connect(self.dash_worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.dash_worker.progress.connect(self.update_status)
        
        # Start thread
        self.worker_thread.start()

    def update_status(self, status):
        #Update window title with status
         self.setWindowTitle("Simulation Data Results")

    def closeEvent(self, event):
        #Handle window closing
        if hasattr(self, 'dash_worker'):
            self.dash_worker.shutdown_server()
        event.accept()  
