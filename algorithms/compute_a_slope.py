import os
import json
import math


def compute_delta_z(z_start: float, z_end: float) -> float:
    """Z축 고도차 (ΔZ) 계산"""
    return z_end - z_start


def compute_slope_gradient(delta_z: float, d_xy: float) -> float:
    """경사율 (ΔZ / d_xy) 계산"""
    if d_xy == 0:
        return None
    return delta_z / d_xy


def compute_a_slope_from_gradient(slope_gradient: float) -> float:
    """arctan 기반 경사각 계산 (라디안)"""
    try:
        return math.atan(slope_gradient)
    except (TypeError, ValueError):
        return None


def compute_gradients_for_simulation(simulation_file_path: str) -> None:
    """
    시뮬레이션 파일의 각 구간에 대해 ΔZ, slope_gradient, a_slope를 계산하여 저장합니다.
    """

    if not os.path.exists(simulation_file_path):
        print(f"❌ Error: Simulation file not found: {simulation_file_path}")
        return

    with open(simulation_file_path, "r", encoding="utf-8") as file:
        simulation_data = json.load(file)

    for fid, entry in simulation_data.items():
        z_min = entry.get("Z_Min")
        z_max = entry.get("Z_Max")
        d_xy = entry.get("d_xy")

        if None in (z_min, z_max, d_xy):
            print(f"⚠️ Warning: Missing Z or d_xy data for FID {fid}, skipping.")
            simulation_data[fid]["delta_z"] = None
            simulation_data[fid]["slope_gradient"] = None
            simulation_data[fid]["a_slope"] = None
            continue

        delta_z = compute_delta_z(z_min, z_max)
        slope_gradient = compute_slope_gradient(delta_z, d_xy)
        a_slope = compute_a_slope_from_gradient(slope_gradient)

        simulation_data[fid]["delta_z"] = delta_z
        simulation_data[fid]["slope_gradient"] = slope_gradient
        simulation_data[fid]["a_slope"] = a_slope

    with open(simulation_file_path, "w", encoding="utf-8") as outfile:
        json.dump(simulation_data, outfile, indent=4, ensure_ascii=False)

    print(f"✅ ΔZ, slope_gradient, a_slope 계산 완료 및 저장됨: {simulation_file_path}")


# 🧪 단독 실행 예제
if __name__ == "__main__":
    dataset_name = "Lucinda"
    simulation_file = f"../algorithms/simulation_results/final_simulation({dataset_name}).json"
    compute_gradients_for_simulation(simulation_file)
