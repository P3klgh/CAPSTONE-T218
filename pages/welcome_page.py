from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QStackedWidget, QFileDialog, QFrame, QMessageBox,
    QDialog, QDialogButtonBox, QTextEdit
)
from PyQt6.QtGui import (
    QPixmap, QSyntaxHighlighter, QTextCharFormat, QColor
)
import qtawesome as qta
import json
from PyQt6.QtCore import Qt, QRegularExpression
from pages.configuration_page import ConfigurationPage
from pages.simulation_dashboard import SimulationDashboard
from scripts.data_validation.validators import validate_train_json, validate_track_json


class JSONHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#00aa00"))

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#1e90ff"))

        self.key_format = QTextCharFormat()
        self.key_format.setForeground(QColor("#bb86fc"))

        self.rules = [
            (QRegularExpression(r'"[^"]*"\s*:'), self.key_format),
            (QRegularExpression(r'"[^"]*"'), self.string_format),
            (QRegularExpression(r'\b\d+(\.\d+)?\b'), self.number_format)
        ]

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


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

        # Track Section
        layout.addWidget(self._label('Track Data:', 'tracklabel'))
        self.track_path_input = QLineEdit()
        self.track_path_input.setPlaceholderText("Choose track data file")
        track_browse = QPushButton("Browse")
        track_browse.clicked.connect(self.browse_track_file)
        track_format = QPushButton("Track Format")
        track_format.clicked.connect(lambda: self.show_format_dialog("Track Format", "track"))
        track_layout = QHBoxLayout()
        track_layout.addWidget(self.track_path_input)
        track_layout.addWidget(track_browse)
        track_layout.addWidget(track_format)
        layout.addLayout(track_layout)

        # Train Section
        layout.addWidget(self._label('Train Data:', 'trainlabel'))
        self.train_path_input = QLineEdit()
        self.train_path_input.setPlaceholderText("Choose train data file")
        train_browse = QPushButton("Browse")
        train_browse.clicked.connect(self.browse_train_file)
        train_format = QPushButton("Train Format")
        train_format.clicked.connect(lambda: self.show_format_dialog("Train Format", "train"))
        train_layout = QHBoxLayout()
        train_layout.addWidget(self.train_path_input)
        train_layout.addWidget(train_browse)
        train_layout.addWidget(train_format)
        layout.addLayout(train_layout)

        frame.setLayout(layout)
        return frame

    def show_format_dialog(self, title, format_type):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(700, 600)

        layout = QVBoxLayout()
        if format_type == "track":
            description_text = (
                "📘 Track JSON Format\n"
                "• Radius: Radius of the curve segment (in meters)\n"
                "• CurveID: Identifier for the curve segment\n"
                "• Z_Min: Minimum elevation at the segment's start (in meters)\n"
                "• Z_Max: Maximum elevation at the segment's end (in meters)\n"
                "• Z_Mean: Average elevation over the segment (in meters)\n"
                "• Avg_Slope: Average gradient of the segment\n"
                "• Min_Slope / Max_Slope: Minimum and maximum slope values\n"
                "• Length: Length of the track segment (in meters)\n"
                "• XStart / YStart: Starting coordinates (e.g. UTM)\n"
                "• XFinish / YFinish: Ending coordinates (e.g. UTM)\n"
                "• X_Center / Y_Center: Center point of the curve"
            )

            example_data = {
                "0.0": {
                    "Radius": 112.045,
                    "CurveID": 1720172,
                    "Z_Min": 25.87,
                    "Z_Max": 25.95,
                    "Z_Mean": 25.91,
                    "Min_Slope": 0.12,
                    "Max_Slope": 0.45,
                    "Avg_Slope": 0.30,
                    "Length": 526.08,
                    "XStart": 732213,
                    "YStart": 7609892,
                    "XFinish": 732219,
                    "YFinish": 7609868,
                    "X_Center": 732425.3,
                    "Y_Center": 7609523.2
                }
            }

            default_filename = "track_example.json"
        elif format_type == "train":
            description_text = (
                "📘 Train JSON Format\n"
                "• mass_full_bin: Mass of one fully loaded bin (in kg)\n"
                "• mass_empty_bin: Mass of one empty bin (in kg)\n"
                "• num_full_bins: Number of fully loaded bins\n"
                "• num_empty_bins: Number of empty bins\n"
                "• mass_locomotive: Mass of the locomotive (in kg)\n"
                "• mass_brakevan: Mass of the brake van (in kg)\n"
                "• has_brakevan: Whether a brake van is included (1 = Yes, 0 = No)\n"
                "• rolling_resistance_full: Rolling resistance of a full bin (N/ton)\n"
                "• rolling_resistance_empty: Rolling resistance of an empty bin (N/ton)\n"
                "• rolling_resistance_locomotive_drive: Rolling resistance of the locomotive (N)\n"
                "• rolling_resistance_brakevan: Rolling resistance of the brake van (N)\n"
                "• curve_resistance_factor: Resistance coefficient for curves\n"
                "• tractive_effort_curve: Dictionary mapping speed (km/h) to tractive effort (N)"
            )

            example_data = {
                "mass_full_bin": 7400,
                "mass_empty_bin": 1280,
                "num_full_bins": 30,
                "num_empty_bins": 5,
                "mass_locomotive": 38000,
                "mass_brakevan": 29000,
                "has_brakevan": 1,
                "rolling_resistance_full": 10.6,
                "rolling_resistance_empty": 13.3,
                "rolling_resistance_locomotive_drive": 184,
                "rolling_resistance_brakevan": 15,
                "curve_resistance_factor": 2628,
                "tractive_effort_curve": {
                    "0": 188.7,
                    "10": 155,
                    "20": 120
                }
            }

            default_filename = "train_example.json"

        description_label = QLabel(description_text)
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # JSON 예시
        json_view = QTextEdit()
        json_view.setPlainText(json.dumps(example_data, indent=4))
        json_view.setReadOnly(True)
        json_view.setFixedHeight(300)

        # ✅ 폰트 스타일 지정: Monospace
        font = json_view.font()
        font.setFamily("Courier New")
        font.setPointSize(10)
        json_view.setFont(font)

        # ✅ 하이라이터 적용
        JSONHighlighter(json_view.document())

        layout.addWidget(json_view)

        # 버튼
        download_btn = QPushButton("⬇ Save Example")
        close_btn = QPushButton("Close")

        def save_json():
            path, _ = QFileDialog.getSaveFileName(dialog, "Save JSON", default_filename, "JSON Files (*.json)")
            if path:
                with open(path, 'w') as f:
                    json.dump(example_data, f, indent=4)

        download_btn.clicked.connect(save_json)
        close_btn.clicked.connect(dialog.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(download_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

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
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Project", "",
                                                   "Project Files (*.json *.xml);;All Files (*)")
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
