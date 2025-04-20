# algorithms/kinematics/tractive_force.py

from typing import Optional


def compute_tractive_force(p_engine_kw: float, velocity_mps: float, efficiency: float = 0.85) -> Optional[float]:
    """
    Calculates tractive force (F_tractive) in Newtons.

    Formula:
        F_tractive = (P_engine * 1000) / (velocity * efficiency)

    Parameters:
        p_engine_kw (float): Engine power in kilowatts (kW)
        velocity_mps (float): Train speed in meters per second (m/s)
        efficiency (float): Transmission efficiency (default: 0.85)

    Returns:
        float: Tractive force in Newtons (N), or None if velocity is zero
    """
    if velocity_mps == 0:
        return None  # 정지 상태에서는 무한대가 되므로 None 반환

    return (p_engine_kw * 1000) / (velocity_mps * efficiency)
