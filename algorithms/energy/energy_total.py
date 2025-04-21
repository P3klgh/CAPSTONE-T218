# algorithms/energy/energy_total.py

def compute_energy_total(prev_force: float, curr_force: float, distance_m: float) -> float:
    """
    세그먼트별 견인력 기반 총 에너지 소비량 계산 (단위: J)

    E_total = ((T_i + T_f) / 2) × d

    Parameters:
        prev_force (float): 이전 세그먼트의 견인력 (N)
        curr_force (float): 현재 세그먼트의 견인력 (N)
        distance_m (float): 세그먼트 거리 (m)

    Returns:
        float: 에너지 소비량 (줄, J)
    """
    avg_force = (prev_force + curr_force) / 2
    return avg_force * distance_m


def compute_total_energy(sim_data: dict) -> dict:
    """
    전체 회생 에너지 및 저장 에너지의 합산 (단위: kWh)

    Parameters:
        sim_data (dict): 시뮬레이션 데이터 (세그먼트별 딕셔너리)

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
