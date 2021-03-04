import os
import sys
import pandas as pd

curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')

raw_measures_csv_path = os.path.join(curr_dir, './../../data/raw/response_framework.csv')
raw_measures_df = pd.read_csv(raw_measures_csv_path)
measures_csv_path = os.path.join(curr_dir, './../../data/dimensions/special_measures_dimension.csv')

def gen_measures_df():
    measures_df = raw_measures_df.rename(columns={"Reporting_PHU": "Keyword_1", "Status_PHU": "Title", "PHU_url": "Description", "Reporting_PHU_id": "Keyword_2"})
    measures_df.insert(0, 'Measures_key', range(len(measures_df)))
    
    return measures_df 

def generate_measures_dim():
    measures_dimension = gen_measures_df()
    measures_dimension.to_csv(measures_csv_path, encoding='utf-8', index=False) 