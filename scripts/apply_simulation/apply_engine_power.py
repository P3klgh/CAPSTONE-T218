import os
import json
from configs.simulation_config import INITIAL_RPM
from algorithms.traction_util.engine_power_dispatcher import get_p_engine

def apply_engine_power_to_simulation(simulation_file_path: str, train_spec_path: str) -> None:
    if not os.path.exists(simulation_file_path) or not os.path.exists(train_spec_path):
        print("❌ 파일 경로를 확인하세요.")
        return

    with open(simulation_file_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)

    with open(train_spec_path, "r", encoding="utf-8") as f:
        train_spec = json.load(f)

    for fid, entry in sim_data.items():
        v_kph = entry.get("velocity_kph", 0)
        p_engine = get_p_engine(v_kph, INITIAL_RPM, train_spec)
        entry["P_engine_kw"] = p_engine

    with open(simulation_file_path, "w", encoding="utf-8") as f:
        json.dump(sim_data, f, indent=4, ensure_ascii=False)

    print(f"✅ P_engine 계산 완료 및 저장됨: {simulation_file_path}")

# 🧪 실행 예제
if __name__ == "__main__":
    dataset_name = "Lucinda"
    sim_path = f"../../algorithms/simulation_results/final_simulation({dataset_name}).json"
    train_spec_path = "../../given_data/train_spec.json"

    apply_engine_power_to_simulation(sim_path, train_spec_path)
