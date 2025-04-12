import json
import os

"""
📌 Data Validation Script for Merged Track Data (Lucinda & Karloo)
This script performs integrity checks on processed track data before using it in simulation algorithms.

🔹 Step 1: Load merged JSON files for Lucinda & Karloo.
🔹 Step 2: Check for missing required fields.
🔹 Step 3: Identify logical inconsistencies (e.g., negative values).
🔹 Step 4: Display errors or confirm data validity.

🔹 Future Extension:
   - Support for user-uploaded files & different track datasets.
   - Integration with database validation before inserting data.
"""

# ✅ Define JSON files to validate (Lucinda & Karloo datasets)
base_dir = "../../given_data/extracted_processed_json"
json_files = {
    "Lucinda": os.path.join(base_dir, "final_merged(Lucinda).json"),
    "Karloo": os.path.join(base_dir, "final_merged(Karloo).json"),
}

# ✅ Required fields (Must exist, otherwise an error)
required_fields = [
    "Min_Slope", "Max_Slope", "Avg_Slope", "Length",
    "Z_Min", "Z_Max", "Z_Mean",
    "X_Start", "Y_Start", "X_End", "Y_End"
]

# ✅ Optional fields (Not required, but useful if present)
optional_fields = ["CurveID", "Radius", "X_Center", "Y_Center"]

# ✅ Function to detect missing fields and logical errors
def is_outlier(data):
    errors = []

    # 🔍 Check for missing required fields
    for field in required_fields:
        if field not in data:
            errors.append(f"❌ Missing field: {field}")

    # 🔍 Logical consistency checks (Avoid None values)
    min_slope = data.get("Min_Slope")
    max_slope = data.get("Max_Slope")
    length = data.get("Length")
    radius = data.get("Radius")
    z_min = data.get("Z_Min")
    z_max = data.get("Z_Max")

    if min_slope is not None and max_slope is not None:
        if min_slope > max_slope:
            errors.append(f"❌ Min_Slope ({min_slope}) is greater than Max_Slope ({max_slope})")

    if length is not None and length < 0:
        errors.append(f"❌ Length is negative: {length}")

    if radius is not None and radius < 0:
        errors.append(f"❌ Radius is negative: {radius}")

    if z_min is not None and z_max is not None:
        if z_min > z_max:
            errors.append(f"❌ Z_Min ({z_min}) is greater than Z_Max ({z_max})")

    return errors


# ✅ Run validation on both datasets (Lucinda & Karloo)
for dataset_name, json_file in json_files.items():
    print(f"\n🔍 Validating dataset: {dataset_name}")

    if not os.path.exists(json_file):
        print(f"❌ Error: JSON file not found: {json_file}")
        continue

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    errors_found = False
    for key, entry in data.items():
        errors = is_outlier(entry)
        if errors:
            print(f"\n🔍 Issues found in ID: {key}")
            for err in errors:
                print(err)
            errors_found = True

    if not errors_found:
        print(f"✅ All data in {dataset_name} is valid!")
