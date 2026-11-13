from src.ingestion import load_data


def test_load_data():
    df = load_data("data/customers.csv")

    assert len(df) == 5
    assert "customer_id" in df.columns
    assert "name" in df.columns

    print("CSV ingestion successful!")