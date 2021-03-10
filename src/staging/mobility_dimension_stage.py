import os
import sys
import numpy as np
import pandas as pd

curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')

raw_mobility_csv_path = os.path.join(
    curr_dir, './../../data/raw/2020_CA_Region_Mobility_Report.csv')
raw_mobility_df = pd.read_csv(raw_mobility_csv_path, usecols=["date", "sub_region_1", "sub_region_2", "metro_area", "retail_and_recreation_percent_change_from_baseline", "grocery_and_pharmacy_percent_change_from_baseline",
                                                              "parks_percent_change_from_baseline", "transit_stations_percent_change_from_baseline", "workplaces_percent_change_from_baseline", "residential_percent_change_from_baseline"])
mobility_csv_path = os.path.join(
    curr_dir, './../../data/dimensions/mobility_dimension.csv')


def gen_mobility_df():
    mobility_df = raw_mobility_df.rename(columns={"sub_region_1": "province", "sub_region_2": "subregion", "retail_and_recreation_percent_change_from_baseline": "retail_and_recreation",
                                                  "grocery_and_pharmacy_percent_change_from_baseline": "grocery_and_pharmacy", "parks_percent_change_from_baseline": "parks", "transit_stations_percent_change_from_baseline": "transit_stations",
                                                  "workplaces_percent_change_from_baseline": "workplaces", "residential_percent_change_from_baseline": "residential"})

    mobility_df["metro_area"] = np.where(mobility_df["subregion"] ==
                                         "Ottawa Division", "National Capital Region", "Greater Toronto Area")

    mobility_df = mobility_df[mobility_df["subregion"].isin(
        ["Ottawa Division", "Toronto Division"])]
    mobility_df.insert(0, 'mobility_dim_key', range(len(mobility_df)))

    # Insert Dummy Row
    row = {}
    row['mobility_dim_key'] = -1
    row['province'] = "" 
    row['subregion'] = "" 
    row['metro_area'] = "" 
    row['date'] = "" 
    row['retail_and_recreation'] = 0.0 
    row['grocery_and_pharmacy'] = 0.0
    row['parks'] = 0.0 
    row['transit_stations'] = 0.0 
    row['workplaces'] = 0.0 
    row['residential'] = 0.0 
    mobility_df = mobility_df.append(row, ignore_index=True)


    return mobility_df


def generate_mobility_dim():
    mobility_dimension = gen_mobility_df()
    mobility_dimension.to_csv(mobility_csv_path, encoding='utf-8', index=False)
