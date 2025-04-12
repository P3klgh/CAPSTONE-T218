import os
import json
from configs.simulation_config import INITIAL_RPM

def initialize_rpm(simulation_file_path: str) -> None:
    """
    시뮬레이션 데이터에 초기 RPM 값을 모든 구간에 설정합니다.
    """
    if not os.path.exists(simulation_file_path):
        print(f"❌ Error: File not found: {simulation_file_path}")
        return

    with open(simulation_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for fid, entry in data.items():
        entry["rpm"] = INITIAL_RPM

    with open(simulation_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"✅ Initial RPM set to {INITIAL_RPM} for all segments in: {simulation_file_path}")


# 🧪 예제 실행
if __name__ == "__main__":
    dataset_name = "Lucinda"
    json_path = f"../../algorithms/simulation_results/final_simulation({dataset_name}).json"
    initialize_rpm(json_path)
