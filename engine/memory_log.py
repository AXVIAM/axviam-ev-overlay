
import json
import os
from datetime import datetime

MEMORY_LOG_PATH = "runtime/memory_log.json"

def initialize_log():
    if not os.path.exists(MEMORY_LOG_PATH):
        with open(MEMORY_LOG_PATH, "w") as f:
            json.dump({"log": []}, f)

def log_cell_state(cell_index, state_data):
    initialize_log()
    with open(MEMORY_LOG_PATH, "r") as f:
        log = json.load(f)

    timestamped_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "cell_index": cell_index,
        "state": state_data
    }

    log["log"].append(timestamped_entry)

    with open(MEMORY_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def get_log():
    if not os.path.exists(MEMORY_LOG_PATH):
        return []
    with open(MEMORY_LOG_PATH, "r") as f:
        log = json.load(f)
    return log["log"]
