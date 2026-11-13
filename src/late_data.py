import pandas as pd


def detect_late_data(df, event_time_column, ingestion_time_column):
    """
    Detect records that arrive more than 24 hours after the event.
    """

    df = df.copy()

    df[event_time_column] = pd.to_datetime(
        df[event_time_column], utc=True
    )

    df[ingestion_time_column] = pd.to_datetime(
        df[ingestion_time_column], utc=True
    )

    df["delay_hours"] = (
        df[ingestion_time_column] - df[event_time_column]
    ).dt.total_seconds() / 3600

    df["is_late"] = df["delay_hours"] > 24
    return df

def partition_by_event_date(df, event_time_column, output_dir):
    """
    Partition records into folders based on event date.
    """

    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df = df.copy()

    df[event_time_column] = pd.to_datetime(
        df[event_time_column], utc=True
    )

    df["event_date"] = (
        df[event_time_column].dt.strftime("%Y-%m-%d")
    )

    for event_date, group in df.groupby("event_date"):
        date_folder = output_path / f"event_date={event_date}"
        date_folder.mkdir(parents=True, exist_ok=True)

        group.to_csv(
            date_folder / "data.csv",
            index=False
        )
    return output_path
    return output_path