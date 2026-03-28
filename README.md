# Most Active Cookie Log Processor

A Python CLI tool to find the most active cookies from a log file for a specific date.

## Overview

This tool processes a CSV log file containing cookies and timestamps. It identifies which cookie(s) appeared most frequently on a target date.

## Features

- **Efficient Parsing**: Processes logs and terminates early if it moves past the target date (assuming log file is sorted by datetime (UTC) descending).
- **Robust Validation**: Validates file is present and provided date formats.
- **Production Logging**: Integrated with Python's `logging` module to provide visibility into processing steps
- **Thorough Testing**: Unit & Feature testing to ensure the tool works as expected

## Prerequisites

- Python 3.6+
- **Development Dependencies**: `pytest` and `parameterized` (for running tests).

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd cookieLog
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required dependencies for development:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line using `main.py`:

```bash
python3 main.py -f <log_file> -d <YYYY-MM-DD>
```

### Arguments

- `-f`: Path to the CSV log file (required).
- `-d`: Target date in `YYYY-MM-DD` format (required).

### Example

```bash
python3 main.py -f cookie_log.csv -d 2018-12-09
```

**Output:**
```text
2026-03-27 14:07:03 [INFO] __main__: Processing cookie logs for file: cookie_log.csv and date: 2018-12-09
2026-03-27 14:07:03 [INFO] processor: Found 1 most active cookie(s) for 2018-12-09
AtY0laUfhglK3lC7
```

## Input File Format

The log file should be a CSV with a header. Each line should contain a cookie identifier and a timestamp, separated by a comma.

```csv
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
```

## Logging Information

Logs are output  using the following format:
`YYYY-MM-DD HH:MM:SS [LEVEL] logger_name: message`

- **INFO**: General processing milestones and results.
- **DEBUG**: Granular details like line-by-line parsing and early exit triggers.
- **WARNING**: Alerts for malformed lines in the input file.
- **ERROR**: Critical failures like missing files or invalid arguments.

## Project Structure

- `main.py`: Entry point 
- `processor.py`: Core logic for parsing and finding active cookies.
- `helpers/helpers.py`: CLI argument parsing construction and validation
- `cookie_log.csv`: Sample log file.
- `requirements.txt`: Project dependencies for development and testing.
- `test/`: Directory containing project tests.

## Running Tests

The project uses `pytest` and `parameterized` for testing. You can run the tests using:


```bash
python3 -m pytest
```
