# traction_util/__init__.py

"""
traction_util 패키지:
Power, Torque, Tractive Effort curve 기반 유틸리티 모음.

제공 모듈:
- power_curve.py: Power vs RPM 선형 보간
- torque_curve.py: Torque vs RPM 선형 보간
- tractive_effort_curve.py: Speed vs Tractive Effort 보간

사용 예시:
from traction_util import interpolate_power_from_rpm
"""

from .power_curve import interpolate_power_curve
from .torque_curve import interpolate_torque_curve
from .tractive_effort_curve import interpolate_tractive_effort

