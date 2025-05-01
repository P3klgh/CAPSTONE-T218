# scripts/main_simulation.py

import os
import json
import sys

# ✅ 절대 경로 기반 루트 설정 (가장 중요)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SIM_RESULT_DIR = os.path.join(BASE_DIR, "algorithms", "simulation_results")
TRAIN_SPEC_PATH = os.path.join(BASE_DIR, "given_data", "train_spec.json")

from algorithms import (
    compute_gradients_for_simulation,
    compute_cumulative_distance,
    compute_curvatures_for_all_segments,
    compute_track_distances
)

from scripts.data_preprocess.data_merge import merge_data, data_files
from scripts.initialize.initialize_velocity import initialize_velocity
from scripts.apply_simulation.simulation_repeater import run_simulation_repeater
from scripts.apply_simulation.apply_energy_to_simulation import main as run_energy
from configs import simulation_config

simulation_config.USE_SPEED_LIMIT = True  # ✅ 상한선 적용 강제

# ✅ 기본 설정값
DEFAULT_DATASET = "Lucinda"
DEFAULT_NUM_ITERATIONS = 3

def run_full_simulation(dataset_name=DEFAULT_DATASET, num_iterations=DEFAULT_NUM_ITERATIONS):
    print(f"\n🔧 [1] 데이터 병합 시작... ({dataset_name})")
    if dataset_name not in data_files:
        print(f"❌ 오류: 지원되지 않는 데이터셋 이름: {dataset_name}")
        return

    merged = merge_data(data_files[dataset_name])
    merged_output_path = data_files[dataset_name]["output"]
    os.makedirs(os.path.dirname(merged_output_path), exist_ok=True)

    with open(merged_output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4)
    print(f"✅ 병합 완료 및 저장: {merged_output_path}")

    # ✅ 시뮬레이션 결과 파일 경로 준비 (절대 경로)
    sim_path = os.path.join(SIM_RESULT_DIR, f"final_simulation({dataset_name}).json")

    # 🔁 순차적으로 알고리즘 실행
    print("\n📏 [1-1] 트랙 거리 계산")
    compute_track_distances(merged_output_path, sim_path)

    print("\n📈 [1-2] 누적 거리 계산")
    compute_cumulative_distance(sim_path)

    print("\n📐 [1-3] 경사도(a_slope) 계산")
    compute_gradients_for_simulation(sim_path)

    print("\n🔄 [1-4] 곡률(curvature) 계산")
    compute_curvatures_for_all_segments(sim_path)

    print("\n🚦 [2] 초기 속도 설정")
    initialize_velocity(sim_path)

    print("\n🔁 [3] 반복 알고리즘 실행")
    run_simulation_repeater(sim_path, TRAIN_SPEC_PATH, num_iterations)

    print("\n⚡ [4] 에너지 계산")
    run_energy(sim_path)

    print("\n✅ 전체 시뮬레이션 완료")

# ✅ CLI 단독 실행 시
if __name__ == "__main__":
    dataset = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATASET
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_NUM_ITERATIONS

    run_full_simulation(dataset_name=dataset, num_iterations=iterations)
