import os
import json
from algorithms.resistance.davis_resistance import compute_davis_resistance
from algorithms.resistance.slope_resistance import compute_slope_resistance
from algorithms.resistance.curve_resistance import compute_curve_resistance
from algorithms.resistance.total_resistance import compute_total_resistance

from utils.mass_utils import compute_total_train_mass       # ✅ 질량 계산 함수 import
from utils.davis_utils import get_davis_constants           # ✅ Davis 상수 불러오기

def apply_resistance_to_simulation(simulation_file_path: str, train_mass_kg: float, a: float, b: float, c: float) -> None:
    if not os.path.exists(simulation_file_path):
        print(f"❌ Error: File not found: {simulation_file_path}")
        return

    with open(simulation_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for fid, entry in data.items():
        v_kph = entry.get("velocity_kph")
        v_mps = (v_kph or 0) / 3.6
        a_slope = entry.get("a_slope")
        r_curve_val = entry.get("curvature_radius")

        # ✅ mass_kg 각 세그먼트에 저장
        entry["mass_kg"] = train_mass_kg
        mass_ton = train_mass_kg / 1000  # 🔥 여기 추가

        r_davis_per_ton = compute_davis_resistance(v_mps, a, b, c)
        r_davis = r_davis_per_ton * mass_ton  # 🔥 여기 핵심 수정
        r_slope = compute_slope_resistance(train_mass_kg, a_slope)
        r_curve = compute_curve_resistance(train_mass_kg, v_mps, r_curve_val, a_slope)
        r_total = compute_total_resistance(r_davis, r_slope, r_curve)

        entry["R_davis"] = r_davis
        entry["R_slope"] = r_slope
        entry["R_curve"] = r_curve
        entry["R_total"] = r_total



    with open(simulation_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"✅ Resistance calculation completed and saved to: {simulation_file_path}")


# 🧪 실행 예제
if __name__ == "__main__":
    dataset = "Lucinda"
    sim_path = f"../../algorithms/simulation_results/final_simulation({dataset}).json"
    spec_path = "../../given_data/train_spec.json"

    # ✅ train_spec에서 질량 계산
    with open(spec_path, "r", encoding="utf-8") as f:
        train_spec = json.load(f)
    total_train_mass_kg = compute_total_train_mass(train_spec)

    # ✅ Davis 상수 유틸로 가져오기
    A, B, C = get_davis_constants()

    apply_resistance_to_simulation(sim_path, total_train_mass_kg, A, B, C)
