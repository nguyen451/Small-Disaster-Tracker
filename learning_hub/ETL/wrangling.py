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

    print("Records where start date is missing: ")
    print(df[df["start_date"].isna()])

    print("Records where end_date is missing: ")
    print(df[df["end_date"].isna()])

    print("Records where influence_area is missing: ")
    print(df[df["influence_area"].isna()])

    # There is disaster call "Tin khan cap can bao so 4" which has lost of missing value
    # I searched on the internet and see that there is a typhoon call Noru - typhoon number 4
    print(df[df["name"].str.contains("4")])
    # the rows "TIN KHAN CAP CON BAO SO 4 is all missing value so I'll delete it"
    

if __name__ == "__main__":
    clean_data()