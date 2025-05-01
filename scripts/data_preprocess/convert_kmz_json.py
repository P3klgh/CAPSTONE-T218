import os
import zipfile
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup

"""
📌 Data Preprocessing for Simulation Algorithm Development
This script extracts raw data from KMZ files, converts them into KML and JSON formats, 
and stores all extracted data in JSON without filtering. 
The processed data will be used for further algorithm development.

🔹 Step 1: Convert KMZ to KML
🔹 Step 2: Convert KML to JSON
🔹 Step 3: Extract all data (No filtering)
🔹 Step 4: Save extracted data for review
"""


# ✅ Step 1: Convert KMZ → KML
def convert_kmz_to_kml(kmz_file, output_dir="../../given_data/extracted_kml"):
    """
    Converts a KMZ file into a KML file.

    Args:
        kmz_file (str): Path to the input KMZ file.
        output_dir (str): Directory where the extracted KML file will be saved.

    Returns:
        str: Path to the extracted KML file, or None if an error occurs.
    """
    if not os.path.exists(kmz_file):
        print(f"❌ Error: {kmz_file} not found.")
        return None

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(kmz_file))[0]
    kml_path = os.path.join(output_dir, f"{filename}.kml")

    with zipfile.ZipFile(kmz_file, 'r') as kmz:
        for file in kmz.namelist():
            if file.endswith(".kml"):
                with open(kml_path, "wb") as kml_file:
                    kml_file.write(kmz.read(file))
                print(f"✅ KMZ → KML converted: {kml_path}")
                return kml_path
    return None


# ✅ Step 2: Convert KML → JSON
def convert_kml_to_json(kml_file, output_dir="../../given_data/extracted_json"):
    """
    Converts a KML file into JSON format by extracting all Placemarks.

    Args:
        kml_file (str): Path to the input KML file.
        output_dir (str): Directory where the JSON file will be saved.

    Returns:
        str: Path to the generated JSON file, or None if an error occurs.
    """
    if not os.path.exists(kml_file):
        print(f"❌ Error: {kml_file} not found.")
        return None

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(kml_file))[0]
    json_path = os.path.join(output_dir, f"{filename}.json")

    tree = ET.parse(kml_file)
    root = tree.getroot()
    ns = {"kml": root.tag.split("}")[0][1:]}

    json_data = {"Placemarks": []}
    for placemark in root.findall(".//kml:Placemark", ns):
        description = placemark.find("kml:description", ns)
        json_data["Placemarks"].append({
            "id": placemark.get("id", "No ID"),
            "description": description.text.strip() if description is not None else ""
        })

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    print(f"✅ KML → JSON converted: {json_path}")
    return json_path


# ✅ Step 3: Extract all data from JSON (No filtering)
def extract_all_data(input_json, output_dir="../../given_data/extracted_processed_json"):
    """
    Extracts all available data from the JSON file without filtering.

    Args:
        input_json (str): Path to the input JSON file.
        output_dir (str): Directory where the processed JSON file will be saved.

    Returns:
        str: Path to the fully extracted JSON file.
    """
    if not os.path.exists(input_json):
        print(f"❌ Error: {input_json} not found.")
        return None

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(input_json))[0]
    output_json = os.path.join(output_dir, f"{filename}_full.json")

    with open(input_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    all_data = []
    for placemark in data.get("Placemarks", []):
        soup = BeautifulSoup(placemark.get("description", ""), "html.parser")
        table = soup.find("table")

        extracted_info = {"id": placemark["id"]}
        if table:
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()

                    # ✅ Convert to float if possible, otherwise keep as a string
                    try:
                        extracted_info[key] = float(value)
                    except ValueError:
                        extracted_info[key] = value

        # ✅ Store all extracted data without filtering
        all_data.append(extracted_info)

    # ✅ Save the fully extracted data in JSON format
    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, indent=4, ensure_ascii=False)

    print(f"✅ All data extracted and saved: {output_json}")
    return output_json


# ✅ Step 4: Main Execution
def main():
    """
    Main execution function that processes multiple KMZ files by:
    - Converting KMZ → KML
    - Converting KML → JSON
    - Extracting all available data (no filtering)
    """

    # ✅ Add new KMZ files here
    kmz_files = [
        "../../given_data/raw_data/HBTSugarLineLucindaCurveRadii.kmz",
        "../../given_data/raw_data/HBTSugarLineLucindaGrade25m.kmz",
        "../../given_data/raw_data/PCK2KarlooCurveRadii.kmz",  # ✅ Newly added
        "../../given_data/raw_data/PCK2KarlooGrade25m.kmz"  # ✅ Newly added
    ]

    for kmz in kmz_files:
        kml_path = convert_kmz_to_kml(kmz)
        if kml_path:
            json_path = convert_kml_to_json(kml_path)
            if json_path:
                extract_all_data(json_path)  # ✅ Save all data without filtering


if __name__ == "__main__":
    main()
