import os
import json
import math
from typing import Tuple

# --------------------------------------
# 📐 유틸리티 함수: 2D 거리 계산
# --------------------------------------
def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# --------------------------------------
# 1️⃣ 곡률 반지름 계산 (2D 기준)
# --------------------------------------
def compute_radius_2d(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float | None:
    a = distance_2d(*p2, *p3)
    b = distance_2d(*p1, *p3)
    c = distance_2d(*p1, *p2)

    s = (a + b + c) / 2
    area_sq = s * (s - a) * (s - b) * (s - c)
    area = math.sqrt(max(area_sq, 0))  # 음수 방지

    if area == 0:
        return None  # 반환할 수 없는 경우

    radius = (a * b * c) / (4 * area)
    return radius

# --------------------------------------
# 2️⃣ 곡률 계산 (κ = 1 / R)
# --------------------------------------
def compute_curvature(radius: float | None) -> float:
    if radius is None or radius == 0 or math.isinf(radius):
        return 0.0
    return 1 / radius

# --------------------------------------
# 3️⃣ 전체 곡률 계산 및 JSON 저장
# --------------------------------------
def compute_curvatures_for_all_segments(simulation_file_path: str) -> None:
    if not os.path.exists(simulation_file_path):
        print(f"❌ File not found: {simulation_file_path}")
        return

    with open(simulation_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sorted_fids = sorted(data.keys(), key=lambda k: float(k))

    for i in range(1, len(sorted_fids) - 1):
        fid_prev = sorted_fids[i - 1]
        fid_curr = sorted_fids[i]
        fid_next = sorted_fids[i + 1]

        def extract_xy(fid):
            entry = data[fid]
            return entry.get("XFinish"), entry.get("YFinish")

        p1 = extract_xy(fid_prev)
        p2 = extract_xy(fid_curr)
        p3 = extract_xy(fid_next)

        if None in p1 or None in p2 or None in p3:
            continue

        radius = compute_radius_2d(p1, p2, p3)
        kappa = compute_curvature(radius)

        # JSON에 저장 가능한 값으로 처리
        data[fid_curr]["curvature_radius"] = radius if radius is not None else None
        data[fid_curr]["curvature_kappa"] = kappa

    with open(simulation_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ 곡률 계산 완료 및 저장됨: {simulation_file_path}")

# 🧪 단독 실행
if __name__ == "__main__":
    dataset_name = "Lucinda"
    file_path = f"../algorithms/simulation_results/final_simulation({dataset_name}).json"
    compute_curvatures_for_all_segments(file_path)
