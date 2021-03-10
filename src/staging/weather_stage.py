import os
import sys
import pandas as pd

curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')

raw_climate_ottawa_csv_path = os.path.join(curr_dir, './../../data/raw/Ottawa_daily_climate.csv')
raw_climate_toronto_csv_path = os.path.join(curr_dir, './../../data/raw/Toronto_daily_climate.csv')

raw_climate_ottawa_df = pd.read_csv(raw_climate_ottawa_csv_path, usecols=["Date/Time", "Station Name", "Max Temp (°C)", "Min Temp (°C)", "Total Precip (mm)"])
raw_climate_toronto_df = pd.read_csv(raw_climate_toronto_csv_path, usecols=["Date/Time", "Station Name", "Max Temp (°C)", "Min Temp (°C)", "Total Precip (mm)"])

weather_csv_path = os.path.join(curr_dir, './../../data/dimensions/weather_dimension.csv')

def generate_weather_df():
    raw_climate_ottawa_df["City"] = "Ottawa"
    raw_climate_toronto_df["City"] = "Toronto"
    weather_df = raw_climate_ottawa_df.append(raw_climate_toronto_df)
    weather_df.insert(0, 'weather_dim_key', range(len(weather_df)))

    return weather_df.rename(columns={"Date/Time": "date", "Max Temp (°C)": "daily_high_temperature", "Min Temp (°C)": "daily_low_temperature", "Total Precip (mm)": "precipitation"})

def generate_weather_dim():
    weather_dimension = generate_weather_df()
    weather_dimension.to_csv(weather_csv_path, encoding='utf-8', index=False)
