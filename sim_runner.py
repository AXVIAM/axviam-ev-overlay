import json
from ev_overlay.simulator import simulate_ev_drive
from ev_overlay.analyzer import evaluate_efficiency

def load_simulation_log(path):
    with open(path, 'r') as f:
        return json.load(f)

def convert_log_to_healing(log_data):
    return [
        {
            "cell_index": idx,
            "restored_psi": round(entry.get("psi_flux", 0.5) * 1.05, 3),
            "restored_tension": round(0.6 + 0.05 * (entry.get("voltage", 3.6) - 3.6), 3)
        }
        for idx, entry in enumerate(log_data)
    ]

def main():
    print("🧪 Running AXVIAM EV Simulation Runner...")
    log_data = load_simulation_log("real_input/sample_bms_log.json")
    healing_data = convert_log_to_healing(log_data)

    print("🔧 Converted healing diagnostics:")
    for cell in healing_data:
        print(cell)

    print("\n🚦 Simulating EV drive with healed pack...")
    simulation_result = simulate_ev_drive(healing_data, output_prefix="sim_runner_real")
    print(f"\n🔋 Simulation output:\n{simulation_result}")

    print("\n📊 Efficiency analysis:")
    print(evaluate_efficiency(simulation_result))

if __name__ == "__main__":
    main()