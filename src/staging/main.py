import argparse
from date_stage import generate_dates

def main():
    parser = argparse.ArgumentParser()
    dimensions = {"date", "patient", "phu", "mobility", "weather", "special_measures"}
    parser.add_argument('-D', '--dimension', help='dimension to stage', required=True, choices=dimensions)
    args = parser.parse_args()

    if args.dimension == 'date':
        generate_dates()
    else:
        return

if __name__ == "__main__":
    main()
