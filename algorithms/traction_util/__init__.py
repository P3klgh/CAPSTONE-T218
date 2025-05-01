# traction_util/__init__.py

"""
traction_util 패키지:
Tractive Effort 보간 유틸리티 모음

제공 모듈:
- tractive_effort_curve.py: Speed vs Tractive Effort 보간

사용 예시:
from traction_util import interpolate_tractive_effort
"""

from .tractive_effort_curve import interpolate_tractive_effort
