import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone


def calculate_file_hash(file_path):
    """Generate SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_manifest(manifest_path):
    """Load previously processed file records."""

    path = Path(manifest_path)

    if not path.exists():
        return {"processed_files": {}}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_duplicate(file_path, manifest_path):
    """Check whether a file was already processed."""

    file_hash = calculate_file_hash(file_path)
    manifest = load_manifest(manifest_path)

    return file_hash in manifest["processed_files"]


def mark_file_processed(file_path, manifest_path, run_id):
    """Record a successfully processed file."""

    file_hash = calculate_file_hash(file_path)
    manifest = load_manifest(manifest_path)

    manifest["processed_files"][file_hash] = {
        "file_name": Path(file_path).name,
        "run_id": run_id,
        "processed_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    path = Path(manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = path.with_suffix(path.suffix + ".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=4)

    temp_path.replace(path)