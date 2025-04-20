# algorithms/energy/energy_regen.py

from configs.simulation_config import BRAKING_EFFICIENCY

def compute_regen_energy(entry: dict) -> float:
    """
    Computes regenerative energy [kWh] for a given simulation segment.

    Requirements in entry:
        - mass_kg (float): total train mass in kg
        - velocity_mps (float): speed at the segment in m/s
        - acceleration (float): acceleration (should be < 0 for braking)
        - time_step (float): time duration in seconds (optional fallback: 1s)

    Returns:
        float: regenerative energy in kilowatt-hours (kWh)
    """
    mass_kg = entry.get("mass_kg")
    velocity_mps = entry.get("velocity_mps", 0)
    acceleration = entry.get("acceleration", 0)
    time_step = entry.get("time_step", 1.0)  # fallback if not set

    if acceleration >= 0:
        return 0.0

    delta_ke_joules = -mass_kg * acceleration * velocity_mps * time_step
    delta_ke_kwh = (delta_ke_joules / 3_600_000) * BRAKING_EFFICIENCY

    return round(delta_ke_kwh, 6)
