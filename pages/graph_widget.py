from random import randint
from PyQt6.QtWidgets import QWidget, QComboBox, QTabWidget, QTableWidget, QListWidget, QListWidgetItem, QStackedWidget, QVBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PyQt6 import QtCore, QtWidgets
import pyqtgraph as pg

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Temperature vs time plot
        self.plot_graph = pg.PlotWidget()
        self.frame_layout = QHBoxLayout()
        self.frame_layout.addWidget(self.plot_graph)
        self.setLayout(self.frame_layout)
        self.plot_graph.setBackground("#f0f0f0")

        # plot static (default) values
        minutes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        self.plot_graph.plot(minutes, temperature)
        self.setFixedSize(250, 250)
        self.setContentsMargins(0,0,0,0)
