import qtawesome as qta  # qtawesome 모듈 가져오기
from PyQt6.QtWidgets import QWidget, QScrollArea, QComboBox, QTabWidget, QTableWidget, QListWidget, QListWidgetItem, QStackedWidget, QVBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt, QRect # 커서를 변경하기 위한 모듈
from modules import title_widget  # 타이틀 모듈 임포트
from functools import partial
import matplotlib
matplotlib.use('QtAgg')

class GraphExpansionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create main container and layout
        container = QWidget()
        main_layout = QVBoxLayout()
        
        # Create search bar
        self.searchbar = QLineEdit()
        main_layout.addWidget(self.searchbar)
        
        # Create scroll area
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        
        # Controls container
        controls_container = QWidget()
        controls_layout = QVBoxLayout()
        
        # Add sample widgets
        self.widgets = []
        widget_names = ["Heater", "Light", "Fan"]
        for name in widget_names:
            widget = QWidget()
            widget_layout = QHBoxLayout()
            label = QLabel(name)
            btn = QPushButton("On")
            widget_layout.addWidget(label)
            widget_layout.addWidget(btn)
            widget.setLayout(widget_layout)
            controls_layout.addWidget(widget)
            self.widgets.append(widget)
            
        # Add spacer
        controls_layout.addStretch()
        
        controls_container.setLayout(controls_layout)
        self.scroll.setWidget(controls_container)
        main_layout.addWidget(self.scroll)
        
        container.setLayout(main_layout)
        self.setCentralWidget(container)
