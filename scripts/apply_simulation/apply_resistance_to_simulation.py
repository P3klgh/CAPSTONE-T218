import os
import json
from algorithms.resistance.davis_resistance import compute_davis_resistance
from algorithms.resistance.slope_resistance import compute_slope_resistance
from algorithms.resistance.curve_resistance import compute_curve_resistance
from algorithms.resistance.total_resistance import compute_total_resistance

def apply_resistance_to_simulation(simulation_file_path: str, train_mass_kg: float, a: float, b: float, c: float) -> None:
    """
    주어진 시뮬레이션 트랙 데이터에 각 구간별 저항력을 계산하여 저장

    Parameters:
        simulation_file_path (str): JSON 파일 경로
        train_mass_kg (float): 전체 기차 질량 [kg]
        a (float): Davis equation constant A
        b (float): Davis equation constant B
        c (float): Davis equation constant C
    """
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

        r_davis = compute_davis_resistance(a, b, c, v_mps)
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


if __name__ == "__main__":
    json_path = "../../algorithms/simulation_results/final_simulation(Lucinda).json"
    total_train_mass_kg = 195000  # 실제 입력에 맞게 조정
    A, B, C = 5000, 400, 30       # 예시 값

    apply_resistance_to_simulation(json_path, total_train_mass_kg, A, B, C)
