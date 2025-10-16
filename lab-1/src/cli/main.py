import argparse
import datetime as dt
from config.settings import settings
from data_io.data_loader import DataLoader  # Changed from data_io.data_loader
from core.filters import record_filter
from core.calculator import calculator


def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze JSON records")
    parser.add_argument("--file", help="Input JSON file path")
    parser.add_argument("--thres", type=float, help="Threshold value")
    parser.add_argument("--all", action="store_true",
                        help="Include all records regardless of status")
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Update settings from command line
    if args.file:
        settings.data_path = args.file
    if args.thres is not None:
        settings.default_threshold = args.thres
    if args.all:
        settings.filter_mode = "ALL"

    # Load and process data
    loader = DataLoader()
    records = loader.load_records()
    filtered_records = record_filter.filter_records(records)
    result = calculator.calculate_statistics(filtered_records)

    # Output results
    timestamp = dt.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    print(result.format_summary(timestamp))

    return result


if __name__ == "__main__":
    main()