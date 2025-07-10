import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

def find_latest_csvs(reports_dir="reports"):
    pattern = os.path.join(reports_dir, "*_simulated_pack_diagnostics_*.csv")
    return sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)[:3]

def plot_simulation_results(csv_path, output_dir="reports/plots"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    name_tag = os.path.basename(csv_path).replace(".csv", "")

    x = range(len(df))
    if "efficiency" in df.columns:
        plt.figure()
        plt.plot(x, df["efficiency"], marker="o")
        plt.title("Efficiency Over Drive Cycles")
        plt.xlabel("Cycle #")
        plt.ylabel("Efficiency")
        plt.grid(True)
        plt.savefig(f"{output_dir}/{name_tag}_efficiency.png")

    if "remaining_capacity_kWh" in df.columns:
        plt.figure()
        plt.plot(x, df["remaining_capacity_kWh"], marker="s", color="green")
        plt.title("Remaining Capacity (kWh)")
        plt.xlabel("Cycle #")
        plt.ylabel("kWh")
        plt.grid(True)
        plt.savefig(f"{output_dir}/{name_tag}_capacity.png")

    if "cycle_count" in df.columns:
        plt.figure()
        plt.plot(x, df["cycle_count"], marker="x", color="red")
        plt.title("Cycle Count Per Simulation Step")
        plt.xlabel("Cycle #")
        plt.ylabel("Cycles")
        plt.grid(True)
        plt.savefig(f"{output_dir}/{name_tag}_cycle_count.png")

def generate_all_plots():
    csv_files = find_latest_csvs()
    for csv_file in csv_files:
        print(f"📊 Generating plots for: {csv_file}")
        plot_simulation_results(csv_file)
    print("✅ Plots saved to /reports/plots/")

if __name__ == "__main__":
    generate_all_plots()
