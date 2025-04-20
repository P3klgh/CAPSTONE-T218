import numpy as np
from typing import Dict

def interpolate_power_curve(power_curve: Dict[str, float], rpm: float) -> float:
    """
    Interpolates engine power (in kW) at a given RPM based on a power curve.

    Parameters:
        power_curve (dict): Dictionary mapping RPM (as string) to power in kW
                            Example: { "600": 105.1, "750": 140.1, "900": 187.2 }
        rpm (float): Engine RPM to interpolate at

    Returns:
        float: Interpolated engine power at the given RPM (in kW)
    """
    # Convert keys to float → mapping: float_rpm -> power
    float_power_curve = {float(k): v for k, v in power_curve.items()}

    # Sort by RPM
    rpm_values = sorted(float_power_curve.keys())
    power_values = [float_power_curve[r] for r in rpm_values]

    # Interpolation
    interpolated_power = float(np.interp(rpm, rpm_values, power_values))
    return interpolated_power
