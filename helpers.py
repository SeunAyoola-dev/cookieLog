import logging
import argparse

logger = logging.getLogger(__name__)

DATE_FORMAT = "YYYY-MM-DD"

def parse_date(value: str) -> str:
    """Validate and return date string in YYYY-MM-DD format."""
    parts = value.split("-")

    if (
        len(parts) != 3
        or len(parts[0]) != 4
        or len(parts[1]) != 2
        or len(parts[2]) != 2
        or not all(part.isdigit() for part in parts)
    ):
        logger.error(f"Invalid date format provided: {value}")
        raise argparse.ArgumentTypeError(
            f"Invalid date format: '{value}'. Must be {DATE_FORMAT}"
        )

    return value

def parse_file(value):
    try:
        open(value).close()

    except FileNotFoundError:
        logger.error(f"File not found: {value}")
        raise argparse.ArgumentTypeError(
            f"File not found: {value}"
        )
    except IsADirectoryError:
        logger.error(f"Path is not a file: {value}")
        raise argparse.ArgumentTypeError(
            f"Path is not a file: {value}"
        )

    return value

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Most Active Cookie')

    parser.add_argument("-f", required=True, help="File with cookies", metavar="FILE", type = parse_file)
    parser.add_argument("-d", required=True, help="Date you want to query", metavar="DATE", type = parse_date)
    return parser