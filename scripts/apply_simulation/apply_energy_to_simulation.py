# scripts/apply_simulation/apply_energy_to_simulation.py

import os
import json

from algorithms.energy.apply_energy import apply_energy_to_simulation

def main(sim_path):
    # ✅ 경로 확인
    if not os.path.exists(sim_path):
        print(f"❌ 파일 없음: {sim_path}")
        return

    # ✅ 파일 로드
    with open(sim_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)

    # ✅ 에너지 계산 실행
    updated_data = apply_energy_to_simulation(sim_data)

    # ✅ 결과 저장
    with open(sim_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)

    print(f"✅ 에너지 계산 완료 및 저장됨: {sim_path}")


# 🧪 단독 실행 시 기본 경로 지정
if __name__ == "__main__":
    DATASET_NAME = "Lucinda"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    default_sim_path = os.path.join(BASE_DIR, "algorithms", "simulation_results", f"final_simulation({DATASET_NAME}).json")
    main(default_sim_path)
