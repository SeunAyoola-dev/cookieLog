import logging
from helpers import build_arg_parser
from processor import process

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    file, date = args.f, args.d
    logger.info(f"Processing cookie logs for file: {file} and date: {date}")
    try:
        process(file, date)
    except Exception as e:
        logger.error(f"An error occurred during processing: {e}")
        exit(1)

if __name__ == "__main__":
    main()