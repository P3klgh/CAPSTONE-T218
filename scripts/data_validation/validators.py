import json
import fastjsonschema
from fastjsonschema import JsonSchemaException
from concurrent.futures import ThreadPoolExecutor
from .validation_schemas import train_schema, track_segment_schema

# 🔧 스키마 컴파일
validate_train_schema = fastjsonschema.compile(train_schema)
validate_track_segment_schema = fastjsonschema.compile(track_segment_schema)

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

# 🔧 간단한 에러 메시지 생성기
def format_error_message(error_msg: str, prefix: str, descriptions: dict) -> str:
    return f"{prefix} {error_msg}"

# ✅ Train JSON 검증 함수
def validate_train_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        validate_train_schema(data)
        return True, None
    except (json.JSONDecodeError, FileNotFoundError) as e:
        return False, f"File error: {str(e)}"
    except JsonSchemaException as ve:
        return False, format_error_message(ve.message, "Train data validation failed:", TRAIN_FIELD_DESCRIPTIONS)

# 🔄 병렬 처리용 세그먼트 검증 함수
def validate_segment_pair(pair):
    key, segment = pair
    try:
        validate_track_segment_schema(segment)
        return None
    except JsonSchemaException as ve:
        return f"Track segment {key} validation failed: {ve.message}"

# ✅ Track JSON 검증 (병렬 버전)
def validate_track_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(validate_segment_pair, data.items()))

        errors = [msg for msg in results if msg]
        if errors:
            return False, "\n".join(errors)
        return True, None

    except (json.JSONDecodeError, FileNotFoundError) as e:
        return False, f"File error: {str(e)}"
