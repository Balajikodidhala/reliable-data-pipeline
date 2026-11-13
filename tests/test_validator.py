import pandas as pd
from src.validator import validate_data


def test_validate_data():
    data = {
        "name": ["Balaji", "Rahul", "Priya", "Balaji"],
        "age": [23, 24, None, 23],
        "city": ["Bengaluru", "Mysore", "Hyderabad", "Bengaluru"]
    }

    df = pd.DataFrame(data)

    result = validate_data(df)

    assert result["total_records"] == 4
    assert result["duplicate_records"] == 1
    assert result["missing_values"]["age"] == 1

    print("All validation checks passed!")