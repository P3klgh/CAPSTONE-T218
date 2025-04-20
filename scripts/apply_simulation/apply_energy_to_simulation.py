# scripts/apply_simulation/apply_energy_to_simulation.py

import os
import json
from algorithms.energy import apply_energy_to_segment
from configs.simulation_config import TIME_STEP_SECONDS, BRAKING_EFFICIENCY

def apply_energy_to_simulation(sim_file_path: str, total_mass_kg: float) -> None:
    """
    Applies energy-related calculations to each segment in the simulation data.

    Parameters:
        sim_file_path (str): Path to the simulation JSON file.
        total_mass_kg (float): Total train mass in kilograms.
    """
    if not os.path.exists(sim_file_path):
        print(f"❌ File not found: {sim_file_path}")
        return

    with open(sim_file_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)

    for fid, segment in sim_data.items():
        apply_energy_to_segment(
            segment,
            mass_kg=total_mass_kg,
            time_step=TIME_STEP_SECONDS,
            brake_efficiency=BRAKING_EFFICIENCY
        )

    with open(sim_file_path, "w", encoding="utf-8") as f:
        json.dump(sim_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Energy computations applied and saved to: {sim_file_path}")


# 🧪 예제 실행
if __name__ == "__main__":
    dataset = "Lucinda"
    sim_path = f"../../algorithms/simulation_results/final_simulation({dataset}).json"
    total_train_mass_kg = 195000  # 또는 외부에서 불러오도록 수정 가능

    apply_energy_to_simulation(sim_path, total_train_mass_kg)
