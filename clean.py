import pandas as pd
import os

def clean_data():
    csv_file = "disasters_2.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        print("Loaded successfully")
    else: 
        print("File not found")
        return 404
    
    """ handling duplicates
    """
    print("Removing duplicates")
    df.drop_duplicates(inplace=True)


    """ handling missing values
    """
    # print("Total missing values: ")
    # print(df.isna().mean() * 100) # return percent type
    # print(df.isna().sum()) # return counting type
    # missing values:name 17%, disaster_level : 95%
    # drop not needed cols:
    # too many missing values in "disaster_level" and we already have level column
    # nodeed kv anhhuong for statistic
    df.drop(columns=["kv_anhhuong", "disaster_level"], inplace=True) # too many missing values and we already have level column
    # filling missing value for name
    df["name"].fillna("Unknown", inplace=True)
    
    # examine data:
    # print(df.info())

    """ handling categorical and non categorical data
    """
    
    # print(df["type"].unique(), df["type"].nunique()) #-> 19
    # print(df["level"].unique(), df["level"].nunique()) # -> 13 unique levels
    for col in ["type", "level"]:
        df[col] = df[col].astype("category")
    
    """ handling time data
    """
    # old data: string: 2022-04-28T02:38:00
    df["time_start"] = pd.to_datetime(df["time_start"]).dt.date # no need to contain time

    # print(df.info())
    # print(df)

    """ handling string data
    """
    df["name"] = df["name"].str.strip()

clean_data()