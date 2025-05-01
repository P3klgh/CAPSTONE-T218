# scripts/apply_simulation/simulation_repeater.py

import os
import json

from scripts.apply_simulation.apply_resistance_to_simulation import apply_resistance_to_simulation
from scripts.apply_simulation.apply_kinematics_to_simulation import apply_kinematics_to_simulation
from utils.mass_utils import compute_total_train_mass
from utils.davis_utils import get_davis_constants




# 🔧 사용자 설정값
DATASET_NAME = "Lucinda"
SIM_PATH = f"../../algorithms/simulation_results/final_simulation({DATASET_NAME}).json"
TRAIN_SPEC_PATH = "../../given_data/train_spec.json"
NUM_ITERATIONS = 3


def run_simulation_repeater(sim_path: str, train_spec_path: str, iterations: int = 3) -> None:
    # ✅ 경로 확인
    if not os.path.exists(sim_path):
        print(f"❌ 시뮬레이션 파일 없음: {sim_path}")
        return
    if not os.path.exists(train_spec_path):
        print(f"❌ 기차 스펙 파일 없음: {train_spec_path}")
        return

    # ✅ 사전 준비: 질량 및 Davis 상수 계산
    with open(train_spec_path, "r", encoding="utf-8") as f:
        train_spec = json.load(f)

    total_mass_kg = compute_total_train_mass(train_spec)
    a, b, c = get_davis_constants(train_spec_path)

    # ✅ 반복 수행
    for i in range(iterations):
        print(f"🔁 반복 {i+1} / {iterations}")
        apply_resistance_to_simulation(sim_path, total_mass_kg, a, b, c)
        apply_kinematics_to_simulation(sim_path, train_spec_path)

    print(f"✅ 총 {iterations}회 반복 완료")


# 🧪 단독 실행용
if __name__ == "__main__":
    run_simulation_repeater(SIM_PATH, TRAIN_SPEC_PATH, NUM_ITERATIONS)
