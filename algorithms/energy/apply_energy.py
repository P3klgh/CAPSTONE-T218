# algorithms/energy/apply_energy.py


from algorithms.energy.energy_total import compute_energy_total
from algorithms.energy.energy_regen import compute_regen_energy
from algorithms.energy.energy_stored import compute_stored_energy

def apply_energy_to_simulation(sim_data: dict) -> dict:
    """
    Applies energy calculations (E_total, E_regen, E_stored) to all segments.

    Parameters:
        sim_data (dict): 시뮬레이션 세그먼트 데이터

    Returns:
        dict: 업데이트된 시뮬레이션 데이터
    """
    sorted_fids = sorted(sim_data.keys(), key=lambda k: float(k))
    prev_force = None

    for i, fid in enumerate(sorted_fids):
        segment = sim_data[fid]
        distance = segment.get("d_xy", 0)

        # 🔋 1. 소비 에너지 계산 (E_total)
        curr_force = segment.get("R_total", 0)
        if prev_force is None:
            prev_force = curr_force  # 첫 세그먼트는 자기 힘만 씀

        e_total_j = compute_energy_total(prev_force, curr_force, distance)
        e_total_kwh = e_total_j / 3_600_000
        segment["energy_total_kWh"] = round(e_total_kwh, 6)

        # 🔄 2. 회생 에너지 계산 (운동 에너지 감소 기반)
        regen_kwh = compute_regen_energy(segment)
        segment["energy_regen_kWh"] = regen_kwh

        # 🔐 3. 저장 에너지 계산
        stored_kwh = compute_stored_energy(regen_kwh)
        segment["energy_stored_kWh"] = stored_kwh

        # 다음 루프용으로 저장
        prev_force = curr_force

    return sim_data
