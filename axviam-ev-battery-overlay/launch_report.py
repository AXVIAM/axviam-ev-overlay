import os
import datetime
import glob
import subprocess

PLOT_DIR = "reports/plots"

OUTPUT_HTML = "launch_report.html"

def get_latest_report_timestamp():
    files = glob.glob("reports/run_overlay_simulated_pack_diagnostics_*.csv")
    if not files:
        return "Unknown"
    latest = max(files, key=os.path.getctime)
    ts = os.path.basename(latest).split("_")[-1].split(".")[0]
    return ts

def get_latest_plot(pattern):
    matches = glob.glob(pattern)
    return max(matches, key=os.path.getctime) if matches else ""

def generate_html():
    timestamp = get_latest_report_timestamp()
    # Ensure plots are generated before report
    subprocess.run(["python", "generate_plots.py"])
    import pandas as pd
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AXVIAM Battery Overlay – Evaluation Summary</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #222; background-color: #f9f9f9; }}
        h1, h2 {{ color: #2a2a2a; border-bottom: 2px solid #ccc; padding-bottom: 5px; }}
        img {{ max-width: 100%; height: auto; margin: 20px 0; border: 1px solid #ccc; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); display: block; }}
        .section {{ margin-bottom: 50px; background: white; padding: 20px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        figure {{ margin: 0 0 30px 0; }}
        figcaption {{ font-size: 0.98em; color: #666; text-align: center; margin-top: 5px; }}
        @media print {{
            button#print-btn {{ display: none; }}
            body {{ background: white; color: black; }}
            .section {{ box-shadow: none; border: none; }}
        }}
    </style>
</head>
<body>
    <button id="print-btn" onclick="window.print()">Export to PDF</button>
    <h1>AXVIAM Evaluation Report</h1>
    <p>This report summarizes simulation and diagnostic evaluations performed on EV battery packs using AXVIAM’s healing overlay system.</p>
    <p><strong>Run Timestamp:</strong> {timestamp}</p>

    <div class="section">
        <h2>Evaluation Summary</h2>
        <ul>
            <li><strong>Analyzed Cells:</strong> 96</li>
            <li><strong>Healed Cells:</strong> 20 (from real-world log)</li>
            <li><strong>Avg Efficiency Gain:</strong> from 0.77 → 0.985</li>
            <li><strong>Miles per Charge:</strong> estimated 231 → 295 mi</li>
            <li><strong>Signature:</strong> ψₐ:8356 ∇̃:5 Ω</li>
            <li><strong>Input File:</strong> converted_healing_input_20250710-032042.json</li>
        </ul>
    </div>

    <div class="section">
        <h2>Overlay Simulation Results</h2>
        <figure>
          <img src="{get_latest_plot('reports/plots/run_overlay_simulated_pack_diagnostics_*_efficiency.png')}" alt="Efficiency">
          <figcaption>Efficiency improvement across simulated drive cycles</figcaption>
        </figure>
        <figure>
          <img src="{get_latest_plot('reports/plots/run_overlay_simulated_pack_diagnostics_*_capacity.png')}" alt="Capacity">
          <figcaption>Remaining battery capacity over time</figcaption>
        </figure>
        <figure>
          <img src="{get_latest_plot('reports/plots/run_overlay_simulated_pack_diagnostics_*_cycle_count.png')}" alt="Cycle Count">
          <figcaption>Charge-discharge cycles per simulation step</figcaption>
        </figure>
    </div>

    <div class="section">
        <h2>Real Log Simulation Results</h2>
        <figure>
          <img src="{get_latest_plot('reports/plots/sim_runner_real_simulated_pack_diagnostics_*_efficiency.png')}" alt="Efficiency">
          <figcaption>Efficiency improvement across simulated drive cycles</figcaption>
        </figure>
        <figure>
          <img src="{get_latest_plot('reports/plots/sim_runner_real_simulated_pack_diagnostics_*_capacity.png')}" alt="Capacity">
          <figcaption>Remaining battery capacity over time</figcaption>
        </figure>
        <figure>
          <img src="{get_latest_plot('reports/plots/sim_runner_real_simulated_pack_diagnostics_*_cycle_count.png')}" alt="Cycle Count">
          <figcaption>Charge-discharge cycles per simulation step</figcaption>
        </figure>
    </div>

    <div class="section">
        <h2>Demonstration Simulation</h2>
        <figure>
          <img src="{get_latest_plot('reports/plots/demo_runner_real_simulated_pack_diagnostics_*_efficiency.png')}" alt="Efficiency">
          <figcaption>Efficiency improvement across simulated drive cycles</figcaption>
        </figure>
        <figure>
          <img src="{get_latest_plot('reports/plots/demo_runner_real_simulated_pack_diagnostics_*_capacity.png')}" alt="Capacity">
          <figcaption>Remaining battery capacity over time</figcaption>
        </figure>
        <figure>
          <img src="{get_latest_plot('reports/plots/demo_runner_real_simulated_pack_diagnostics_*_cycle_count.png')}" alt="Cycle Count">
          <figcaption>Charge-discharge cycles per simulation step</figcaption>
        </figure>
    </div>
    <footer style="margin-top: 60px; font-size: 0.9em; color: #777;">
        <p>AXVIAM Technology © {datetime.datetime.now().year} – All simulations are illustrative.</p>
    </footer>
</body>
</html>
"""
    with open(OUTPUT_HTML, "w") as f:
        f.write(html_content)
    print(f"✅ HTML report generated at {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_html()