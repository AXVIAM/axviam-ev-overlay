import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'engine'))
import json
from breath_core import generate_breath_signature

def initialize_factory_pack(pack_id, metadata_path):
    """
    Initializes a battery pack at the factory level with its symbolic signature imprint.

    Args:
        pack_id (str): Unique identifier for the battery pack.
        metadata_path (str): Path to the JSON metadata file containing initial factory calibration data.

    Returns:
        dict: Factory-initialized pack data with symbolic imprint.
    """
    with open(metadata_path, 'r') as file:
        metadata = json.load(file)
        metadata.setdefault("capacity_kWh", 75)  # Default to 75 kWh if not present

    imprint = generate_breath_signature(pack_id, metadata)

    factory_initialized = {
        "pack_id": pack_id,
        "factory_metadata": metadata,
        "symbolic_imprint": imprint,
        "status": "factory_initialized"
    }

    return factory_initialized


def initialize_factory():
    """
    Initializes a default factory pack for use in the EV overlay pipeline.

    Returns:
        dict: Initialized pack dictionary.
    """
    # Use a default pack ID and a sample metadata dictionary
    pack_id = "default_pack_001"
    metadata = {
        "cell_count": 96,
        "factory_voltage_range": [300, 400],
        "initial_temperature_C": 25,
        "manufacture_date": "2025-07-09",
        "chemical_profile": "NMC-532",
        "capacity_kWh": 75,
    }

    imprint = generate_breath_signature(pack_id, metadata)

    return {
        "pack_id": pack_id,
        "factory_metadata": metadata,
        "symbolic_imprint": imprint,
        "status": "factory_initialized"
    }
