import os
import subprocess

# ✅ Define the list of algorithm scripts to execute in order
ALGORITHM_SCRIPTS = [
    "algorithms/compute_track_distance.py",  # Computes track distance (d_xy)
    "algorithms/compute_a_slope.py"  # Computes slope angle (a_slope)
    # Future expansions:
    # "algorithms/R_slope.py",  # Computes slope resistance (R_slope)
    # "algorithms/R_curve.py",  # Computes curvature resistance (R_curve)
    # "algorithms/energy_consumption.py"  # Calculates energy usage
]


# ✅ Function to execute all algorithms in sequence
def run_simulation():
    print("🚀 Starting the simulation process...")

    for script in ALGORITHM_SCRIPTS:
        print(f"⚡ Running {script}...")

        # Execute the script as a subprocess with UTF-8 encoding
        result = subprocess.run(
            ["python", script],
            capture_output=True,
            text=True,
            encoding="utf-8",  # ✅ Force UTF-8 encoding
            errors="replace"   # ✅ Prevent UnicodeDecodeError by replacing problematic characters
        )

        # ✅ Print script output
        print(result.stdout)

        # ✅ Check for errors
        if result.returncode != 0:
            print(f"❌ Error encountered in {script}: {result.stderr}")
            print("⚠️ Stopping further execution due to an error.")
            break  # Stop execution if an error occurs

    print("✅ Simulation process completed.")


# ✅ Run the simulation if executed directly
if __name__ == "__main__":
    run_simulation()
