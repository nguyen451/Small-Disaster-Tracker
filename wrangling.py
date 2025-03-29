import pandas as pd
import os

def clean_data() -> None:
    # load data
    csv_file = "disasters.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        print("Data loaded")
    else: print("Loading failed: File not found")
    
    # handling mising values
    print("Total missing values: ")
    print(df.isna().sum())

    


clean_data()