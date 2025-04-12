# configs/simulation_config.py

"""
Global simulation configuration file.
Stores default values used across all simulation steps.
"""

# Initial settings
INITIAL_VELOCITY_KPH = 10             # 초기 속도 [km/h]
INITIAL_RPM = 750                     # 초기 엔진 RPM [rev/min]
TIME_STEP_SECONDS = 1.0              # 시뮬레이션 시간 간격 [s]
SIMULATION_DURATION_SECONDS = 3600   # 총 시뮬레이션 시간 [s]

# Optional toggles
USE_SPEED_LIMIT = True               # 트랙 제한 속도 적용 여부
MAX_GLOBAL_SPEED_KPH = 80            # 전체 구간 최대 허용 속도
TRANSMISSION_EFFICIENCY = 0.85  # 기본값 (필요시 조정 가능)

# Braking settings
BRAKING_EFFICIENCY = 0.7