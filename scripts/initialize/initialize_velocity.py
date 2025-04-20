import os
import json
from configs.simulation_config import INITIAL_VELOCITY_KPH

def initialize_velocity(simulation_file_path: str) -> None:
    """
    시뮬레이션 데이터에 초기 속도를 모든 구간에 설정합니다.
    초기 속도는 configs/simulation_config.py의 INITIAL_VELOCITY_KPH에서 가져옵니다.

    Parameters:
        simulation_file_path (str): JSON 파일 경로
    """
    if not os.path.exists(simulation_file_path):
        print(f"❌ Error: File not found: {simulation_file_path}")
        return

    with open(simulation_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for fid, entry in data.items():
        entry["velocity_kph"] = INITIAL_VELOCITY_KPH
        entry["velocity_mps"] = INITIAL_VELOCITY_KPH / 3.6

    with open(simulation_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"✅ Initial velocity set to {INITIAL_VELOCITY_KPH} km/h for all segments in: {simulation_file_path}")


# 🧪 예제 실행
if __name__ == "__main__":
    dataset_name = "Lucinda"
    json_path = f"../../algorithms/simulation_results/final_simulation({dataset_name}).json"

    initialize_velocity(json_path)
