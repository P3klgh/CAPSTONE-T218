import qtawesome as qta  # qtawesome 모듈 가져오기
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # 커서를 변경하기 위한 모듈
from modules import title_widget  # 타이틀 모듈 임포트
from functools import partial
from pages.graph_widget import GraphWidget
from pages.report_page import ReportPage
from PyQt6.QtWebEngineWidgets import QWebEngineView
import matplotlib
matplotlib.use('QtAgg')

class SimulationDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        main_layout = QHBoxLayout()

        #left panel
        content_layout1 = QHBoxLayout()
        content_layout1.setContentsMargins(0, 0, 0, 0)
        content_layout1.setSpacing(2)

        # Add graphical widgets
        self.graph_widget = GraphWidget()
        self.graph_widget2 = GraphWidget()
        self.graph_widget3 = GraphWidget()
        self.graph_widget4 = GraphWidget()
        graph_grid = QVBoxLayout()
        graph_grid2 = QVBoxLayout()
        graph_grid.addWidget(self.graph_widget)
        graph_grid.addWidget(self.graph_widget2)
        graph_grid2.addWidget(self.graph_widget3)
        graph_grid2.addWidget(self.graph_widget4)
        content_layout1.addLayout(graph_grid)
        content_layout1.addLayout(graph_grid2)
        
        # Control panel
        self.control_panel = QWidget()
        control_layout = QVBoxLayout(self.control_panel)
        
        # Add controls
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_label = QLabel("Speed: 1")
        
        self.start_button = QPushButton("Start Simulation")
        self.reset_button = QPushButton("Reset")

        # Display labels
        self.map_label = QLabel("Map Layout:")
        
        # Add widgets to control layout
        control_layout.addWidget(self.map_label)

        
        # Visualize / initialize simulation report
        self.view_report_button = QPushButton("View report")
        self.view_report_button.clicked.connect(self.show_report)
        control_layout.addWidget(self.view_report_button)
        
        # Display area
        self.display_area = QWidget()
        display_layout = QGridLayout(self.display_area)
        
        # Status labels
        self.status_label = QLabel("Status: Idle")
        self.value_label = QLabel("Value: 0.0")
        
        display_layout.addWidget(self.map_label, 0, 0)
        display_layout.addWidget(self.status_label, 1, 0)
        display_layout.addWidget(self.value_label, 2, 0)
        
        # Add panels to main layout
        main_layout.addLayout(content_layout1)
        main_layout.addWidget(self.control_panel)
        main_layout.addWidget(self.display_area)
        
        # Setup timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        
        # Connect signals
        self.speed_slider.valueChanged.connect(self.update_speed)
        self.start_button.clicked.connect(self.toggle_simulation)
        self.reset_button.clicked.connect(self.reset_simulation)
        
        # Initialize state
        self.is_running = False
        self.simulation_value = 0.0

        self.setLayout(main_layout)
        
    def update_speed(self):
        speed = self.speed_slider.value()
        self.speed_label.setText(f"Speed: {speed}")
    
    def toggle_simulation(self):
        if not self.is_running:
            self.timer.start(1000 // self.speed_slider.value())
            self.start_button.setText("Stop Simulation")
            self.status_label.setText("Status: Running")
        else:
            self.timer.stop()
            self.start_button.setText("Start Simulation")
            self.status_label.setText("Status: Paused")
        self.is_running = not self.is_running
    
    def reset_simulation(self):
        self.timer.stop()
        self.is_running = False
        self.simulation_value = 0.0
        self.start_button.setText("Start Simulation")
        self.status_label.setText("Status: Idle")
        self.value_label.setText("Value: 0.0")
    
    def update_simulation(self):
        # Your simulation logic goes here
        self.simulation_value += 0.1 * (self.speed_slider.value() / 50.0)
        self.value_label.setText(f"Value: {self.simulation_value:.2f}")
    
    def show_report(self):
         #create window 
        self.report_window = ReportPage("https://www.google.com/")
        self.report_window.exec()
        # self.view = QWebEngineView()
        # self.view.setUrl(QUrl("https://qt-project.org/"))
        # self.view.resize(1024, 750)
        # self.view.show()


