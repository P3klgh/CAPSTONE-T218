import qtawesome as qta  # qtawesome 모듈 가져오기
from PyQt6.QtWidgets import QWidget, QComboBox, QTabWidget, QTableWidget, QListWidget, QListWidgetItem, QStackedWidget, QVBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt, QRect # 커서를 변경하기 위한 모듈
from modules import title_widget  # 타이틀 모듈 임포트
from functools import partial
import matplotlib
matplotlib.use('QtAgg')

class GraphExpansionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.frame_layout = QHBoxLayout()

        # Graphical output:
        self.graphical_label = "Graphical output:"

    def create_graphical_output():
        self.plot_graph.showGrid(x=True, y=True)

    def create_map_layout():
        # Top:
        self.map_layout = "Map Layout:"
        self.map_layout_top = "Top:"

        # Side:
        self.map_layout_side = "Side:"
    
    def update_data():
        # Update data arrays
        self.plot_graph
        self.plot_graph.plot(new_x_data, new_y_data)
