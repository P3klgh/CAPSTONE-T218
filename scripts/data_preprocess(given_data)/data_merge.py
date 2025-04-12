import json
import os

# 기본 폴더 설정
base_dir = "../../given_data/extracted_processed_json"

# 파일 경로 설정 (Lucinda & Karloo)
data_files = {
    "Lucinda": {
        "curve_radii": os.path.join(base_dir, "HBTSugarLineLucindaCurveRadii_full.json"),
        "grade25m": os.path.join(base_dir, "HBTSugarLineLucindaGrade25m_full.json"),
        "grade_full": os.path.join(base_dir, "HBTSugarLineLucindaGrade_full.json"),
        "output": os.path.join(base_dir, "final_merged(Lucinda).json")
    },
    "Karloo": {
        "curve_radii": os.path.join(base_dir, "PCK2KarlooCurveRadii_full.json"),
        "grade25m": os.path.join(base_dir, "PCK2KarlooGrade25m_full.json"),
        "grade_full": os.path.join(base_dir, "PCK2KarlooGrade_full.json"),
        "output": os.path.join(base_dir, "final_merged(Karloo).json")
    }
}

# JSON 데이터 불러오기
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 데이터 병합 함수 (null 기본값 포함)
def merge_data(files_dict):
    curve_radii_data = load_json(files_dict["curve_radii"])
    grade25m_data = load_json(files_dict["grade25m"])
    grade_full_data = load_json(files_dict["grade_full"])

    merged_data = {}

    # ✅ Step 1: curve_radii 먼저 병합 (있으면 우선)
    for entry in curve_radii_data:
        fid = entry["FID"]
        merged_data[fid] = {
            "Radius": entry.get("Radius"),
            "CurveID": entry.get("CurveID"),
            "X_Center": entry.get("X_Center"),
            "Y_Center": entry.get("Y_Center"),
        }

    # ✅ Step 2: slope25m 병합
    for entry in grade25m_data:
        fid = entry["FID"]
        merged_data.setdefault(fid, {}).update({
            "Min_Slope": entry.get("Min_Slope"),
            "Max_Slope": entry.get("Max_Slope"),
            "Avg_Slope": entry.get("Avg_Slope"),
        })

    # ✅ Step 3: grade_full 병합
    for entry in grade_full_data:
        fid = entry["FID"]
        merged_data.setdefault(fid, {}).update({
            "Length": entry.get("Length"),
            "Z_Min": entry.get("Z_Min"),
            "Z_Max": entry.get("Z_Max"),
            "Z_Mean": entry.get("Z_Mean"),
            "XStart": entry.get("XStart"),
            "YStart": entry.get("YStart"),
            "XFinish": entry.get("XFinish"),
            "YFinish": entry.get("YFinish"),
        })

    # ✅ Step 4: 누락된 곡선 필드에 기본값(None) 추가
    for fid, entry in merged_data.items():
        entry.setdefault("Radius", None)
        entry.setdefault("CurveID", None)
        entry.setdefault("X_Center", None)
        entry.setdefault("Y_Center", None)

    return merged_data

# 각 데이터셋 병합 및 저장
for dataset_name, files_dict in data_files.items():
    merged_data = merge_data(files_dict)
    output_file = files_dict["output"]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=4)

    print(f"✅ 병합 완료 ({dataset_name}): {output_file}")
