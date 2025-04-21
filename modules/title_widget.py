# 타이틀 모듈 (title_widget.py)
from PyQt6.QtWidgets import QLabel, QHBoxLayout

class TitleWidget:
    def create_title(title_text):
        title_label = QLabel(title_text)
        title_label.setStyleSheet("font-size: 22px; width: 100%; padding: 10px 5px; border-radius: 5px; font-weight: bold; color: #444444; margin-top: 10px; margin-left: 20px;")

        # 제목을 위한 레이아웃 생성
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        return title_layout