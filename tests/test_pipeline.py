import pandas as pd

from src.pipeline import run_pipeline


def test_complete_pipeline(tmp_path):

    # Create sample input data
    input_file = tmp_path / "customers.csv"

    data = pd.DataFrame({
        "customer_id": [101, 102, 101, 103],
        "name": ["Balaji", "Rahul", "Balaji", None],
        "city": [
            "Bengaluru",
            "Mysore",
            "Bengaluru",
            "Chennai"
        ],
        "event_time": [
            "2026-11-10 10:00:00",
            "2026-11-10 11:00:00",
            "2026-11-11 12:00:00",
            "2026-11-11 13:00:00"
        ],
        "ingestion_time": [
            "2026-11-10 10:05:00",
            "2026-11-10 11:05:00",
            "2026-11-12 12:00:00",
            "2026-11-11 13:05:00"
        ]
    })

    data.to_csv(input_file, index=False)
    # Run complete pipeline
    result = run_pipeline(
        str(input_file),
        str(tmp_path / "output")
        )
    assert (
    tmp_path / "output" / "partitions" /
    "event_date=2026-11-10"
    ).exists()
    # Check results
    assert result["metrics"]["input_records"] == 4
    assert result["metrics"]["cleaned_records"] == 2
    assert result["metrics"]["quarantined_records"] == 2

    assert result["output_files"]["cleaned_file"]
    assert result["output_files"]["quarantine_file"]

    # Test duplicate file detection
    second_result = run_pipeline(
        str(input_file),
        str(tmp_path / "output")
    )

    assert second_result["status"] == "skipped"
    assert second_result["reason"] == "Duplicate file already processed"