import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QStackedWidget, QFileDialog, QFrame, QMessageBox,
    QDialog, QDialogButtonBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from pages.configuration_page import ConfigurationPage
from pages.simulation_dashboard import SimulationDashboard
from scripts.data_validation.validators import validate_train_json, validate_track_json

class WelcomePage(QWidget):
    def __init__(self, parent=QWidget):
        super().__init__(parent)
        self.parent = parent

        self.init_ui()
        self.attach_events()
        self.activate_page(0, self.create_project_button)

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.title = QLabel('Train Simulator')
        self.title.setObjectName('h1_heading')
        self.main_layout.addWidget(self.title)
        self.main_layout.addSpacing(10)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(25, 0, 0, 0)

        self.create_project_button = QPushButton("Create a new project")
        self.create_project_button.setObjectName('createprojectoption')
        self.create_project_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.open_project_button = QPushButton("Open previous project")
        self.open_project_button.setObjectName('openprojectoption')
        self.open_project_button.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addWidget(self.create_project_button)
        button_layout.addWidget(self.open_project_button)
        self.main_layout.addLayout(button_layout)

        self.stacked_widget = QStackedWidget()
        self.page1 = self.create_project_page()
        self.page2 = self.open_previous_project_page()
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.main_layout.addWidget(self.stacked_widget)

        self.create_button = QPushButton('Create')
        self.create_button.setObjectName('create')
        self.create_button.clicked.connect(self.show_configuration_page)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 15, 20, 15)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.create_button)
        self.main_layout.addLayout(bottom_layout)
        self.main_layout.addStretch()

    def attach_events(self):
        self.create_project_button.clicked.connect(lambda: self.activate_page(0, self.create_project_button))
        self.open_project_button.clicked.connect(lambda: self.activate_page(1, self.open_project_button))

    def create_project_page(self):
        frame = QFrame()
        frame.setObjectName('create_frame')
        layout = QVBoxLayout()

        layout.addWidget(self._label('Project Name:', 'projectnamelabel'))
        self.project_name_input = self._input_field("Enter project name")
        layout.addWidget(self.project_name_input)
        self.project_name_error = self._error_label('project name is empty')
        layout.addWidget(self.project_name_error)

        layout.addWidget(self._label('Created By:', 'createdbylabel'))
        self.created_by_input = self._input_field("Enter your name")
        layout.addWidget(self.created_by_input)
        self.user_name_error = self._error_label('user name is empty')
        layout.addWidget(self.user_name_error)

        layout.addWidget(self._label('Track Data:', 'tracklabel'))
        self.track_path_input = QLineEdit()
        self.track_path_input.setPlaceholderText("Choose track data file")
        track_browse = QPushButton("Browse")
        track_browse.clicked.connect(self.browse_track_file)
        track_format = QPushButton("Track Format")
        track_format.clicked.connect(lambda: self.show_format_dialog("assets/track_format.png", "Track Format"))
        track_layout = QHBoxLayout()
        track_layout.addWidget(self.track_path_input)
        track_layout.addWidget(track_browse)
        track_layout.addWidget(track_format)
        layout.addLayout(track_layout)

        layout.addWidget(self._label('Train Data:', 'trainlabel'))
        self.train_path_input = QLineEdit()
        self.train_path_input.setPlaceholderText("Choose train data file")
        train_browse = QPushButton("Browse")
        train_browse.clicked.connect(self.browse_train_file)
        train_format = QPushButton("Train Format")
        train_format.clicked.connect(lambda: self.show_format_dialog("assets/train_format.png", "Train Format"))
        train_layout = QHBoxLayout()
        train_layout.addWidget(self.train_path_input)
        train_layout.addWidget(train_browse)
        train_layout.addWidget(train_format)
        layout.addLayout(train_layout)

        frame.setLayout(layout)
        return frame

    def show_format_dialog(self, image_path, title):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout()
        pixmap = QPixmap(image_path)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        layout.addWidget(label)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.exec()

    def open_previous_project_page(self):
        frame = QFrame()
        frame.setObjectName('existing_frame')
        layout = QVBoxLayout()

        layout.addWidget(self._label('Project Name:', 'projectnamelabel2'))
        path_layout = QHBoxLayout()
        self.project_path_input = QLineEdit()
        browse_button = QPushButton(qta.icon('fa.folder-open', color='white'), 'Browse')
        browse_button.clicked.connect(self.browse_file)
        path_layout.addWidget(self.project_path_input)
        path_layout.addWidget(browse_button)

        open_button = QPushButton('Open')

        layout.addLayout(path_layout)
        layout.addWidget(open_button)
        frame.setLayout(layout)
        return frame

    def show_configuration_page(self):
        project_name = self.project_name_input.text()
        user_name = self.created_by_input.text()
        track_path = self.track_path_input.text()
        train_path = self.train_path_input.text()

        self.project_name_error.hide()
        self.user_name_error.hide()

        if not project_name:
            self.project_name_error.show()
        if not user_name:
            self.user_name_error.show()
        if not track_path or not train_path:
            QMessageBox.warning(self, "Missing files", "Please select both track and train data files.")
            return
        if not project_name or not user_name:
            return

        self.title.setText('Settings')

        self.run_button = QPushButton('Run simulation')
        self.run_button.setFixedWidth(150)
        self.run_button.clicked.connect(self.show_simulation_page)

        self.page3 = ConfigurationPage(project_name, user_name, self.run_button)
        self.stacked_widget.addWidget(self.page3)
        self.stacked_widget.setCurrentIndex(2)

        self.create_project_button.hide()
        self.open_project_button.hide()
        self.create_button.hide()

    def show_simulation_page(self):
        self.title.setText('Simulation Dashboard')
        self.page4 = SimulationDashboard()
        self.stacked_widget.addWidget(self.page4)
        self.stacked_widget.setCurrentIndex(3)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Project Files (*.json *.xml);;All Files (*)")
        if file_name:
            self.project_path_input.setText(file_name.split('/')[-1])

    def browse_track_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Track Data", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_name:
            valid, error = validate_track_json(file_name)
            if not valid:
                QMessageBox.critical(self, "Invalid Track File", error)
                return
            self.track_path_input.setText(file_name)

    def browse_train_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Train Data", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_name:
            valid, error = validate_train_json(file_name)
            if not valid:
                QMessageBox.critical(self, "Invalid Train File", error)
                return
            self.train_path_input.setText(file_name)

    def _label(self, text, object_name):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setObjectName(object_name)
        return label

    def _input_field(self, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setObjectName('nameinput')
        field.setFixedHeight(30)
        return field

    def _error_label(self, text):
        label = QLabel(text)
        label.setObjectName('errorlabel')
        label.setStyleSheet("color: red; font-size: 12px;")
        label.hide()
        return label

    def activate_page(self, index, button):
        self.set_active_button(button)
        self.stacked_widget.setCurrentIndex(index)

    def set_active_button(self, active_button):
        for btn in [self.create_project_button, self.open_project_button]:
            btn.setProperty("active", btn == active_button)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
