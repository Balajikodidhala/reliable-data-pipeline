import pandas as pd


def validate_data(df):
    """
    Validate the input DataFrame.
    """

    report = {}

    # Check total records
    report["total_records"] = len(df)

    # Check missing values
    report["missing_values"] = df.isnull().sum().to_dict()

    # Check duplicate records
    report["duplicate_records"] = int(df.duplicated().sum())

    # Check empty records
    report["empty_records"] = int(df.isnull().all(axis=1).sum())

    return report