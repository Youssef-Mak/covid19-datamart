import os
import sys
import pandas as pd

curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
raw_phu_csv_path = os.path.join(
        curr_dir, './../../data/raw/confirmed_positive_covid_cases.csv')
phu_dim_csv_path = os.path.join(
        curr_dir, './../../data/dimensions/phu_dimension.csv')

raw_phu_df = pd.read_csv(raw_phu_csv_path)

def filter_phu_locations(phu_df, cols_renamed=False):
    if not cols_renamed:
        phu_df["city"] = phu_df["Reporting_PHU_City"]

    toronto_phu_df = phu_df[phu_df["city"] == "Toronto"]
    durham_phu_df = phu_df[phu_df["city"].isin(["Oshawa", "Whitby",
        "Ajax", "Clarington", "Pickering", "Scugog", "Uxbridge", "Brock"])]
    halton_phu_df = phu_df[phu_df["city"].isin([
        "Burlington", "Oakville", "Milton", "Halton Hills"])]
    peel_phu_df = phu_df[phu_df["city"].isin(["Mississauga", "Brampton", "Caledon"])]
    york_phu_df = phu_df[phu_df["city"].isin(["Aurora", "East Gwillimbury", "Georgina", "King",
        "Markham", "NewMarket", "Newmarket", "Richmond Hill", "Vaughan", "Whitchurch-Stouffville"])]

    gta_df = pd.concat([toronto_phu_df, durham_phu_df,
        halton_phu_df, peel_phu_df, york_phu_df])
    gta_df["general_area"] = "Toronto"

    ottawa_phu_df = phu_df[phu_df["city"] == "Ottawa"]
    ottawa_phu_df["general_area"] = "Ottawa"

    return pd.concat([gta_df, ottawa_phu_df])


def gen_phu_df(phu_df):
    rel_cols = ["Reporting_PHU", "Reporting_PHU_Address", "Reporting_PHU_City", "Reporting_PHU_Postal_Code",
            "Reporting_PHU_Website", "Reporting_PHU_Latitude", "Reporting_PHU_Longitude"]

    rel_df = raw_phu_df.drop(
            columns=[col for col in raw_phu_df if col not in rel_cols])
    phu_df = rel_df.rename(columns={"Reporting_PHU": "phu_name", "Reporting_PHU_Address": "address",
        "Reporting_PHU_City": "city", "Reporting_PHU_Postal_Code": "postal_code",
        "Reporting_PHU_Website": "url", "Reporting_PHU_Longitude": "longitude",
        "Reporting_PHU_Latitude": "latitude"})

    phu_df = filter_phu_locations(phu_df, cols_renamed=True)

    phu_df = phu_df.drop_duplicates()
    phu_df["phu_dim_key"] = range(0, len(phu_df))

    return phu_df


def generate_phu_dim():
    phu_df_columns = [
            "phu_name",
            "address",
            "city",
            "postal_code",
            "province",
            "url",
            "latitude",
            "longitude",
            "phu_dim_key"
            ]
    phu_df = pd.DataFrame(columns=phu_df_columns)

    phu_dim_df = gen_phu_df(phu_df)
    phu_dim_df.to_csv(phu_dim_csv_path, encoding='utf-8', index=False)
