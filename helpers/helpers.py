from datetime import datetime
import argparse
import os

DATE_FORMAT = '%Y-%m-%d'
def parse_date(value):
    """Validate and return date string in YYYY-MM-DD format"""
    try:
        datetime.strptime(value, DATE_FORMAT)
        return value

    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: {value}. Must be YYYY-MM-DD"
        )

def parse_file(value):

    if not os.path.exists(value):
        raise argparse.ArgumentTypeError(
            f"File does not exist: {value}"
        )
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError(
            f"Not a valid file: {value}"
        )

    return value

def build_arg_parser():
    parser = argparse.ArgumentParser(description='Most Active Cookie')

    parser.add_argument("-f", required=True, help="File with cookies", metavar="FILE", type = parse_file)
    parser.add_argument("-d", required=True, help="Date you want to query", metavar="DATE", type = parse_date)
    return parser