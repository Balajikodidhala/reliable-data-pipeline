from src.deduplication import (
    is_duplicate,
    mark_file_processed
)


def test_duplicate_file_detection(tmp_path):

    csv_file = tmp_path / "customers.csv"
    manifest = tmp_path / "manifest.json"

    csv_file.write_text(
        "id,name\n1,Balaji\n",
        encoding="utf-8"
    )

    assert is_duplicate(csv_file, manifest) is False

    mark_file_processed(
        csv_file,
        manifest,
        "run_001"
    )

    assert is_duplicate(csv_file, manifest) is True


def test_modified_file_is_not_duplicate(tmp_path):

    csv_file = tmp_path / "customers.csv"
    manifest = tmp_path / "manifest.json"

    csv_file.write_text(
        "id,name\n1,Balaji\n",
        encoding="utf-8"
    )

    mark_file_processed(
        csv_file,
        manifest,
        "run_001"
    )

    csv_file.write_text(
        "id,name\n2,Rahul\n",
        encoding="utf-8"
    )

    assert is_duplicate(csv_file, manifest) is False