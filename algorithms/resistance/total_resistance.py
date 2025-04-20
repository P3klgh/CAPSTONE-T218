def compute_total_resistance(r_davis: float, r_slope: float, r_curve: float) -> float:
    """
    전체 저항력 R_total 계산

    Parameters:
        r_davis (float): 데이비스 저항력 [N]
        r_slope (float): 경사 저항력 [N]
        r_curve (float): 곡률 저항력 [N]

    Returns:
        float: 총 저항력 R_total [N]
    """
    return r_davis + r_slope + r_curve
