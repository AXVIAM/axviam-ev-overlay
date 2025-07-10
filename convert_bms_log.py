import csv
import json
from datetime import datetime
import os

def convert_json_to_healing_format(input_json_path, output_json_path):
    healing_data = []

    with open(input_json_path, "r") as infile:
        try:
            raw_data = json.load(infile)
        except json.JSONDecodeError:
            print("❌ Failed to parse input JSON.")
            return

    for entry in raw_data:
        try:
            cell_index = int(entry.get("cell_id", entry.get("cell_index", 0)))
            voltage = float(entry["voltage"])
            temperature = float(entry["temperature"])

            restored_psi = round((voltage - 2.5) / 1.5, 3)
            restored_tension = round(1.0 - (temperature - 20) / 40, 3)

            healing_data.append({
                "cell_index": cell_index,
                "restored_psi": max(0.0, min(1.0, restored_psi)),
                "restored_tension": max(0.0, min(1.0, restored_tension))
            })
        except (ValueError, KeyError):
            continue

    with open(output_json_path, "w") as outfile:
        json.dump(healing_data, outfile, indent=2)

    print(f"✅ Converted {len(healing_data)} cells to AXVIAM healing format.")
    print(f"📄 Output saved to: {output_json_path}")

if __name__ == "__main__":
    input_file = "real_input/sample_bms_log.json"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = f"reports/converted_healing_input_{timestamp}.json"

    os.makedirs("reports", exist_ok=True)
    convert_json_to_healing_format(input_file, output_file)