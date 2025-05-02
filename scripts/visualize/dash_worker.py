from PyQt6.QtCore import QThread, QObject, pyqtSignal
from scripts.visualize.dash_worker import *
import threading

class DashWorker(QObject):
    #Worker object that handles the Dash application
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def __init__(self, application):
        super().__init__()
        self.app = None
        self.server_thread = None
        self.running = False
        self.application = application
    
    def run_server(self):
        self.app = self.application
        self.server_thread = threading.Thread(target=lambda: self.app.run(
            debug=False,
            host='127.0.0.1',
            port=8050,
            use_reloader=False
        ))
        self.server_thread.daemon = True
        self.server_thread.start()
        self.progress.emit("Server started")
        self.running = True

    def shutdown_server(self):
        if self.running and self.server_thread:
            self.app.server.shutdown_server()
            self.server_thread.join(timeout=5)
            self.running = False
            self.progress.emit("Server stopped")