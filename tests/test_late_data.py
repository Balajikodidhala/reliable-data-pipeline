import pandas as pd

from src.late_data import detect_late_data


def test_detect_late_data():

    df = pd.DataFrame({
        "event_time": [
            "2026-01-01 00:00:00",
            "2026-01-01 00:00:00"
        ],
        "ingestion_time": [
            "2026-01-01 12:00:00",
            "2026-01-02 02:00:00"
        ]
    })

    result = detect_late_data(
        df,
        "event_time",
        "ingestion_time"
    )

    assert result["is_late"].tolist() == [False, True]

    print("Late data detection successful!")