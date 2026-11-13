import pandas as pd
from src.cleaning import clean_data


def test_clean_data():

    data = {
        "customer_id": [101, 102, 101, 103],
        "name": [" Balaji ", "Rahul", "Balaji", None],
        "city": [" Bengaluru ", "Mysore", "Bengaluru", "Chennai"]
    }

    df = pd.DataFrame(data)

    cleaned, quarantine, metrics = clean_data(df)

    assert len(cleaned) == 2
    assert len(quarantine) == 2

    assert cleaned.iloc[0]["name"] == "Balaji"

    assert metrics["input_records"] == 4
    assert metrics["cleaned_records"] == 2
    assert metrics["quarantined_records"] == 2