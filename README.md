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























Reliable Data Pipeline

1. Project Overview

The Reliable Data Pipeline is a Python-based data engineering project designed to process customer data reliably and efficiently.

The pipeline handles data ingestion, cleaning, validation, duplicate detection, late-arriving data, and event-date partitioning.

It separates valid records from invalid records, tracks processed files, and generates execution reports to improve data quality, reliability, and traceability.

2. Features

- Data Ingestion: Reads customer data from CSV files.
- Data Cleaning: Standardizes column names, removes unnecessary whitespace, and handles empty values.
- Data Validation: Checks required fields and identifies invalid records.
- Duplicate Detection: Uses SHA-256 hashing to identify previously processed files.
- Quarantine Handling: Separates invalid records for further investigation.
- Late Data Detection: Identifies records arriving after the expected processing time.
- Event-Date Partitioning: Organizes records into folders based on event dates.
- Processing Manifest: Maintains a record of previously processed files.
- Execution Reports: Generates JSON reports containing processing status and record counts.
- Logging and Error Tracking: Maintains logs to help monitor pipeline execution.
- Automated Testing: Uses Pytest to verify pipeline functionality.

3. Project Architecture

The pipeline follows this processing workflow:

              Input CSV File
                    |
                    v
              Data Ingestion
                    |
                    v
          Duplicate File Detection
             (SHA-256 Hash)
                    |
                    v
             Data Cleaning
                    |
                    v
            Data Validation
                    |
             +------+------+
             |             |
             v             v
        Valid Records   Invalid Records
             |             |
             v             v
       Processed Data   Quarantine
             |
             v
      Late Data Detection
             |
             v
      Event-Date Partitioning
             |
             v
          Output Files
             |
       +-----+------+
       |            |
       v            v
   Run Reports    Logs

Architecture Note: The current implementation uses cleaned and quarantined outputs. Separate raw, validated, and curated storage zones can be added as an extension to meet the full object-storage architecture requirement.

4. Project Folder Structure

reliable-data-pipeline/
│
├── data/
│   └── customers.csv
│
├── output/
│   ├── cleaned_customers.csv
│   ├── quarantine_customers.csv
│   ├── manifest.json
│   ├── run_report_*.json
│   ├── partitions/
│   └── logs/
│
├── src/
│   ├── pipeline.py
│   ├── cleaning.py
│   ├── deduplication.py
│   └── late_data.py
│
├── tests/
│   ├── test_pipeline.py
│   ├── test_partition.py
│   └── test_deduplication.py
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md

Main Modules:

- "pipeline.py" – Controls the overall pipeline execution.
- "cleaning.py" – Handles data cleaning and validation.
- "deduplication.py" – Detects duplicate files using SHA-256 hashing.
- "late_data.py" – Handles late-arriving data detection and event-date partitioning.

Testing: The project uses Pytest to validate the implemented functionality.   