# AXVIAM EV Battery Overlay System

This repository contains the AXVIAM EV Battery Overlay, a non-invasive software system designed to extend the performance, resilience, and lifecycle of electric vehicle (EV) battery packs.

## Overview

The system enables enhanced battery behavior by interfacing with curvature-aligned diagnostics. It dynamically recalibrates energy distribution, optimizes factory load preparation, and maps second-life trajectories — all from a lightweight, curvature-aligned control layer.

## Core Benefits

- 📈 **Range Boost**: Increases per-charge driving range by 14–22% (demonstrated in internal simulations).
- 🏭 **Factory Preparedness**: Optimizes cells during factory calibration with curvature-aligned factory pattern imprinting.
- 🔄 **Second-Life Readiness**: Classifies individual cells by entropy load signature and recommends reuse routing.
- 🧬 **Restorative Breath Mapping**: Each pack is given a healing profile that responds to drive strain in real-time.

## 🔬 Simulation Layer

This release includes a full simulation runner (`sim_runner.py`) that allows EV engineers to preview AXVIAM’s healing impact on performance metrics such as efficiency degradation and extended range. Using real or simulated healing data, the system demonstrates its effect on efficiency and capacity degradation across drive cycles.

- Accepts: Healing data in JSON format
- Outputs: CSV diagnostics logs uniquely tagged per runner (`run_overlay`, `sim_runner`, or `demo_runner`)
- Includes: Realistic degradation modeling, cycle-based capacity loss, and efficiency shifts
- Use case: Prototype validation, internal fleet simulation, and performance benchmarking for EV partners
- Real log conversion: Includes `convert_bms_log.py` to transform BMS-style logs into AXVIAM-compatible healing format

## Key Scripts

- `breath_core.py`: Establishes dynamic restoration loops for each pack under curvature logic.
- `antifragility.py`: Encodes resilience mapping functions for driving adaptation.
- `memory_log.py`: Stores resonance trace per cell during operation and healing.
- `analyzer.py`: Aggregates restoration metrics and prepares summaries.
- `simulator.py`: Synthetic test driver to validate restoration gains and resonance curves.
- `factory_init.py`: Phase 1 module for factory pattern imprinting at the manufacturing level.
- `healing_parser.py`: Prepares reports from restoration cycle outputs.
- `run_overlay.py`: Launch point for the full pipeline.
- `convert_bms_log.py`: Transforms real-world battery telemetry logs into AXVIAM healing format for simulation.
- `sim_runner.py`: Standalone runner to validate real-world gains with healing data.

## 📦 Demo Showcase

A ready-to-run demo is included via `demo_runner.py`, preconfigured with internal factory settings and sample healing diagnostics.

```bash
python demo_runner.py
```

This demonstrates the full overlay process using internal metadata and a realistic diagnostic input, simulating healing gains and outputting a distinct diagnostics file for review.

## 🚀 One-Click Full Evaluation

To run the entire AXVIAM evaluation pipeline — converting real-world telemetry, applying the overlay, and simulating outcomes — use:

```bash
python run_all_dashboard.py
```

This performs:
- 🔄 Real log conversion (`convert_bms_log.py`)
- 🚗 Overlay application and efficiency analysis (`run_overlay.py`)
- 🧪 Full simulated projection across drive cycles (`sim_runner.py`)
- 📄 Output diagnostic files saved to `reports/`, with unique tags
- 📊 Auto-generates summary plots for capacity, efficiency, and cycle count (`generate_plots.py`)

### Running with Your Own Data

1. Place your BMS telemetry log as a JSON file inside the `real_input/` folder (e.g., `real_input/my_bms_log.json`).
2. Run the full evaluation pipeline:

```bash
python run_all_dashboard.py
```

3. Outputs including diagnostics CSVs, plots, and a summary HTML report will be generated inside the `reports/` folder.
4. Open the HTML report to review the visualized results:

```bash
open reports/launch_report.html
```

5. Review the terminal output for a concise summary of key metrics.

## Folder Structure Summary

- `real_input/` — Place your raw telemetry input files here (JSON format). Only sample files included by default.
- `reports/` — Auto-generated folder containing output diagnostics (CSV), plots (PNG), PDF summary, and the HTML report.
- `ev_overlay/`, `engine/` — Core Python modules and scripts powering the overlay and simulations.

## Understanding the Evaluation Summary Metrics

- **Average Efficiency**: Ratio of effective battery capacity utilized vs expected capacity. Higher means better energy retention.
- **Total Miles Driven**: Simulated miles covered during testing.
- **Total Capacity Loss (kWh)**: Estimated degradation in battery capacity after simulated use.
- **Average Remaining Capacity (kWh)**: Estimated usable battery capacity remaining.
- **Miles per Charge**: Projected range per charge based on efficiency improvements.

## Prerequisites

- Python 3.13 or later recommended.
- Required Python packages installed via:

```bash
pip install -r requirements.txt
```

- For best results, use a virtual environment to isolate dependencies.
