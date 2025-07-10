import random
import csv

def simulate_drive_cycle(pack_state, miles=100):
    """
    Simulates an EV drive cycle for a given number of miles.
    Returns the adjusted pack state and diagnostics.
    """
    # Ensure default keys exist
    pack_state.setdefault("capacity_kWh", 75)
    pack_state.setdefault("cycles", 0)
    # Add slight variability to capacity and cycles
    pack_state["capacity_kWh"] *= random.uniform(0.98, 1.02)
    pack_state["cycles"] += random.uniform(-0.1, 0.1)

    consumption_rate = 0.25  # kWh per mile (nominal)
    degradation_factor = 0.005  # percentage of capacity lost per 100 miles
    
    total_consumption = miles * consumption_rate
    capacity_loss = degradation_factor * (miles / 100) * pack_state["capacity_kWh"]
    pack_state["capacity_kWh"] -= capacity_loss
    pack_state["cycles"] += miles / 250
    # Introduce minor degradation over time
    if "restored_psi" in pack_state:
        pack_state["restored_psi"] *= random.uniform(0.98, 0.995)
    if "restored_tension" in pack_state:
        pack_state["restored_tension"] *= random.uniform(0.985, 0.997)

    efficiency = round(1 - (capacity_loss / total_consumption) + random.uniform(-0.01, 0.01), 4)

    diagnostics = {
        "miles_driven": miles,
        "total_consumed_kWh": total_consumption,
        "capacity_loss_kWh": round(capacity_loss, 3),
        "efficiency": efficiency,
        "remaining_capacity_kWh": round(pack_state["capacity_kWh"], 2),
        "cycle_count": round(pack_state["cycles"], 2)
    }

    return pack_state, diagnostics

def simulate_multiple_packs(packs, miles_each=100):
    results = []
    for pack in packs:
        if "capacity_kWh" not in pack:
            pack["capacity_kWh"] = 75  # default fallback
        # Add slight variations before simulating drive cycle
        pack["restored_psi"] = random.uniform(0.45, 0.72)
        pack["restored_tension"] = random.uniform(0.59, 0.615)
        updated_pack, diagnostics = simulate_drive_cycle(pack, miles_each)
        results.append(diagnostics)
    return results

import time

def generate_output_filename(prefix=None):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    if prefix:
        return f"reports/{prefix}_simulated_pack_diagnostics_{timestamp}.csv"
    return f"reports/simulated_pack_diagnostics_{timestamp}.csv"

def save_simulation_results(results, filename=None):
    if filename is None:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"reports/simulated_pack_diagnostics_{timestamp}.csv"
    keys = results[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

def simulate_ev_drive(packs, miles_each=100, output_prefix=None):
    """
    Wrapper for simulate_multiple_packs to match expected interface.
    """
    results = simulate_multiple_packs(packs, miles_each)
    save_simulation_results(results, filename=generate_output_filename(output_prefix))
    return results
