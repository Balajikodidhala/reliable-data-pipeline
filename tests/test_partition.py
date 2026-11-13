import pandas as pd
from src.late_data import partition_by_event_date


def test_partition_by_event_date(tmp_path):
    df = pd.DataFrame({
        "event_time": [
            "2026-01-01 10:00:00",
            "2026-01-02 12:00:00",
            "2026-01-01 15:00:00"
        ]
    })

    output = partition_by_event_date(
        df,
        "event_time",
        tmp_path
    )

    assert (tmp_path / "event_date=2026-01-01").exists()
    assert (tmp_path / "event_date=2026-01-02").exists()