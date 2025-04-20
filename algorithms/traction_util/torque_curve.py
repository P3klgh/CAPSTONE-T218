import numpy as np
from typing import Dict

def interpolate_torque_curve(torque_curve: Dict[str, float], rpm: float) -> float:
    """
    Interpolates engine torque (in Nm) at a given RPM based on a torque curve.
    """
    # 문자열 key를 float로 변환해 매핑
    float_curve = {float(k): v for k, v in torque_curve.items()}

    rpm_values = sorted(float_curve.keys())
    torque_values = [float_curve[r] for r in rpm_values]

    return float(np.interp(rpm, rpm_values, torque_values))
