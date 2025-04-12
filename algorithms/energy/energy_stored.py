# algorithms/energy/energy_stored.py

def compute_stored_energy(e_regen_kwh: float, efficiency: float = 0.95) -> float:
    """
    회생 에너지 저장량을 계산합니다.

    Parameters:
        e_regen_kwh (float): 회생 에너지 (kWh)
        efficiency (float): 저장 효율 (기본값: 0.95)

    Returns:
        float: 저장된 에너지 (kWh)
    """
    if e_regen_kwh < 0:
        raise ValueError("❌ 회생 에너지는 음수일 수 없습니다.")

    return e_regen_kwh * efficiency
