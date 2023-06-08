import argparse
import sys

parser = None


def parse_command_line():
    global parser
    parser = argparse.ArgumentParser(
        description="Get all miles walked for a particular month/year from Apple Health XML dump"
    )
    parser.add_argument(
        "--month", metavar="M", type=int, nargs="?", help="Month (1-12)"
    )
    parser.add_argument(
        "--year", metavar="Y", type=int, nargs="?", help="Year (4 digits, e.g. 2023)"
    )
    parser.add_argument(
        "--type", metavar="T", nargs="?", help="Workout type (W==Walking, R=Running)",
    )
    parser.add_argument("--file", metavar="F", nargs="?", help="File to read from")

    args = parser.parse_args()
    if args.year is None:
        print("ERROR: Please provide a '--year' argument")
        parser.print_help()
        sys.exit(1)
    if (args.year < 0) or (args.year > 10000):
        print("ERROR: Year must be a non-negative number < 10000")
        parser.print_help()
        sys.exit(2)
    if args.type is None:
        print("ERROR: Please specify a workout type via the --type argument")
        sys.exit(4)
    if args.month is not None:
        if (args.month < 1) or (args.month > 12):
            print("ERROR: Month must be a number between 1 and 12")
            parser.print_help()
            sys.exit(2)
    if args.file is None:
        print("ERROR: Please provide a '--file' argument")
        parser.print_help()
        sys.exit(3)
    return args.file, args.type, args.year, args.month


def print_usage():
    global parser
    if parser is not None:
        parser.print_help()
