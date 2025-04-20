import qtawesome as qta  # qtawesome 모듈 가져오기
from PyQt6.QtWidgets import QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt  # 커서를 변경하기 위한 모듈
from modules import title_widget  # 타이틀 모듈 임포트
from pages.configuration_page import ConfigurationPage

class WelcomePage(QWidget):
    def __init__(self, parent=QWidget):
        super().__init__(parent)

        # 전체 레이아웃 설정
        self.parent = parent
        self.main_layout = QVBoxLayout()

        # 타이틀 라벨 설정 (모듈 사용)
        self.title = QLabel()
        self.title.setText('Train Simulator') # 타이틀을 좌측 정렬
        self.title.setObjectName('h1_heading')
        self.main_layout.addWidget(self.title)

        self.main_layout.addSpacing(10)  # 20px 간격 추가

        # QStackedWidget 생성
        self.stacked_widget = QStackedWidget()

        # 페이지 1 - Create a new project
        self.page1 = self.create_project_page()

        # 페이지 2 - Open previous project
        self.page2 = self.open_previous_project_page()

        # 각 페이지를 QStackedWidget에 추가
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        # QLabel 버튼 생성
        button_layout = QHBoxLayout()  # 버튼들을 가로로 배치
        button_layout.setContentsMargins(25, 0, 0, 0)  # 왼쪽에 20px 여백을 추가

        self.create_project_button = QLabel("Create a new project")
        self.create_project_button.setObjectName('createprojectoption')
        self.create_project_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_project_button.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 좌측 정렬
        self.create_project_button.mousePressEvent = self.show_create_project

        self.open_project_button = QLabel("Open previous project")
        self.open_project_button.setObjectName('openprojectoption')
        self.open_project_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_project_button.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 좌측 정렬
        self.open_project_button.mousePressEvent = self.show_open_project

        button_layout.addWidget(self.create_project_button)
        button_layout.addWidget(self.open_project_button)

        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def create_project_page(self):
        # 페이지 1 - 프로젝트 생성 페이지 구성
        page1_frame = QFrame()
        page1_frame.setObjectName('create_frame')
        page1_layout = QVBoxLayout()

        # 프로젝트 이름 라벨 및 입력 필드
        project_name_label = QLabel('Project Name:')
        project_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 좌측 정렬
        project_name_label.setObjectName('projectnamelabel')
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter project name")  # 플레이스홀더 추가
        self.project_name_input.setFixedHeight(30) # 입력 필드의 높이 설정
        self.project_name_input.setObjectName("nameinput")
        
        # Insert error labels
        self.project_name_error = QLabel('project name is empty')
        self.project_name_error.setObjectName('errorlabel1')
        self.user_name_error = QLabel('user name is empty')
        self.user_name_error.setObjectName('errorlabel2')
        self.project_name_error.hide()
        self.user_name_error.hide()

        # 작성자 라벨 및 입력 필드
        created_by_label = QLabel('Created By:')
        created_by_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 좌측 정렬
        created_by_label.setObjectName('createdbylabel')
        self.created_by_input = QLineEdit()
        self.created_by_input.setPlaceholderText("Enter your name")  # 플레이스홀더 추가
        self.created_by_input.setObjectName("nameinput")
        self.created_by_input.setFixedHeight(30)  # 입력 필드의 높이 설정

        # 생성 버튼
        self.create_button = QPushButton('Create')
        self.create_button.setObjectName('create')
        self.create_button.mousePressEvent = self.show_configuration_page

        # 레이아웃에 위젯 추가
        page1_layout.addWidget(project_name_label)
        page1_layout.addWidget(self.project_name_input)
        page1_layout.addWidget(self.project_name_error)
        page1_layout.addWidget(created_by_label)
        page1_layout.addWidget(self.created_by_input)
        page1_layout.addWidget(self.user_name_error)
        page1_layout.addWidget(self.create_button, alignment=Qt.AlignRight)
        page1_frame.setLayout(page1_layout)

        return page1_frame

    def open_previous_project_page(self):
        # 페이지 2 - 이전 프로젝트 열기 페이지 구성
        page2_frame = QFrame()
        page2_frame.setObjectName('existing_frame')
        page2_layout = QVBoxLayout()

        # 프로젝트 경로 라벨 및 입력 필드
        project_path_label = QLabel('Project Name:')
        project_path_label.setObjectName('projectnamelabel2')
        project_path_label.setObjectName('inputlabel1')
        project_path_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 좌측 정렬
        self.project_path_input = QLineEdit()
        path_layout = QHBoxLayout()
        browse_button = QPushButton(qta.icon('fa.folder-open', color='white'), 'Browse')
        browse_button.clicked.connect(self.browse_file)
        path_layout.addWidget(self.project_path_input)
        path_layout.addWidget(browse_button)

        # 열기 버튼
        open_button = QPushButton('Open')

        # 레이아웃에 위젯 추가
        page2_layout.addWidget(project_path_label)
        page2_layout.addLayout(path_layout)
        page2_layout.addWidget(open_button)
        page2_frame.setLayout(page2_layout)
        return page2_frame

    def browse_file(self):
        # 파일 탐색기 열기
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Project Files (*.json *.xml);;All Files (*)")
        if file_name:
            # 파일 이름만 추출해서 텍스트 필드에 표시
            self.project_path_input.setText(file_name.split('/')[-1])

    def show_create_project(self, event):
        self.stacked_widget.setCurrentIndex(0)
        self.create_project_button.update()
        self.open_project_button.update()

    def show_open_project(self, event):
        self.stacked_widget.setCurrentIndex(1)      
        self.open_project_button.update()
        self.create_project_button.update()

    def show_configuration_page(self, event):
        project_name = self.project_name_input.text()
        user_name = self.created_by_input.text()

        if (len(project_name) == 0) and (len(user_name) == 0):
            self.project_name_error.show()
            self.user_name_error.show()
            return
        elif len(project_name) == 0:
            self.project_name_error.show()
            return
        elif len(user_name) == 0:
            self.user_name_error.show()
            return
        
        # 페이지 3 - Open configuration page
        self.title.setText('Settings Page')
        self.setObjectName('h2_heading')
        self.page3 = ConfigurationPage(project_name, user_name)
        self.stacked_widget.addWidget(self.page3)
        
        self.create_project_button.hide()
        self.open_project_button.hide()
        self.stacked_widget.setCurrentIndex(2)
        self.create_button.update()
        self.open_project_button.update()
        self.create_project_button.update()

        