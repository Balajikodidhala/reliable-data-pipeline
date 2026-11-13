from src.late_data import (
    detect_late_data,
    partition_by_event_date
)
from src.deduplication import (
    is_duplicate,
    mark_file_processed
)

from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4
from pathlib import Path

from src.ingestion import load_data
from src.validator import validate_data
from src.cleaning import clean_data
from src.storage import save_outputs
from src.monitoring import setup_logger, save_run_report


def run_pipeline(input_file, output_dir):

    run_id = str(uuid4())
    start_time = perf_counter()
    started_at = datetime.now(timezone.utc).isoformat()

    logger = setup_logger(
        Path(output_dir) / "logs",
        run_id
    )

    report = {
        "run_id": run_id,
        "status": "running",
        "started_at": started_at,
        "input_file": str(input_file),
        "metrics": {},
        "error": None
    }

    logger.info("Pipeline started")
    try:
        # Step 0: Duplicate Detection
        manifest_path = Path(output_dir) / "manifest.json"

        if is_duplicate(input_file, manifest_path):
            report["status"] = "skipped"
            report["reason"] = "Duplicate file already processed"
            logger.warning("Duplicate file detected. Skipping.")
            return report
        # Step 1: Ingestion
        raw_data = load_data(input_file)
        if "event_time" in raw_data.columns:
            # Step 1.1: Add ingestion timestamp
            raw_data["ingestion_time"] = datetime.now(
                timezone.utc
            )

            # Step 1.2: Detect late-arriving records
            raw_data = detect_late_data(
                raw_data,
                "event_time",
                "ingestion_time"
            )

            logger.info("Late-arriving data detection completed")
        else:
            logger.info(
                "Late-arriving data detection skipped: "
                "event_time column not found"
            )
        logger.info("Data ingestion completed")

        # Step 2: Validation
        validation_report = validate_data(raw_data)
        logger.info("Data validation completed")

        # Step 3: Cleaning
        cleaned, quarantine, metrics = clean_data(raw_data)
        logger.info("Data cleaning completed")
        # Step 3.1: Partition cleaned data by event date
        if "event_time" in cleaned.columns:
            partitioned_data = partition_by_event_date(
                df=cleaned,
                event_time_column="event_time",
                output_dir=f"{output_dir}/partitions"
            )
            logger.info("Data partitioning completed")

        # Step 4: Storage
        output_files = save_outputs(
            cleaned,
            quarantine,
            output_dir
        )
        logger.info("Data storage completed")

        # Record metrics
        report["metrics"] = {
            **metrics,
            "validation": {
                "total_records": int(
                    validation_report["total_records"]
                ),
                "duplicate_records": int(
                    validation_report["duplicate_records"]
                ),
                "missing_values": {
                    key: int(value)
                    for key, value in
                    validation_report["missing_values"].items()
                }
            }
        }

        report["output_files"] = output_files
        report["status"] = "success"

        mark_file_processed(
            input_file,
            manifest_path,
            run_id
        )

        logger.info("Pipeline completed successfully")

        return report

    except Exception as error:

        report["status"] = "failed"
        report["error"] = {
            "type": type(error).__name__,
            "message": str(error)
        }

        logger.exception("Pipeline execution failed")

        raise

    finally:
        report["finished_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        report["duration_seconds"] = round(
            perf_counter() - start_time, 4
        )

        report_file = save_run_report(
            report,
            output_dir,
            run_id
        )
        report["report_file"]=report_file

        logger.info(f"Execution report saved: {report_file}")