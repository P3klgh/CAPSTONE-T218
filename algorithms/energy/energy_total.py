# algorithms/energy/energy_total.py

def compute_total_energy(sim_data: dict) -> dict:
    """
    Accumulates total regenerative and stored energy from all segments.

    Parameters:
        sim_data (dict): Simulation data with energy info per segment.

    Returns:
        dict: {
            "total_energy_regen_kWh": float,
            "total_energy_stored_kWh": float
        }
    """
    total_regen = 0.0
    total_stored = 0.0

    for segment in sim_data.values():
        total_regen += segment.get("energy_regen_kWh", 0.0)
        total_stored += segment.get("energy_stored_kWh", 0.0)

    return {
        "total_energy_regen_kWh": round(total_regen, 3),
        "total_energy_stored_kWh": round(total_stored, 3)
    }
