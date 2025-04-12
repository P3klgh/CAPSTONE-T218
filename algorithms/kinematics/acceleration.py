# acceleration.py

"""
🔧 Acceleration Computation Module

Computes acceleration based on the net force (F_tractive - R_total) and train mass.

Equation:
    a = (F_tractive - R_total) / M
"""

def compute_acceleration(f_tractive: float, r_total: float, total_mass_kg: float) -> float:
    """
    Computes acceleration of the train.

    Parameters:
        f_tractive (float): Tractive force (N)
        r_total (float): Total resistance (N)
        total_mass_kg (float): Mass of the train (kg)

    Returns:
        float: Acceleration (m/s²)
    """
    if total_mass_kg <= 0:
        raise ValueError("❌ Train mass must be positive.")

    return (f_tractive - r_total) / total_mass_kg
