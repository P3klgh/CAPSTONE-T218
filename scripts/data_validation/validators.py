# scripts/data_validation/validators.py

import json
from jsonschema import validate, ValidationError
from .validation_schemas import train_schema, track_segment_schema

# 📌 필드별 설명 매핑
TRAIN_FIELD_DESCRIPTIONS = {
    "mass_full_bin": "Mass of a full bin (kg)",
    "mass_empty_bin": "Mass of an empty bin (kg)",
    "num_full_bins": "Number of full bins",
    "num_empty_bins": "Number of empty bins",
    "mass_locomotive": "Mass of the locomotive (kg)",
    "mass_brakevan": "Mass of the brake van (kg)",
    "has_brakevan": "Whether the train uses a brake van (0 or 1)",
    "rolling_resistance_full": "Rolling resistance of full bin (N/ton)",
    "rolling_resistance_empty": "Rolling resistance of empty bin (N/ton)",
    "rolling_resistance_locomotive_drive": "Locomotive resistance in drive (N/ton)",
    "rolling_resistance_locomotive_neutral": "Locomotive resistance in neutral (N/ton)",
    "rolling_resistance_brakevan": "Brake van rolling resistance (N/ton)",
    "curve_resistance_factor": "Curve resistance constant (Nm/ton)",
    "engine_power_curve": "Required engine power-speed data (dict of kW vs speed)",
    "tractive_efficiency_curve": "Optional tractive efficiency curve (dict of % vs speed)",
}

TRACK_FIELD_DESCRIPTIONS = {
    "XStart": "Start X coordinate (meters)",
    "YStart": "Start Y coordinate (meters)",
    "XFinish": "End X coordinate (meters)",
    "YFinish": "End Y coordinate (meters)",
    "Z_Min": "Start elevation (meters)",
    "Z_Max": "End elevation (meters)",
    "Length": "Segment length (meters)",
    "Track_speed_Limit": "Speed limit for segment (km/h)",
    "Radius": "Curve radius (optional)",
    "CurveID": "Curve identifier (optional)",
    "X_Center": "Curve center X (optional)",
    "Y_Center": "Curve center Y (optional)"
}

# 🔧 메시지 포매터 함수
def format_error_message(error: ValidationError, prefix: str, descriptions: dict) -> str:

    messages = []

    if error.context:
        for sub_error in error.context:
            messages.append(format_error_message(sub_error, prefix, descriptions))
        return "\n".join(messages)

    if error.validator == 'required':
        missing_fields = [
            field for field in error.validator_value
            if field not in error.instance
        ]
        msg_lines = [f"{prefix} missing required fields:"]
        for f in missing_fields:
            desc = descriptions.get(f, "No description available")
            msg_lines.append(f"- {f}: {desc}")
        return "\n".join(msg_lines)

    elif error.validator == 'pattern':
        field = error.path[-1] if error.path else "Unknown field"
        expected = error.schema.get("pattern", "N/A")
        actual = error.instance
        desc = descriptions.get(field, "No description available")
        return (f"{prefix} invalid format in field '{field}': {desc}\n"
                f"- Expected pattern: {expected}\n"
                f"- Provided: {actual}")

    return f"{prefix} {error.message}"

# ✅ 검증 함수
def validate_train_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        validate(instance=data, schema=train_schema)
        return True, None
    except (json.JSONDecodeError, FileNotFoundError) as e:
        return False, f"File error: {str(e)}"
    except ValidationError as ve:
        return False, format_error_message(ve, "Train data validation failed:", TRAIN_FIELD_DESCRIPTIONS)

def validate_track_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key, segment in data.items():
            try:
                validate(instance=segment, schema=track_segment_schema)
            except ValidationError as ve:
                return False, format_error_message(ve, f"Track segment {key} validation failed:", TRACK_FIELD_DESCRIPTIONS)

        return True, None

    except (json.JSONDecodeError, FileNotFoundError) as e:
        return False, f"File error: {str(e)}"
