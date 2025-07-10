import os
import sys
import csv
import glob
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "ev_overlay"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "engine"))
from ev_overlay.factory_init import initialize_factory_pack
from ev_overlay.healing_parser import run_healing_diagnostics
from ev_overlay.simulator import simulate_ev_drive
from analyzer import evaluate_efficiency

def main():
    print("🚗 Starting AXVIAM EV Battery Overlay...")

    # Step 1: Initialize factory settings
    manifest = initialize_factory_pack("default_pack", "metadata.json")
    print("✅ Factory initialized:", manifest)

    # Look for the most recent converted healing input
    healing_input_files = sorted(
        glob.glob(os.path.join("reports", "converted_healing_input_*.json")),
        key=os.path.getmtime,
        reverse=True
    )

    if healing_input_files:
        latest_file = healing_input_files[0]
        print(f"📥 Using real-world input from: {latest_file}")
        with open(latest_file, "r") as f:
            healing_data = json.load(f)
    else:
        healing_data = run_healing_diagnostics()
        print(f"🩺 Healing diagnostics result: {healing_data}")

    # Step 3: Simulate EV drive performance
    simulation_output = simulate_ev_drive(healing_data, output_prefix="run_overlay")
    print("🔋 Drive simulation complete.")

    # Step 4: Evaluate results
    analysis_result = evaluate_efficiency(simulation_output)
    print("📊 Efficiency analysis:", analysis_result)

if __name__ == "__main__":
    main()
