import pandas as pd
import os

"""
📌 Convert Excel Data to JSON for Simulation Algorithm
This script converts raw track data from Excel (`.xls`) files into JSON format. 
All extracted data is saved **without filtering** to maintain completeness.

🔹 Step 1: Load Excel files
🔹 Step 2: Convert to JSON format
🔹 Step 3: Save to extracted processed folder (for further analysis)
"""

# ✅ Step 1: Define Excel files to convert
xls_files = [
    "../../given_data/raw_data/HBTSugarLineLucindaGrade.xls",
    "../../given_data/raw_data/PCK2KarlooGrade.xls"  # ✅ Newly added file
]

# ✅ Step 2: Set simulation_results directory (same as KMZ-converted JSONs)
output_dir = "../../given_data/extracted_processed_json"
os.makedirs(output_dir, exist_ok=True)

# ✅ Step 3: Convert each Excel file to JSON
for xls_file in xls_files:
    if not os.path.exists(xls_file):
        print(f"❌ Warning: {xls_file} not found. Skipping...")
        continue

    # Load Excel data
    df = pd.read_excel(xls_file)
    filename = os.path.splitext(os.path.basename(xls_file))[0]  # Extract filename without extension
    json_path = os.path.join(output_dir, f"{filename}_full.json")

    # Save to JSON (without filtering)
    df.to_json(json_path, orient="records", indent=4, force_ascii=False)

    print(f"✅ Excel full data converted to JSON: {json_path}")
