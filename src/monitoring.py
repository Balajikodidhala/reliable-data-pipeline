import json
import logging
from pathlib import Path


def setup_logger(log_dir, run_id):
    """
    Create a logger for each pipeline execution.
    """

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(f"pipeline.{run_id}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(
            log_path / f"{run_id}.log",
            encoding="utf-8"
        )

        console_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def save_run_report(report, output_dir, run_id):
    """
    Save execution details as a JSON report.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    report_file = output_path / f"run_report_{run_id}.json"

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, default=str)

    return str(report_file)