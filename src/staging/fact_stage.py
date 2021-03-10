import os
import sys
import time
import code
import pandas as pd
from phu_stage import filter_phu_locations

curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
raw_phu_csv_path = os.path.join(
        curr_dir, './../../data/raw/confirmed_positive_covid_cases.csv')
date_dim_csv_path = os.path.join(
        curr_dir, './../../data/dimensions/date_dimension.csv')
patient_dim_csv_path = os.path.join(
        curr_dir, './../../data/dimensions/patient_dimension.csv')
phu_dim_csv_path = os.path.join(
        curr_dir, './../../data/dimensions/phu_dimension.csv')
weather_dim_csv_path = os.path.join(
        curr_dir, './../../data/dimensions/weather_dimension.csv')
special_measures_csv_path = os.path.join(
        curr_dir, './../../data/dimensions/special_measures_dimension.csv')
mobility_dim_csv_path = os.path.join(
        curr_dir, './../../data/dimensions/mobility_dimension.csv')
fact_csv_path = os.path.join(
        curr_dir, './../../data/dimensions/fact_dimension.csv')

special_measures_df = pd.read_csv(special_measures_csv_path)
mobility_dim_df = pd.read_csv(mobility_dim_csv_path)
weather_dim_df = pd.read_csv(weather_dim_csv_path)
patient_dim_df = pd.read_csv(patient_dim_csv_path)
date_dim_df = pd.read_csv(date_dim_csv_path)
phu_dim_df = pd.read_csv(phu_dim_csv_path)
raw_phu_df = pd.read_csv(raw_phu_csv_path)

date_fk_dict = pd.Series(date_dim_df.date_dim_key.values,
        index=date_dim_df.full_date).to_dict()
phu_fk_addr_dict = pd.Series(
        phu_dim_df.phu_dim_key.values, index=phu_dim_df.address).to_dict()


def get_date_fk(full_date):
    if full_date == "nan":
        return -1
    return int(date_fk_dict.get(full_date, -1))


def get_patient_fk(age_group, gender, case_info, outbreak):
    outbreak = True if (outbreak == "Yes") else (
            False if (outbreak == "No") else "")
    result_match = patient_dim_df[patient_dim_df["age_group"] == age_group]
    result_match = result_match[result_match["gender"] == gender]
    result_match = result_match[result_match["acquisition_group"] == case_info]
    if outbreak == "":
        result_match = result_match[result_match["outbreak_related"].isnull(
            ) == True]
    else:
        result_match = result_match[result_match["outbreak_related"] == outbreak]
    match = result_match.head(1)
    try:
        return match["patient_dim_key"].values[0]
    except:
        code.interact(local=dict(globals(), **locals()))


def get_phu_fk(reporting_phu_address):
    return phu_fk_addr_dict.get(reporting_phu_address)


def get_phu_city(reporting_phu_address):
    result_match = phu_dim_df[phu_dim_df["address"] == reporting_phu_address]
    match = result_match.head(1)
    return match["general_area"].values[0]


def get_weather_fk(date, phu_addr):
    result_match = weather_dim_df[weather_dim_df["date"] == date]
    city = get_phu_city(phu_addr)
    result_match = result_match[result_match["City"] == city]
    match = result_match.head(1)
    try:
        return match["weather_dim_key"].values[0]
    except:
        code.interact(local=dict(globals(), **locals()))


def get_special_measures_fk(date, phu_addr):
    phu_fk = get_phu_fk(phu_addr)
    phu_row = phu_dim_df[phu_dim_df["phu_dim_key"] == phu_fk]
    phu_match = phu_row.head(1)
    try:
        phu_name = phu_match["phu_name"].values[0]
    except:
        code.interact(local=dict(globals(), **locals()))
    result_match = special_measures_df[special_measures_df["keyword_one"] == phu_name]
    mask = (result_match["start_date"] <= date) & (
            result_match["end_date"] > date)
    result_date = result_match.loc[mask]
    if result_date.empty:
        return -1
    result_date = result_date.head(1)
    return result_date["special_measures_dim_key"].values[0]


def get_mobility_fk(date, phu_addr):
    result_match = mobility_dim_df[mobility_dim_df["date"] == date]
    city = get_phu_city(phu_addr)
    if city == "Ottawa":
        result_match = result_match[result_match["subregion"]
                == "Ottawa Division"]
        match = result_match.head(1)
        if match.empty:
            return -1
        try:
            return match["mobility_dim_key"].values[0]
        except:
            code.interact(local=dict(globals(), **locals()))
    elif city == "Toronto":
        result_match = result_match[result_match["subregion"]
                == "Toronto Division"]
        match = result_match.head(1)
        if match.empty:
            return -1
        try:
            return match["mobility_dim_key"].values[0]
        except:
            code.interact(local=dict(globals(), **locals()))


def gen_fact_df(df):
    original_raw_columns = list(raw_phu_df)
    filtered_phu_df = filter_phu_locations(raw_phu_df)

    # Facts/Measures
    print("Producing Fact and Measures ✨")
    filtered_phu_df["resolved"] = filtered_phu_df.apply(
            lambda row: row["Outcome1"] == "Resolved", axis=1)
    filtered_phu_df["un_resolved"] = filtered_phu_df.apply(
            lambda row: row["Outcome1"] == "Not Resolved", axis=1)
    filtered_phu_df["fatal"] = filtered_phu_df.apply(
            lambda row: row["Outcome1"] == "Fatal", axis=1)

    # Date Foreign Key Assignment
    print("Date Foreign Key Assignment ✨")
    filtered_phu_df["onset_date_dim_key"] = filtered_phu_df.apply(
            lambda row: get_date_fk(row["Accurate_Episode_Date"]), axis=1)
    filtered_phu_df["reported_date_dim_key"] = filtered_phu_df.apply(
            lambda row: get_date_fk(row["Case_Reported_Date"]), axis=1)
    filtered_phu_df["test_date_dim_key"] = filtered_phu_df.apply(
            lambda row: get_date_fk(row["Test_Reported_Date"]), axis=1)
    filtered_phu_df["specimen_date_dim_key"] = filtered_phu_df.apply(
            lambda row: get_date_fk(row["Specimen_Date"]), axis=1)

    # Patient Foreign Key Assignment
    print("Patient Foreign Key Assignment ✨")
    filtered_phu_df["patient_dim_key"] = filtered_phu_df.apply(lambda row: get_patient_fk(
        row["Age_Group"], row["Client_Gender"], row["Case_AcquisitionInfo"], row["Outbreak_Related"]), axis=1)

    # Public Health Unit Foreign Key Assignment
    print("Public Health Unit Foreign Key Assignment ✨")
    filtered_phu_df["phu_dim_key"] = filtered_phu_df.apply(
            lambda row: get_phu_fk(row["Reporting_PHU_Address"]), axis=1)

    # Weather Foreign Key Assignment
    print("Weather Foreign Key Assignment ✨")
    filtered_phu_df["weather_dim_key"] = filtered_phu_df.apply(lambda row: get_weather_fk(
        row["Accurate_Episode_Date"], row["Reporting_PHU_Address"]), axis=1)

    # Special Measures Foreign Key Assignment
    print("Special Measures Foreign Key Assignment ✨")
    special_measures_df["start_date"] = pd.to_datetime(
            special_measures_df["start_date"])
    special_measures_df["end_date"] = pd.to_datetime(
            special_measures_df["end_date"])
    filtered_phu_df["special_measures_dim_key"] = filtered_phu_df.apply(lambda row: get_special_measures_fk(
        row["Accurate_Episode_Date"], row["Reporting_PHU_Address"]), axis=1)

    # Mobility Foreign Key Assignment
    print("Mobility Foreign Key Assignment ✨")
    filtered_phu_df["mobility_dim_key"] = filtered_phu_df.apply(lambda row: get_mobility_fk(
        row["Accurate_Episode_Date"], row["Reporting_PHU_Address"]), axis=1)

    print("Cleanup 🧽")
    # Drop All Raw Columns
    fact_df = filtered_phu_df.drop(
            columns=[col for col in filtered_phu_df if col in original_raw_columns])

    # Drop Redundant Dimensional Rows
    # Weather : Station Name, date, City
    weather_dim_final_df = weather_dim_df.drop(
            columns=["Station Name", "date", "City"])
    weather_dim_final_df.to_csv(
            weather_dim_csv_path, encoding='utf-8', index=False)
    # Phu : "general_area"
    phu_dim_final_df = phu_dim_df.drop(
            columns=["general_area"])
    phu_dim_final_df.to_csv(
            phu_dim_csv_path, encoding='utf-8', index=False)
    # Mobility : date
    mobility_dim_final_df = mobility_dim_df.drop(columns=["date"])
    mobility_dim_final_df.to_csv(
            mobility_dim_csv_path, encoding='utf-8', index=False)
    # Fact : city, general_area,
    final_fact_df = fact_df.drop(columns=["city", "general_area"]).drop_duplicates(["onset_date_dim_key", "reported_date_dim_key", "test_date_dim_key", "specimen_date_dim_key","patient_dim_key", "phu_dim_key", "weather_dim_key", "special_measures_dim_key", "mobility_dim_key"])

    return final_fact_df


def generate_fact_dim():
    fact_df_columns = [
            "onset_date_dim_key",
            "reported_date_dim_key",
            "test_date_dim_key",
            "specimen_date_dim_key",
            "patient_dim_key",
            "phu_dim_key",
            "weather_dim_key",
            "special_measures_dim_key",
            "mobility_dim_key",
            "resolved",
            "un_resolved",
            "fatal"
            ]
    fact_df = pd.DataFrame(columns=fact_df_columns)

    fact_df = gen_fact_df(fact_df)
    fact_df.to_csv(fact_csv_path, encoding='utf-8', index=False)
