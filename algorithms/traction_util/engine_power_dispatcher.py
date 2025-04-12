import math
from typing import Dict
from ..traction_util.power_curve import interpolate_power_curve
from ..traction_util.torque_curve import interpolate_torque_curve
from ..traction_util.tractive_effort_curve import interpolate_tractive_effort

def get_p_engine(
    speed_kph: float,
    rpm: float,
    train_spec: Dict
) -> float:
    """
    Calculates engine power (P_engine) in kilowatts based on available curve data in train_spec.

    Priority order:
        1. engine_power_curve (Power vs RPM)
        2. engine_torque_curve (Torque vs RPM)
        3. tractive_effort_curve (Tractive Effort vs Speed)
    """
    if "engine_power_curve" in train_spec:
        return interpolate_power_curve(train_spec["engine_power_curve"], rpm)

    elif "engine_torque_curve" in train_spec:
        torque_nm = interpolate_torque_curve(train_spec["engine_torque_curve"], rpm)
        omega_rad_s = (rpm * 2 * math.pi) / 60
        p_engine_kw = (torque_nm * omega_rad_s) / 1000
        return p_engine_kw

    elif "tractive_effort_curve" in train_spec:
        tractive_force_kn = interpolate_tractive_effort(train_spec["tractive_effort_curve"], speed_kph)
        v_mps = speed_kph / 3.6
        p_engine_kw = (tractive_force_kn * 1000 * v_mps) / 1000  # Convert to kW
        return p_engine_kw

    else:
        raise ValueError("❌ No valid curve data found in train specification.")
