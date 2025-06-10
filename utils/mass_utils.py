# utils/mass_utils.py

def compute_total_train_mass(spec: dict) -> float:
    """
    Parameters:
        spec (dict): train_spec.json

    Returns:
        float: 전체 질량 (kg)
    """
    return (
        spec["mass_full_bin"] * spec["num_full_bins"]
        + spec["mass_empty_bin"] * spec["num_empty_bins"]
        + spec["mass_locomotive"]
        + (spec["mass_brakevan"] if spec["has_brakevan"] else 0)
    )
