import os
import json


def compute_cumulative_distance(simulation_file_path: str) -> None:
    """
    시뮬레이션 파일에서 각 구간의 d_xy를 기반으로 누적 거리를 계산해
    cumulative_distance 필드에 저장합니다.
    """

    if not os.path.exists(simulation_file_path):
        print(f"❌ Error: Simulation file not found: {simulation_file_path}")
        return

    # ✅ 시뮬레이션 데이터 로드
    with open(simulation_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # ✅ FID 정렬 (문자열이므로 float 변환 후 정렬)
    sorted_fids = sorted(data.keys(), key=lambda x: float(x))

    cumulative = 0
    for fid in sorted_fids:
        d_xy = data[fid].get("d_xy")

        if d_xy is None:
            print(f"⚠️ Warning: Missing d_xy for FID {fid}, setting cumulative_distance = None")
            data[fid]["cumulative_distance"] = None
            continue

        data[fid]["cumulative_distance"] = cumulative
        cumulative += d_xy

    # ✅ 계산된 데이터 저장
    with open(simulation_file_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

    print(f"✅ 누적 거리(cumulative_distance) 계산 완료 및 저장됨: {simulation_file_path}")

if __name__ == "__main__":
    dataset_name = "Lucinda"
    simulation_file = f"../algorithms/simulation_results/final_simulation({dataset_name}).json"
    compute_cumulative_distance(simulation_file)