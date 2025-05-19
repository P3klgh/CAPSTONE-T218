from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGroupBox, QFormLayout, QPushButton
)
from PyQt6.QtGui import QPixmap
import os
import json

from scripts.visualize.track_mapper import generate_track_plot  # ✅ 새 matplotlib 기반 함수 사용


# ✅ train_spec.json 로드 함수
def load_train_spec(filepath="given_data/train_spec.json"):
    with open(filepath, "r") as f:
        data = json.load(f)

    full_bins = data["num_full_bins"]
    empty_bins = data["num_empty_bins"]

    total_mass = (
        data["mass_full_bin"] * full_bins +
        data["mass_empty_bin"] * empty_bins +
        data["mass_locomotive"] +
        (data["mass_brakevan"] if data["has_brakevan"] else 0)
    )

    return total_mass, full_bins, empty_bins


class ConfigurationPage(QWidget):
    def __init__(self, project_name, user_name, run_button, parent=None):
        super().__init__(parent)

        self.project_name = project_name
        self.user_name = user_name

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(20, 20, 20, 20)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        main_layout.addWidget(self.create_train_summary_box())
        main_layout.addWidget(self.create_track_map_box(), stretch=1)
        main_layout.addWidget(self.create_simulation_input_box())

        outer_layout.addLayout(main_layout)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        run_button.setFixedWidth(160)
        button_layout.addWidget(run_button)

        outer_layout.addLayout(button_layout)

        self.setLayout(outer_layout)

        # ✅ Train Summary 라벨 초기화
        self.update_train_summary()

    def create_train_summary_box(self):
        group = QGroupBox("Train Summary")
        layout = QVBoxLayout()

        self.mass_label = QLabel("Total Mass: -- kg")
        self.full_bin_label = QLabel("Full Bins: --")
        self.empty_bin_label = QLabel("Empty Bins: --")

        for label in [self.mass_label, self.full_bin_label, self.empty_bin_label]:
            label.setObjectName("small_label")
            layout.addWidget(label)

        group.setLayout(layout)
        return group

    def create_track_map_box(self):
        group = QGroupBox("Track Map")
        layout = QVBoxLayout()

        # 🟡 테스트용 샘플 경로
        track_json_path = "given_data/extracted_processed_json/final_merged(Karloo).json"
        output_image_path = "visual_output/karloo_track.png"

        generate_track_plot(track_json_path, output_image_path)

        # 🖼️ 이미지 로드
        pixmap = QPixmap(output_image_path)
        if pixmap.isNull():
            print("[ERROR] Could not load map image:", output_image_path)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setMinimumSize(400, 250)

        layout.addWidget(image_label)
        group.setLayout(layout)
        return group

    def create_simulation_input_box(self):
        group = QGroupBox("Simulation Settings")
        layout = QVBoxLayout()
        layout.setSpacing(12)

        input_style = {
            "placeholderTexts": ["e.g. 40", "e.g. 1200", "e.g. 90"],
            "objectNames": ["small_input2"] * 3,
            "labels": ["Initial Speed (km/h):", "Initial RPM:", "Max Speed (km/h):"]
        }

        inputs = [QLineEdit() for _ in range(3)]
        for i, field in enumerate(inputs):
            field.setPlaceholderText(input_style["placeholderTexts"][i])
            field.setObjectName(input_style["objectNames"][i])
            label = QLabel(input_style["labels"][i])
            label.setObjectName("small_label")

            layout.addWidget(label)
            layout.addWidget(field)

        self.init_speed_input = inputs[0]
        self.init_rpm_input = inputs[1]
        self.max_speed_input = inputs[2]

        group.setLayout(layout)
        return group

    # ✅ Train Summary 라벨 업데이트 함수
    def update_train_summary(self):
        try:
            total_mass, full_bins, empty_bins = load_train_spec()
            self.mass_label.setText(f"Total Mass: {total_mass:,} kg")
            self.full_bin_label.setText(f"Full Bins: {full_bins}")
            self.empty_bin_label.setText(f"Empty Bins: {empty_bins}")
        except Exception as e:
            print("[ERROR] Failed to load train_spec.json:", e)
