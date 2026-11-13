import pandas as pd
from pathlib import Path


def save_outputs(cleaned, quarantine, output_dir):
    """
    Save cleaned and quarantined data separately.
    """

    output_path = Path(output_dir)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Define output file paths
    cleaned_file = output_path / "cleaned_customers.csv"
    quarantine_file = output_path / "quarantine_customers.csv"

    # Save cleaned records
    cleaned.to_csv(cleaned_file, index=False)

    # Save invalid records
    quarantine.to_csv(quarantine_file, index=False)

    return {
        "cleaned_file": str(cleaned_file),
        "quarantine_file": str(quarantine_file)
    }