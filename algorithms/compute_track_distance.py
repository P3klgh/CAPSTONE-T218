import os
import json
import math


def compute_distance(x1, y1, x2, y2):
    """Euclidean distance 계산 함수"""
    if None in (x1, y1, x2, y2):
        return None
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def compute_track_distances(input_file: str, output_file: str) -> None:
    """트랙의 d_xy (2D 거리) 계산 및 저장"""

    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found: {input_file}")
        return

    # ✅ 입력 데이터 로드
    with open(input_file, "r", encoding="utf-8") as file:
        input_data = json.load(file)

    # ✅ 기존 결과가 있으면 불러오기
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    else:
        existing_data = {}

    # ✅ 거리 계산 및 병합
    for fid, entry in input_data.items():
        x_start = entry.get("XStart")
        y_start = entry.get("YStart")
        x_end = entry.get("XFinish")
        y_end = entry.get("YFinish")

        d_xy = compute_distance(x_start, y_start, x_end, y_end)

        if d_xy is None:
            print(f"⚠️ Warning: Missing coordinates for FID {fid}, setting d_xy = None")

        entry["d_xy"] = d_xy  # 거리 값 추가

        # 기존 데이터에 병합
        if fid in existing_data:
            existing_data[fid].update(entry)
        else:
            existing_data[fid] = entry

    # ✅ 결과 저장
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(existing_data, outfile, indent=4, ensure_ascii=False)

    print(f"✅ Track distances computed and saved to: {output_file}")


# 🧪 단독 실행 시 테스트 가능
if __name__ == "__main__":
    dataset_name = "Lucinda"
    input_path = f"../given_data/extracted_processed_json/final_merged({dataset_name}).json"
    output_path = f"../algorithms/simulation_results/final_simulation({dataset_name}).json"
    compute_track_distances(input_path, output_path)
