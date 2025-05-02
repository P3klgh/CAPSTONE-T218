import qtawesome as qta  # qtawesome 모듈 가져오기
from PyQt6.QtWidgets import *
from PyQt6.QtCore import * # 커서를 변경하기 위한 모듈
from modules import title_widget  # 타이틀 모듈 임포트
from functools import partial
from pages.graph_widget import GraphWidget
from pages.report_page import ReportPage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPalette, QColor
from scripts.visualize.plot_table import *
from scripts.visualize.plot_graphs import *
import threading 
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
        
        graph1 = QWebEngineView()
        graph2 = QWebEngineView()
        graph3 = QWebEngineView()

        graph_grid = QVBoxLayout()
        graph_grid2 = QVBoxLayout()

        graph_grid.addWidget(graph1)
        graph_grid.addWidget(graph2)
        graph_grid2.addWidget(graph3)
        
        graph1.page().setUrl(QUrl.fromLocalFile(plot_energy_velocity_toggle("algorithms/simulation_results/final_simulation(Lucinda).json", 0)))
        graph2.page().setUrl(QUrl.fromLocalFile(plot_energy_velocity_toggle("algorithms/simulation_results/final_simulation(Lucinda).json", 1)))
        graph3.page().setUrl(QUrl.fromLocalFile(plot_energy_velocity_toggle("algorithms/simulation_results/final_simulation(Lucinda).json", 2)))
    
        content_layout1.addLayout(graph_grid)
        content_layout1.addLayout(graph_grid2)
        
        # Control panel
        self.control_panel = QWidget()
        control_layout = QVBoxLayout(self.control_panel)
        
        self.start_button = QPushButton("Start Simulation")
        self.reset_button = QPushButton("Reset")

        # Display labels
        self.map_label = QLabel("Map Layout:")
        
        # Add widgets to control layout
        control_layout.addWidget(self.map_label)

        # map layout widget(s)
        self.map_layout_widget = QWebEngineView()
        self.map_layout_widget2 = QWebEngineView()
        self.map_layout_widget.setFixedSize(300, 150)
        self.map_layout_widget2.setFixedSize(300, 150)
        
        control_layout.addWidget(self.map_layout_widget)
        control_layout.addWidget(self.map_layout_widget2)

        # Visualize / initialize simulation report
        self.view_report_button = QPushButton("View report")
        self.view_report_button.clicked.connect(self.show_report)

        control_layout.addWidget(self.view_report_button)
        
        # Display area
        # self.map_display_area = QWidget()
        # display_layout = QVBoxLayout(self.map_display_area)
        
        # Status labels
        # self.status_label = QLabel("Status: Idle")
        # self.value_label = QLabel("Value: 0.0")
        
        # display_layout.addWidget(self.map_label)
        # display_layout.addWidget(self.status_label, 1, 0)
        # display_layout.addWidget(self.value_label, 2, 0)
        
        # Add panels to main layout
        main_layout.addLayout(content_layout1)
        main_layout.addWidget(self.control_panel)

        self.setLayout(main_layout)
        
    
    def show_report(self):
        #create window
        self.report_page = ReportPage()
        self.report_page.browser.setUrl(QUrl("http://127.0.0.1:8050"))
        self.report_page.show()
