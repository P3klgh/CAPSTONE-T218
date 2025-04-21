# algorithms/kinematics/apply_kinematics.py

from algorithms.kinematics.tractive_force import compute_tractive_force
from algorithms.kinematics.acceleration import compute_acceleration
from algorithms.kinematics.velocity_update import update_velocity
from algorithms.traction_util.engine_power_dispatcher import get_p_engine_from_speed
from configs.simulation_config import  TIME_STEP_SECONDS, USE_SPEED_LIMIT, MAX_GLOBAL_SPEED_KPH

def apply_kinematics_to_segment(entry: dict, mass_kg: float, train_spec: dict) -> float:
    v_mps = entry.get("velocity_mps", 0)
    r_total = entry.get("R_total", 0)

    # ✅ 0. 너무 낮은 속도 방어 (트랙션 계산 방지)
    if v_mps < 0.1:
        v_mps = 0.1  # 최소 속도 강제 주입

    # 1. P_engine 계산
    p_engine_kw = get_p_engine_from_speed(v_mps * 3.6, train_spec)
    entry["P_engine_kw"] = p_engine_kw

    # 2. F_tractive 계산
    f_tractive = compute_tractive_force(p_engine_kw, v_mps)
    if f_tractive is None:
        f_tractive = 0

    # 3. 가속도 계산
    acceleration = compute_acceleration(f_tractive, r_total, mass_kg)
    entry["acceleration"] = acceleration

    # 4. 속도 업데이트 + 클램핑
    updated_velocity = update_velocity(v_mps, acceleration, TIME_STEP_SECONDS)
    # ✅ 속도 제한 적용 (기본값: 80 km/h)
    if USE_SPEED_LIMIT:
        max_speed_mps = MAX_GLOBAL_SPEED_KPH / 3.6
        if updated_velocity > max_speed_mps:
            updated_velocity = max_speed_mps  # 속도 클램핑
            # 🔽 감속이 발생한 것으로 간주하고 가속도 다시 계산
            acceleration = (updated_velocity - v_mps) / TIME_STEP_SECONDS

    # ✅ 음수 속도 방어
    updated_velocity = max(updated_velocity, 0.0)
    entry["acceleration"] = acceleration  # 최종적으로 보정된 acceleration 저장
    return updated_velocity