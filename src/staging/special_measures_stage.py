import os
import sys
import pandas as pd

curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')

raw_measures_csv_path = os.path.join(
    curr_dir, './../../data/raw/response_framework.csv')
raw_measures_df = pd.read_csv(raw_measures_csv_path)
measures_csv_path = os.path.join(
    curr_dir, './../../data/dimensions/special_measures_dimension.csv')


def gen_measures_df():
    measures_df = raw_measures_df.rename(columns={
                                         "Reporting_PHU": "keyword_one", "Status_PHU": "title", "PHU_url": "description", "Reporting_PHU_id": "keyword_two"})
    measures_df["start_date"] = measures_df.apply(
            lambda row: row["start_date"][:10], axis=1)
    measures_df["end_date"] = measures_df.apply(
            lambda row: row["end_date"][:10], axis=1)
    measures_df.insert(0, 'special_measures_dim_key', range(len(measures_df)))

    dummy_row = {"keyword_one": "", "keyword_two": "", "title": "", "description": "", "start_date": "", "end_date": "", "special_measures_dim_key": -1}
    measures_df = measures_df.append(dummy_row, ignore_index=True)

    return measures_df


def generate_measures_dim():
    measures_dimension = gen_measures_df()
    measures_dimension.to_csv(measures_csv_path, encoding='utf-8', index=False)
