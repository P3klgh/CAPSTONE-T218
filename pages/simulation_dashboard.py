from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from pages.report_page import ReportPage
from scripts.visualize.plot_graphs import plot_energy_velocity_toggle
import matplotlib
matplotlib.use('QtAgg')


class SimulationDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ─── Main Layout ───────────────────────────────
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(30)

        # ─── Graph Panel (with GroupBox) ───────────────
        graph_group = QGroupBox("Simulation Graph")
        graph_layout = QVBoxLayout()

        self.graph_view = QWebEngineView()
        graph_url = QUrl.fromLocalFile(
            plot_energy_velocity_toggle("algorithms/simulation_results/final_simulation(Lucinda).json", 2)
        )
        self.graph_view.page().setUrl(graph_url)

        graph_layout.addWidget(self.graph_view)
        graph_group.setLayout(graph_layout)

        main_layout.addWidget(graph_group, stretch=2)

        # ─── Control Panel ─────────────────────────────
        self.control_panel = QWidget()
        control_layout = QVBoxLayout(self.control_panel)

        # 👉 GroupBox for Map Layout
        map_group = QGroupBox("Map Layout")
        map_layout = QVBoxLayout()

        self.map_layout_widget = QWebEngineView()
        self.map_layout_widget2 = QWebEngineView()
        self.map_layout_widget.setFixedSize(300, 150)
        self.map_layout_widget2.setFixedSize(300, 150)

        map_layout.addWidget(self.map_layout_widget)
        map_layout.addWidget(self.map_layout_widget2)
        map_group.setLayout(map_layout)

        control_layout.addWidget(map_group)
        control_layout.addStretch()

        self.view_report_button = QPushButton("View report")
        self.view_report_button.setFixedWidth(300)
        control_layout.addWidget(self.view_report_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.view_report_button.clicked.connect(self.show_report)

        main_layout.addWidget(self.control_panel, stretch=1)

        self.setLayout(main_layout)

    def show_report(self):
        self.report_page = ReportPage()
        self.report_page.browser.setUrl(QUrl("http://127.0.0.1:8050"))
        self.report_page.show()
