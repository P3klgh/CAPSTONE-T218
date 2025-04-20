import math

def compute_slope_resistance(mass_kg: float, a_slope_rad: float) -> float:
    """
    기울기에 의한 저항력 R_slope 계산 (단위: N)
    공식: R_slope = M * g * sin(a_slope)

    Parameters:
        mass_kg (float): 구간에서 적용되는 질량 (kg)
        a_slope_rad (float): 해당 구간의 기울기 (radians)

    Returns:
        float: R_slope (경사 저항력) [N]
    """
    g = 9.81  # 중력 가속도 [m/s^2]
    if a_slope_rad is None:
        return 0
    return mass_kg * g * math.sin(a_slope_rad)
