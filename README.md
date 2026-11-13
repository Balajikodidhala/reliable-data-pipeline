Reliable Data Pipeline

Project Overview

The Reliable Data Pipeline is a Python-based project designed to process customer data reliably through data cleaning, validation, duplicate-file detection, and structured output generation.

Features

- Data ingestion from CSV files
- Data cleaning and standardization
- Data validation
- Separation of valid and quarantined records
- Duplicate-file detection using SHA-256 hashing
- Processing manifest to track processed files
- Late-arriving data detection
- Event-date partitioning when event-time data is available
- Pipeline execution reports
- Logging and error tracking
- Automated tests using Pytest

Project Structure

reliable-data-pipeline/
├── data/
├── output/
├── src/
├── tests/
├── README.md
└── requirements.txt

Technologies Used

- Python
- Pandas
- Pytest
- JSON
- CSV
- SHA-256

Setup

Clone or download the project and navigate to its directory.

Install dependencies:

pip install -r requirements.txt

Run the Pipeline

python -c "from src.pipeline import run_pipeline; print(run_pipeline('data/customers.csv', 'output'))"

Run Tests

python -m pytest -v

Output

The pipeline generates:

- Cleaned customer data
- Quarantined customer records
- Processing manifest
- Pipeline execution reports
- Log files
- Event-date partition folders when applicable

Project Goal

To build a reliable and testable data pipeline that handles data quality, duplicate processing, late-arriving data, and execution tracking.     