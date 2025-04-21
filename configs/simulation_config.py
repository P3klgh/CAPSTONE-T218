# configs/simulation_config.py

"""
Global simulation configuration file.
Stores default values used across all simulation steps.
"""

# 초기 설정
INITIAL_VELOCITY_KPH = 20             # ✅ 초기 속도는 velocity 초기화에 사용
INITIAL_RPM = 750                     # ✅ P_engine 계산에 쓰이는 초기 RPM
TIME_STEP_SECONDS = 1.0              # ✅ 운동학에서 v = v0 + a·t 계산에 사용
SIMULATION_DURATION_SECONDS = 3600   # ❓ 현재는 미사용 (전체 시뮬 시간 제어용이지만 반복 구조에서는 안 쓰일 수도 있음)

# 속도 제한 관련
USE_SPEED_LIMIT = True               # ✅ 향후 트랙 제한 속도 적용 시 유용
MAX_GLOBAL_SPEED_KPH = 80         # ✅ 속도 상한선 (예: velocity update 후 클램핑)

# 동력 전달 효율
TRANSMISSION_EFFICIENCY = 0.85       # ✅ tractive force 계산에 사용됨

# 제동 관련 (현재 사용하지 않는다면 주석처리 or 유지)
BRAKING_EFFICIENCY = 0.7             # ❓ 에너지 소비/제동 계산 구현 시 사용 예정
