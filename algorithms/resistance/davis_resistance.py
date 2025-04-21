import math

def compute_davis_resistance(velocity: float, A: float, B: float, C: float) -> float:
    """
    Compute the basic Davis resistance using the formula:
    R = A + B*v + C*v^2

    Parameters:
    - velocity (float): Train velocity in m/s
    - A (float): Constant rolling resistance term (default: 5.0)
    - B (float): Velocity-dependent resistance coefficient (default: 1.2)
    - C (float): Aerodynamic resistance coefficient (default: 0.05)

    Returns:
    - Resistance (float): Calculated resistance in Newtons per ton
    """
    R = A + B * velocity + C * velocity ** 2
    return R
