import logging
from helpers.helpers import parse_date
logger = logging.getLogger(__name__)

def parse_input_file(file_path, target_date):
    logger.debug(f"[INFO] Parsing input file: {file_path}")
    counts = {}

    with open(file_path, "r") as file:
        next(file)

        for line_num, line in enumerate(file):
            try:
                cookie, timestamp = line.strip().split(",")
                date = timestamp.split("T")[0]

                parse_date(date)

                if date == target_date:
                    counts[cookie] = counts.get(cookie, 0) + 1


                elif date < target_date:
                    logger.debug(f"[INFO] Early exit at line {line_num} because date {date} < target_date {target_date}")
                    break # break early

            except Exception as e:
                logger.warning(f"[ERROR] Skipping malformed line {line_num}: {line.strip()} - {e}")
                continue


    return counts

def find_most_active_cookies(counts):
    if not counts:
        logger.debug("[WARNING] find_most_active_cookies called with empty counts")
        return []

    most_active_count = max(counts.values())
    return [cookie for cookie, count in counts.items() if count == most_active_count]

def process(file, date):
    logger.debug(f"[INFO] Starting processing for date: {date}")
    counts = parse_input_file(file, date)
    
    if not counts:
        logger.warning(f"[WARNING] No cookies found for date: {date}")


    most_active_cookies = find_most_active_cookies(counts)
    logger.info(f"[INFO] Found {len(most_active_cookies)} most active cookie(s) for {date}")

    for cookie in most_active_cookies:
        print(cookie)

