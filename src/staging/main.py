import argparse
from phu_stage import generate_phu_dim
from date_stage import generate_dates_dim
from patient_stage import generate_patients_dim
from mobility_dimension_stage import generate_mobility_dim
from weather_stage import generate_weather_dim
from special_measures_stage import generate_measures_dim


def main():
    parser = argparse.ArgumentParser()
    dimensions = {"date", "patient", "phu",
                  "mobility", "weather", "special_measures"}
    parser.add_argument(
        '-D', '--dimension', help='dimension to stage', required=True, choices=dimensions)
    args = parser.parse_args()

    if args.dimension == 'date':
        generate_dates_dim()
    elif args.dimension == 'patient':
        generate_patients_dim()
    elif args.dimension == 'mobility':
        generate_mobility_dim()
    elif args.dimension == 'phu':
        generate_phu_dim()
    elif args.dimension == 'weather':
        generate_weather_dim()
    elif args.dimension == 'special_measures':
        generate_measures_dim()
    else:
        return


if __name__ == "__main__":
    main()
