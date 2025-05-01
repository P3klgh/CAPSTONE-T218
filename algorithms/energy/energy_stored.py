# algorithms/energy/energy_stored.py

from configs.simulation_config import BRAKING_EFFICIENCY

def compute_stored_energy(e_regen_kwh: float) -> float:
    """
    회생 에너지 저장량을 계산합니다. (단위: kWh)

    Parameters:
        e_regen_kwh (float): 회생 에너지 (kWh)

    Returns:
        float: 저장된 에너지 (kWh)
    """
    if e_regen_kwh <= 0:
        return 0.0

    return round(e_regen_kwh * BRAKING_EFFICIENCY, 6)
