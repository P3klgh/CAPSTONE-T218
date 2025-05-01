import os
import json

from algorithms.kinematics import apply_kinematics_to_segment
from configs.simulation_config import (
    TIME_STEP_SECONDS,
    INITIAL_RPM,
    INITIAL_VELOCITY_KPH,
    TRANSMISSION_EFFICIENCY
)
from algorithms.traction_util.engine_power_dispatcher import get_p_engine_from_speed
from utils.mass_utils import compute_total_train_mass  # ✅ 질량 유틸 가져오기

def apply_kinematics_to_simulation(sim_file_path: str, train_spec_path: str) -> None:
    """
    Applies kinematic updates to each time step in the simulation JSON file.

    Args:
        sim_file_path (str): Path to the simulation track JSON file.
        train_spec_path (str): Path to the train specification JSON file.
    """
    if not os.path.exists(sim_file_path) or not os.path.exists(train_spec_path):
        print("❌ One or more input files not found.")
        return

    with open(sim_file_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)

    with open(train_spec_path, "r", encoding="utf-8") as f:
        train_spec = json.load(f)

    total_mass_kg = compute_total_train_mass(train_spec)  # ✅ 여기서 자동 계산

    sorted_fids = sorted(sim_data.keys(), key=lambda k: float(k))

    for fid in sorted_fids:
        segment = sim_data[fid]

        # ✅ velocity_mps 값이 없을 때만 초기값을 설정
        if "velocity_mps" not in segment:
            current_velocity_mps = INITIAL_VELOCITY_KPH / 3.6
            segment["velocity_mps"] = current_velocity_mps
            segment["velocity_kph"] = INITIAL_VELOCITY_KPH
            print(f"⚠️ FID {fid}: velocity 없음 → 초기값({INITIAL_VELOCITY_KPH} km/h)으로 설정.")
        else:
            current_velocity_mps = segment["velocity_mps"]

        # 엔진 출력 계산
        p_engine = get_p_engine_from_speed(current_velocity_mps * 3.6,train_spec)
        segment["P_engine_kw"] = p_engine

        # 운동학 알고리즘 적용
        next_velocity = apply_kinematics_to_segment(
            segment,
            total_mass_kg,
            train_spec
        )

        # 결과 저장
        segment["velocity_mps"] = next_velocity
        segment["velocity_kph"] = next_velocity * 3.6

    with open(sim_file_path, "w", encoding="utf-8") as f:
        json.dump(sim_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Kinematics applied and saved to: {sim_file_path}")


# 🧪 실행 예제
if __name__ == "__main__":
    dataset = "Lucinda"
    sim_path = f"../../algorithms/simulation_results/final_simulation({dataset}).json"
    train_spec_path = "../../given_data/train_spec.json"

    apply_kinematics_to_simulation(sim_path, train_spec_path)
