# algorithms/kinematics/velocity_update.py

def update_velocity(prev_velocity_mps: float, acceleration_mps2: float, time_step_sec: float) -> float:
    """
    Computes new velocity using basic kinematic equation:
    v = v0 + a * dt

    Parameters:
        prev_velocity_mps (float): Previous velocity [m/s]
        acceleration_mps2 (float): Acceleration [m/s^2]
        time_step_sec (float): Time interval [s]

    Returns:
        float: Updated velocity [m/s]
    """
    return prev_velocity_mps + acceleration_mps2 * time_step_sec
