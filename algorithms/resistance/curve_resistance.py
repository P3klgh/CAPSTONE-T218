import math

def compute_curve_resistance(mass_kg: float, velocity_mps: float, r_curve: float, a_slope_rad: float) -> float:
    """
    곡률에 의한 저항력 R_curve 계산 (단위: N)
    공식: R_curve = M * v² / rCurve * sin(a_slope)

    Parameters:
        mass_kg (float): 질량 (kg)
        velocity_mps (float): 속도 (m/s)
        r_curve (float): 곡률 반지름 (meters)
        a_slope_rad (float): 기울기 각도 (radians)

    Returns:
        float: R_curve (곡률 저항력) [N]
    """
    if r_curve in (None, 0) or a_slope_rad is None:
        return 0
    return (mass_kg * velocity_mps ** 2 / r_curve) * math.sin(a_slope_rad)
