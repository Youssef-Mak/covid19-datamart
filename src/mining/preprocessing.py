import database_connect
import psycopg2
import pandas as pd
import math
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
import os

def main():
    try:
        database_connection = database_connect.connect()
        cursor = database_connection.cursor()

        # Get the data
        query_string = '''
                        SELECT spec.title, mob.metro_area, mob.subregion, f.resolved, f.un_resolved, f.fatal, phu.phu_name, p.age_group, p.gender, d.day, d.month, d.season
                        FROM "Covid19DataMart".covid19_tracking_fact AS f 
                        INNER JOIN "Covid19DataMart".date_dimension AS d 
                        ON f.onset_date_dim_key = d.date_dim_key 
                        INNER JOIN "Covid19DataMart".patient_dimension AS p 
                        ON f.patient_dim_key = p.patient_dim_key  
                        INNER JOIN "Covid19DataMart".phu_dimension AS phu 
                        ON f.phu_dim_key = phu.phu_dim_key
                        INNER JOIN "Covid19DataMart".mobility_dimension AS mob
                        ON f.mobility_dim_key = mob.mobility_dim_key
                        INNER JOIN "Covid19DataMart".special_measures_dimension as spec
                        ON f.special_measures_dim_key = spec.special_measures_dim_key'''

        print("Querying data...")
        raw_data = query_data(query_string, cursor)
        print("Preprocessing data...")
        preprocess_data(raw_data)
        cursor.close()
        database_connection.close()
        print('Database connection closed.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if database_connection is not None:
            database_connection.close()
            print('Database connection closed.')

def preprocess_data(data):
    """
    Preprocesses thed raw data by converting to numerical forms and outputting into a csv file ready to use.
    
    List of Features:
        1. special measures title
        2. metro area
        3. subregion
        4. resolved, unresolved, fatal
        5. phu location name
        6. age
        7. gender
        8. day, month, season

    Preprocessing Pipeline Stages:
        Stage 1: Handling missing data
        Stage 2: Handling categorical attributes
        Stage 3: Data normalization
        Stage 4: Under or oversampling
    """

    # Separate the raw data into categories with columns in a dataframe
    unprocessed_data = separate_raw_data(data)
    
    # Handle missing data
    handle_missing_data(unprocessed_data)

    # Convert categorical attributes
    processed_data = convert_categorical_to_numeric(unprocessed_data)

    # Normalize data
    normalize_data(processed_data)

    # Undersample data
    undersampled_df = undersample_data(processed_data)

    # Shuffle the data around in case the other guys don't realize it is sorted
    undersampled_df = undersampled_df.sample(frac=1).reset_index(drop=True)

    # Save the processed data to a csv file for the next stage of the project.
    undersampled_df.to_csv("C:/Users/grayd/OneDrive/Documents/University of Ottawa/Fourth Year/Winter 2021/CSI4142/Group Project/Data Mart/covid19-datamart/data/preprocessed_data/mined_data.csv", index=False)


def separate_raw_data(raw_data):
    return pd.DataFrame(raw_data, columns=["Special Measure", "metro_area", "subregion", "resolved", "unresolved", "fatal", "phu_location", "age", "gender", "day", "month", "season"])


def undersample_data(data):
    rus = RandomUnderSampler(random_state=0) 
    resolved_indices = data[data["resolved"] == 1].index
    random_indices = np.random.choice(resolved_indices, 5000, replace=False)
    resolved_sample = data.loc[random_indices]
    unresolved_sample = data.loc[data[data["unresolved"] == 1].index]
    fatal_sample = data.loc[data[data["fatal"] == 1].index]

    undersampled_df = pd.DataFrame()
    undersampled_df = undersampled_df.append(resolved_sample)
    undersampled_df = undersampled_df.append(fatal_sample, ignore_index=True)
    undersample_df = undersampled_df.append(unresolved_sample, ignore_index=True)

    return undersample_df
    

def normalize_data(data):
    """
    Features to normalize:
        1. day
        2. month
        3. age
    """

    def normalize_helper(feature):
        data[feature] = (data[feature] - data[feature].mean()) / data[feature].std()

    columns_to_normalize = ["day", "month", "age"]
    
    for feature in columns_to_normalize:
        normalize_helper(feature)


def convert_categorical_to_numeric(df):
    # One hot encode resolved, unresolved, fatal. This is already pretty much done because there are 
    # 3 columns of true/false already. Just need to replace these values with 1's and 0's.

    df["resolved"].replace([False, True], [0, 1], inplace=True)
    df["unresolved"].replace([False, True], [0, 1], inplace=True)
    df["fatal"].replace([False, True], [0, 1], inplace=True)

    # One hot encode special measure title, metro area, subregion, gender, and season
    features_to_encode = ['Special Measure', 'metro_area', 'subregion', 'gender', 'season', 'phu_location']
    
    for feature in features_to_encode:
        df = encode_and_bind(df, feature)

    # Convert age to numeric 
    df["age"].replace(["<20", "UNKNOWN"], ["10s", "20s"], inplace=True)
    df["age"] = df["age"].str[0:-1]
    df["age"] = df["age"].astype(int)
    
    return df
    

def encode_and_bind(original_dataframe, feature_to_encode):
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
    res = pd.concat([original_dataframe, dummies], axis=1)
    res = res.drop([feature_to_encode], axis=1)

    return res


def handle_missing_data(data):    
    # Replace 'None' special measure values to 'other'
    data["Special Measure"].fillna("Other", inplace=True)

    # Impute missing metro-area with most common metro area
    data["metro_area"].fillna("Greater Toronto Area", inplace=True)

    # Impute missing subregion with most common subregion
    data["subregion"].fillna("Toronto Divison", inplace=True)

    # Find any empty cells in resolved, unresolved, fatal and replace with False
    data[["resolved", "unresolved", "fatal"]].fillna(False, inplace=True) 

    # Impute phu location name if missing
    data["phu_location"].fillna("Toronto Public Health", inplace=True)

    # Replace missing age values with the mode of ages seen
    data["age"].fillna(data["age"].mode()[0], inplace=True)


def query_data(query, cursor):
    cursor.execute(query)
    rows = cursor.fetchall()

    return rows

if __name__ == '__main__':
    main()
