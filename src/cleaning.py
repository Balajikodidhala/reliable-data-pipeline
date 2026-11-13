import pandas as pd


def clean_data(df):
    """
    Clean customer data and separate invalid records.
    """

    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove extra spaces from text columns
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    # Check required columns
    required = ["customer_id", "name"]

    for column in required:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    # Identify missing required values
    invalid = df[required].isna().any(axis=1)

    for column in required:
        invalid |= df[column].eq("")

    quarantine = df[invalid].copy()
    quarantine["error_reason"] = "Missing required customer information"

    valid = df[~invalid].copy()

    # Identify duplicate customer IDs
    duplicates = valid.duplicated(
        subset=["customer_id"], keep="first"
    )

    duplicate_records = valid[duplicates].copy()
    duplicate_records["error_reason"] = "Duplicate customer ID"

    quarantine = pd.concat(
        [quarantine, duplicate_records],
        ignore_index=True
    )

    # Keep only unique valid records
    cleaned = valid[~duplicates].copy()

    metrics = {
        "input_records": len(df),
        "cleaned_records": len(cleaned),
        "quarantined_records": len(quarantine)
    }

    return cleaned, quarantine, metrics