import statistics

def analyze_battery_pack(healing_data):
    """
    Analyze EV battery pack healing data and return key diagnostics.
    """
    if not healing_data or not isinstance(healing_data, list):
        return {"error": "Invalid data format"}

    restored_psis = []
    restored_tensions = []

    for entry in healing_data:
        psi = entry.get("restored_psi")
        tension = entry.get("restored_tension")
        if psi is not None and tension is not None:
            restored_psis.append(psi)
            restored_tensions.append(tension)

    if not restored_psis or not restored_tensions:
        return {"error": "No valid healing data found"}

    psi_gain = round(statistics.mean(restored_psis), 3)
    tension_gain = round(statistics.mean(restored_tensions), 3)
    health_score = round((psi_gain + tension_gain) / 2, 3)

    return {
        "average_restored_psi": psi_gain,
        "average_restored_tension": tension_gain,
        "overall_health_score": health_score
    }

def evaluate_efficiency(simulation_results):
    """
    Analyze simulation results from EV drive to assess battery efficiency.
    """
    if not simulation_results or not isinstance(simulation_results, list):
        return {"error": "Invalid simulation result format"}

    efficiencies = []
    miles = 0
    total_kwh_lost = 0
    remaining_capacities = []

    for result in simulation_results:
        efficiency = result.get("efficiency")
        if efficiency is not None:
            efficiencies.append(efficiency)
        miles += result.get("miles_driven", 0)
        total_kwh_lost += result.get("capacity_loss_kWh", 0)
        if "remaining_capacity_kWh" in result:
            remaining_capacities.append(result["remaining_capacity_kWh"])

    if not efficiencies:
        return {"error": "No valid efficiency data found"}

    return {
        "average_efficiency": round(statistics.mean(efficiencies), 3),
        "total_miles_driven": miles,
        "total_capacity_loss_kWh": round(total_kwh_lost, 3),
        "average_remaining_capacity_kWh": round(statistics.mean(remaining_capacities), 3) if remaining_capacities else None
    }
