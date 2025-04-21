# traction_util/engine_power_dispatcher.py

from typing import Dict
from .tractive_effort_curve import interpolate_tractive_effort

def get_p_engine_from_speed(speed_kph: float, train_spec: Dict) -> float:
    """
    속도를 기반으로 견인력 곡선에서 엔진 파워를 계산합니다.

    Parameters:
        speed_kph (float): 현재 속도 (km/h)
        train_spec (dict): 기차 스펙 정보 (tractive_effort_curve 포함)

    Returns:
        float: 추정된 엔진 파워 (kW)
    """
    if "tractive_effort_curve" not in train_spec:
        raise ValueError("❌ train_spec에 'tractive_effort_curve'가 없습니다.")

    tractive_force_kn = interpolate_tractive_effort(speed_kph, train_spec["tractive_effort_curve"])
    v_mps = speed_kph / 3.6
    p_engine_kw = (tractive_force_kn * 1000 * v_mps) / 1000  # N * m/s → kW

    return p_engine_kw
