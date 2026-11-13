import pandas as pd
from pathlib import Path


def load_data(file_path):
    """
    Load raw CSV data into a DataFrame.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported")

    df = pd.read_csv(path)

    return df