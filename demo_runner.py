import json
from ev_overlay.factory_init import initialize_factory_pack
from ev_overlay.healing_parser import run_healing_diagnostics
from ev_overlay.simulator import simulate_ev_drive
from ev_overlay.analyzer import evaluate_efficiency

def main():
    print("🧪 Running AXVIAM EV Simulation Runner...")

    # Step 1: Initialize factory
    factory = initialize_factory_pack("default_pack", "metadata.json")
    print("🏭 Factory Pack Initialized:", factory)

    # Step 2: Run healing diagnostics
    import glob
    import os

    # Find the latest converted healing input file
    healing_files = glob.glob("reports/converted_healing_input_*.json")
    if not healing_files:
        raise FileNotFoundError("No converted healing input files found in reports/")
    latest_healing_file = max(healing_files, key=os.path.getmtime)

    with open(latest_healing_file, "r") as f:
        healing_data = json.load(f)
    print("🔧 Healing diagnostics loaded:")
    for entry in healing_data:
        print(entry)

    # Step 3: Simulate EV drive
    print("\n🚦 Simulating EV drive with healed pack...")
    output_prefix = "demo_runner_real"
    simulation_result = simulate_ev_drive([{
        "pack_id": factory["pack_id"],
        "healing_data": healing_data,
        "capacity_kWh": factory["factory_metadata"].get("capacity_kWh", 75),
        "cycles": 0
    }], output_prefix=output_prefix)

    print("\n🔋 Simulation output:")
    for result in simulation_result:
        print(result)

    # Step 4: Evaluate efficiency
    print("\n📊 Efficiency analysis:")
    print(evaluate_efficiency(simulation_result))

if __name__ == "__main__":
    main()