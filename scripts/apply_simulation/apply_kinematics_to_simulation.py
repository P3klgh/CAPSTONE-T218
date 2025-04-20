# apply_kinematics_to_simulation.py
import os
import json


from algorithms.kinematics import apply_kinematics_to_segment
from configs.simulation_config import (
    TIME_STEP_SECONDS,
    INITIAL_RPM,
    INITIAL_VELOCITY_KPH,
    TRANSMISSION_EFFICIENCY
)
from algorithms.traction_util.engine_power_dispatcher import get_p_engine

def apply_kinematics_to_simulation(sim_file_path: str, train_spec_path: str, total_mass_kg: float) -> None:
    """
    Applies kinematic updates to each time step in the simulation JSON file.

    Args:
        sim_file_path (str): Path to the simulation track JSON file.
        train_spec_path (str): Path to the train specification JSON file.
        total_mass_kg (float): Total mass of the train in kg.
    """
    if not os.path.exists(sim_file_path) or not os.path.exists(train_spec_path):
        print("❌ One or more input files not found.")
        return

    with open(sim_file_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)

    with open(train_spec_path, "r", encoding="utf-8") as f:
        train_spec = json.load(f)

    sorted_fids = sorted(sim_data.keys(), key=lambda k: float(k))
    current_velocity_mps = INITIAL_VELOCITY_KPH / 3.6  # Convert km/h to m/s

    for fid in sorted_fids:
        segment = sim_data[fid]

        # 엔진 출력 계산
        p_engine = get_p_engine(current_velocity_mps * 3.6, INITIAL_RPM, train_spec)
        segment["P_engine_kw"] = p_engine

        # 전체 저항력
        r_total = segment.get("R_total", 0)

        # 다음 속도 계산
        next_velocity = apply_kinematics_to_segment(
            segment,  # entry = 현재 구간 데이터
            total_mass_kg,
            train_spec
        )

        segment["velocity_mps"] = next_velocity
        segment["velocity_kph"] = next_velocity * 3.6

        current_velocity_mps = next_velocity  # 다음 구간 계산에 반영

    with open(sim_file_path, "w", encoding="utf-8") as f:
        json.dump(sim_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Kinematics applied and saved to: {sim_file_path}")


# 🧪 예제 실행
if __name__ == "__main__":
    dataset = "Lucinda"
    sim_path = f"../../algorithms/simulation_results/final_simulation({dataset}).json"
    train_spec_path = "../../given_data/train_spec.json"
    total_train_mass_kg = 195000

    apply_kinematics_to_simulation(sim_path, train_spec_path, total_train_mass_kg)
