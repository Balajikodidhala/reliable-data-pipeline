import pandas as pd
from src.storage import save_outputs


def test_save_outputs(tmp_path):

    cleaned = pd.DataFrame({
        "customer_id": [101, 102],
        "name": ["Balaji", "Rahul"]
    })

    quarantine = pd.DataFrame({
        "customer_id": [103],
        "name": [None],
        "error_reason": ["Missing required customer information"]
    })

    result = save_outputs(
        cleaned,
        quarantine,
        tmp_path
    )

    assert tmp_path.joinpath(
        "cleaned_customers.csv"
    ).exists()

    assert tmp_path.joinpath(
        "quarantine_customers.csv"
    ).exists()

    saved_data = pd.read_csv(result["cleaned_file"])

    assert len(saved_data) == 2