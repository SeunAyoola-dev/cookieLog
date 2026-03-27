from helpers.helpers import build_arg_parser
from processor import process

def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    file, date = args.f, args.d
    process(file, date)

if __name__ == "__main__":
    main()