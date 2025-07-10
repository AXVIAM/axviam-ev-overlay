
import csv

def parse_healing_report(csv_file_path):
    """
    Parses the symbolic healing report and returns structured data.
    Each row is converted into a dictionary of cell metrics.
    """
    parsed_data = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cell_data = {
                "cell_index": int(row["cell_index"]),
                "restored_psi": float(row["restored_psi"]),
                "restored_tension": float(row["restored_tension"]),
            }
            parsed_data.append(cell_data)
    return parsed_data


def run_healing_diagnostics(report_path="reports/healing_report.csv"):
    """
    Wrapper function that parses the healing report and returns structured data.
    This is the callable entry point expected by run_overlay.py
    """
    return parse_healing_report(report_path)
