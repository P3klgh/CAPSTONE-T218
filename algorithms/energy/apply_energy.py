# algorithms/energy/apply_energy.py

from algorithms.energy.energy_regen import compute_regen_energy
from algorithms.energy.energy_stored import compute_stored_energy
from algorithms.energy.energy_total import compute_total_energy


def apply_energy_to_segment(entry: dict, mass_kg: float, time_step: float, brake_efficiency: float) -> None:
    """
    Applies energy calculations to a single simulation segment.

    Parameters:
        entry (dict): Track segment data (must contain acceleration, velocity, etc.)
        mass_kg (float): Total mass of the train [kg]
        time_step (float): Time step between segments [s]
        brake_efficiency (float): Brake efficiency (0~1)
    """
    # ✅ 필요한 값들을 entry에 추가해서 넘긴다
    entry["mass_kg"] = mass_kg
    entry["time_step"] = time_step

    # 1. Regen energy
    energy_regen = compute_regen_energy(entry)  # <- 수정된 호출 방식
    entry["E_regen_kWh"] = energy_regen

    # 2. Stored energy (scaled by brake efficiency)
    energy_stored = compute_stored_energy(energy_regen, brake_efficiency)
    entry["E_stored_kWh"] = energy_stored

    # 3. Total energy (accumulation will be handled in energy_total)
    entry["E_total_kWh"] = compute_total_energy(energy_regen, energy_stored)
