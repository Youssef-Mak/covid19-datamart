import os
import sys
import pandas as pd

curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
raw_patient_csv_path = os.path.join(
    curr_dir, './../../data/raw/confirmed_positive_covid_cases.csv')
patient_dim_csv_path = os.path.join(
    curr_dir, './../../data/dimensions/patient_dimension.csv')

raw_patient_df = pd.read_csv(raw_patient_csv_path)


def gen_patient_df(patient_df):
    rel_cols = ["Client_Gender", "Age_Group",
                "Case_AcquisitionInfo", "Outbreak_Related"]

    rel_df = raw_patient_df.drop(
        columns=[col for col in raw_patient_df if col not in rel_cols])
    patient_df = rel_df.rename(columns={"Client_Gender": "gender", "Age_Group": "age_group",
                                        "Case_AcquisitionInfo": "acquisition_group", "Outbreak_Related": "outbreak_related"})
    patient_df["outbreak_related"] = patient_df["outbreak_related"].apply(
        lambda x: True if (x == "Yes") else (False if (x == "No") else ""))

    patient_df = patient_df.drop_duplicates()
    patient_df["patient_dim_key"] = range(0, len(patient_df))

    return patient_df


def generate_patients_dim():
    patient_df_columns = [
        "gender",
        "age_group",
        "acquisition_group",
        "outbreak_related",
        "patient_dim_key"
    ]
    patient_df = pd.DataFrame(columns=patient_df_columns)

    patient_dim_df = gen_patient_df(patient_df)
    patient_dim_df.to_csv(patient_dim_csv_path, encoding='utf-8', index=False)
