import argparse
from fact_stage import generate_fact_dim
from phu_stage import generate_phu_dim
from date_stage import generate_dates_dim
from patient_stage import generate_patients_dim
from mobility_dimension_stage import generate_mobility_dim
from weather_stage import generate_weather_dim
from special_measures_stage import generate_measures_dim


def main():
    parser = argparse.ArgumentParser()
    dimensions = {"date", "patient", "phu",
                  "mobility", "weather", "special_measures", "fact", "all"}
    parser.add_argument(
        '-D', '--dimension', help='dimension to stage', required=True, choices=dimensions)
    args = parser.parse_args()

    if args.dimension == 'date':
        print("Staging Date Dimension 📅")
        generate_dates_dim()
    elif args.dimension == 'patient':
        print("Staging Patient Dimension 🤧")
        generate_patients_dim()
    elif args.dimension == 'mobility':
        print("Staging Mobility Dimension 🏃")
        generate_mobility_dim()
    elif args.dimension == 'phu':
        print("Staging Public Health Unit Dimension 🏥")
        generate_phu_dim()
    elif args.dimension == 'weather':
        print("Staging Weather Dimension 🌤")
        generate_weather_dim()
    elif args.dimension == 'special_measures':
        print("Staging Special Measures Dimension 🔒")
        generate_measures_dim()
    elif args.dimension == 'fact':
        print("Staging Fact Dimension 📝")
        generate_fact_dim()
    elif args.dimension == 'all':
        print("Staging Date Dimension 📅")
        generate_dates_dim()
        print("Staging Patient Dimension 🤧")
        generate_patients_dim()
        print("Staging Mobility Dimension 🏃")
        generate_mobility_dim()
        print("Staging Public Health Unit Dimension 🏥")
        generate_phu_dim()
        print("Staging Weather Dimension 🌤")
        generate_weather_dim()
        print("Staging Special Measures Dimension 🔒")
        generate_measures_dim()
    else:
        return


if __name__ == "__main__":
    main()
