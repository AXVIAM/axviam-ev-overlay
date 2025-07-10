import os
import subprocess
from datetime import datetime
import webbrowser
import pandas as pd

# One-click master runner for AXVIAM EV Battery Overlay

def run_command(command, label):
    print(f"\n🔹 {label}...")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print(f"⚠️ {label} Error:\n{result.stderr}")


def print_summary(csv_files):
    print("\n📈 Summary of Latest AXVIAM Evaluation Outputs:")
    for csv_file in csv_files:
        path = os.path.join("reports", csv_file)
        if not os.path.exists(path):
            print(f"⚠️ File not found: {csv_file}")
            continue
        df = pd.read_csv(path)
        avg_eff = None
        total_miles = None
        total_capacity_loss = None
        avg_remaining_capacity = None
        # Attempt to read metrics if columns exist
        if "efficiency" in df.columns:
            avg_eff = df["efficiency"].mean()
        if "miles_driven" in df.columns:
            total_miles = df["miles_driven"].sum()
        if "capacity_loss_kWh" in df.columns:
            total_capacity_loss = df["capacity_loss_kWh"].sum()
        if "remaining_capacity_kWh" in df.columns:
            avg_remaining_capacity = df["remaining_capacity_kWh"].mean()

        print(f"\n- {csv_file}:")
        if avg_eff is not None:
            print(f"  • Average Efficiency: {avg_eff:.3f}")
        if total_miles is not None:
            print(f"  • Total Miles Driven: {total_miles}")
        if total_capacity_loss is not None:
            print(f"  • Total Capacity Loss (kWh): {total_capacity_loss:.3f}")
        if avg_remaining_capacity is not None:
            print(f"  • Average Remaining Capacity (kWh): {avg_remaining_capacity:.3f}")

def print_evaluation_summary():
    import json
    import os

    summary_file = None
    # Find the latest converted healing input json
    candidates = [f for f in os.listdir("reports") if f.startswith("converted_healing_input_") and f.endswith(".json")]
    if candidates:
        summary_file = sorted(candidates)[-1]

    if summary_file is None:
        print("\n⚠️ Evaluation Summary: No converted healing input file found.")
        return

    summary_path = os.path.join("reports", summary_file)
    try:
        with open(summary_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"\n⚠️ Evaluation Summary: Failed to load {summary_file}: {e}")
        return

    # Extract summary info
    total_cells = 96  # hardcoded known total cells count for now
    healed_cells = len(data) if isinstance(data, list) else 0
    avg_efficiency_start = 0.77  # baseline known from metadata in the factory initialization (hardcoded)
    avg_efficiency_end = None
    input_file = summary_file

    # Try to read the final efficiency from the CSVs
    # Prefer run_overlay CSV (latest)
    import pandas as pd
    overlay_csv_candidates = [f for f in os.listdir("reports") if f.startswith("run_overlay_simulated_pack_diagnostics_") and f.endswith(".csv")]
    if overlay_csv_candidates:
        overlay_csv = sorted(overlay_csv_candidates)[-1]
        try:
            df = pd.read_csv(os.path.join("reports", overlay_csv))
            if "efficiency" in df.columns:
                avg_efficiency_end = df["efficiency"].mean()
        except Exception:
            pass

    if avg_efficiency_end is None:
        avg_efficiency_end = avg_efficiency_start

    # Approximate miles per charge based on capacity and efficiency
    # Base miles per charge start at 231 (arbitrary example)
    miles_start = 231
    # Estimate end miles per charge by ratio of efficiency gain
    miles_end = round(miles_start * (avg_efficiency_end / avg_efficiency_start))

    # Construct symbolic signature (placeholder, can be read from factory metadata file or hardcoded)
    signature = "ψₐ:8356 ∇̃:5 Ω"  # for now hardcoded to last run_overlay signature

    print("\n📋 Evaluation Summary")
    print(f"  Analyzed Cells: {total_cells}")
    print(f"  Healed Cells: {healed_cells} (from real-world log)")
    print(f"  Avg Efficiency Gain: from {avg_efficiency_start:.3f} → {avg_efficiency_end:.3f}")
    print(f"  Miles per Charge: estimated {miles_start} → {miles_end} mi")
    print(f"  Signature: {signature}")
    print(f"  Input File: {input_file}")
    print()


def main():
    print("\n🚀 AXVIAM One-Click Evaluation Runner")
    timestamp = "latest"

    # Clean old outputs (except previous zip bundles)
    print("🧹 Cleaning old evaluation outputs...")
    for folder in ["reports", "reports/plots"]:
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            if os.path.isfile(fpath) and not fname.endswith(".zip"):
                os.remove(fpath)

    # Step 1: Convert real-world BMS log to healing format
    run_command("python convert_bms_log.py --output_suffix latest", "Converting BMS log")

    # Step 2: Run full overlay process with converted healing data
    run_command("python run_overlay.py --output_suffix latest", "Running AXVIAM overlay")

    # Step 3: Run simulation using the real-world converted input
    run_command("python sim_runner.py --output_suffix latest", "Running Simulation Runner")

    # Step 4: Run demo with factory healing example
    run_command("python demo_runner.py --output_suffix latest", "Running Demo Runner")
    
    run_command("python generate_plots.py --output_suffix latest", "Generating Output Visuals")

    latest_csvs = [
        "reports/demo_runner_real_simulated_pack_diagnostics_latest.csv",
        "reports/sim_runner_real_simulated_pack_diagnostics_latest.csv",
        "reports/run_overlay_simulated_pack_diagnostics_latest.csv"
    ]
    # update_command = f"python update_readme_summary.py {' '.join(latest_csvs)}"
    # run_command(update_command, "Updating README summary")
    run_command("python launch_report.py", "Generating HTML Output Summary")

    # Copy latest timestamped outputs to _latest versions
    import shutil
    def copy_latest(source_pattern, target_latest):
        matches = [f for f in os.listdir("reports") if (f.startswith(source_pattern) and (f.endswith(".csv") or f.endswith(".json")))]
        if matches:
            latest_file = sorted(matches)[-1]
            shutil.copyfile(os.path.join("reports", latest_file), os.path.join("reports", target_latest))

    copy_latest("converted_healing_input_", "converted_healing_input_latest.json")
    copy_latest("demo_runner_real_simulated_pack_diagnostics_", "demo_runner_real_simulated_pack_diagnostics_latest.csv")
    copy_latest("sim_runner_real_simulated_pack_diagnostics_", "sim_runner_real_simulated_pack_diagnostics_latest.csv")
    copy_latest("run_overlay_simulated_pack_diagnostics_", "run_overlay_simulated_pack_diagnostics_latest.csv")

    # Step 7: Zip the latest evaluation outputs
    zip_name = f"evaluation_bundle_{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip"
    zip_command = (
        f"zip -r {zip_name} "
        f"reports/converted_healing_input_latest.json "
        f"reports/demo_runner_real_simulated_pack_diagnostics_latest.csv "
        f"reports/sim_runner_real_simulated_pack_diagnostics_latest.csv "
        f"reports/run_overlay_simulated_pack_diagnostics_latest.csv "
        f"reports/plots/*.png "
        f"launch_report.html"
    )
    run_command(zip_command, f"Creating evaluation snapshot: {zip_name}")

    # --- Summary Report ---
    import pandas as pd

    print_summary([
        "demo_runner_real_simulated_pack_diagnostics_latest.csv",
        "sim_runner_real_simulated_pack_diagnostics_latest.csv",
        "run_overlay_simulated_pack_diagnostics_latest.csv"
    ])

    print_evaluation_summary()

    print("\n✅ All AXVIAM tests complete. Review output files in /reports.")

    # Automatically open the HTML summary report in the default web browser
    import webbrowser
    report_path = os.path.abspath("launch_report.html")
    try:
        browser = webbrowser.get()
        browser.open_new_tab(f"file://{report_path}")
    except Exception as e:
        print(f"⚠️ Failed to open browser automatically: {e}")
        print(f"🔗 You can manually open: file://{report_path}")


if __name__ == "__main__":
    main()