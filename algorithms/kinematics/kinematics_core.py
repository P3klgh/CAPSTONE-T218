# algorithms/kinematics/apply_kinematics.py

from algorithms.kinematics.tractive_force import compute_tractive_force
from algorithms.kinematics.acceleration import compute_acceleration
from algorithms.kinematics.velocity_update import update_velocity
from algorithms.traction_util.engine_power_dispatcher import get_p_engine
from configs.simulation_config import INITIAL_RPM, TIME_STEP_SECONDS

def apply_kinematics_to_segment(entry: dict, mass_kg: float, train_spec: dict) -> float:
    """
    Applies kinematics formulas to compute the next velocity for a track segment.

    Parameters:
        entry (dict): Track segment data with velocity, resistance, etc.
        mass_kg (float): Total train mass in kg
        train_spec (dict): Train specification dictionary

    Returns:
        float: Updated velocity (m/s)
    """
    v_mps = entry.get("velocity_mps", 0)
    r_total = entry.get("R_total", 0)

    # 1. P_engine 계산
    p_engine_kw = get_p_engine(v_mps * 3.6, INITIAL_RPM, train_spec)
    entry["P_engine_kw"] = p_engine_kw

    # 2. F_tractive 계산
    f_tractive = compute_tractive_force(p_engine_kw, v_mps)
    if f_tractive is None:
        f_tractive = 0  # 정지 상태일 경우 0 처리

    # 3. 가속도 계산
    acceleration = compute_acceleration(f_tractive, r_total, mass_kg)
    entry["acceleration"] = acceleration

    # 4. 속도 업데이트
    updated_velocity = update_velocity(v_mps, acceleration, TIME_STEP_SECONDS)
    return updated_velocity
