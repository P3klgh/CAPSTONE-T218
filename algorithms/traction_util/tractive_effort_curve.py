import numpy as np
from typing import Dict

def interpolate_tractive_effort(speed_kph: float, tractive_effort_curve: Dict[str, float]) -> float:
    """
    Interpolates tractive effort (in kN) at a given speed (km/h) based on the tractive effort curve.
    """
    float_curve = {float(k): v for k, v in tractive_effort_curve.items()}

    speed_values = sorted(float_curve.keys())
    effort_values = [float_curve[s] for s in speed_values]

    return float(np.interp(speed_kph, speed_values, effort_values))
