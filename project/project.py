from helper import helper
import pandas as pd
import os
import sqlite3
import unicodedata
import re


def main():
    datafile = "proper_data.csv"
    rawdata = "disasters_2.csv"

    # Application name
    print("SMALL SIMPLE DISASTER TRACKER")

    # check if user want to refresh data
    if not os.path.exists(datafile) or os.path.getsize(datafile) == 0:
        get_data(datafile, rawdata)
    else:
        refresh = input("Refresh data (press 1), else press other keys: ")
        if refresh == "1":
            get_data(datafile, rawdata)

    
    # run the application:
    while True:
        print("Choose 1 choice: ")
        print("1. Vietnamese disaster statistics")
        print("2. One Vietnamese specific province")
        print("3. Exit")
        choice = int(input("Your choice: "))

        match choice:
            case 1: 
                vie_disasters(datafile)    
            case 2:
                prov_disasters(datafile)
            case 3:
                break
            case _:
                print("Invalid choice")


def get_data(datafile : str, rawdatafile : str) -> None:
    """
        Read data from the gov disaster web, save to a csv file and a SQL database
        Transform and clean data
    """
    # get raw data
    start = 2022
    stop = 2026
    disasters = []
    for i in range(start, stop):
        # data is a list of disaster
        data = helper.get_js(i)
        for disaster in data:
            disasters.append({
                "name" : disaster["name_vn"],
                "kv_anhhuong" : disaster["kv_anhhuong"],
                "time_start" : disaster["time_start"],
                "lon" : disaster["lon"],
                "lat" : disaster["lat"],
                "level" : disaster["level"],
                "disaster_level" : disaster["disaster_level"],
                "type" : disaster["disaster"]["name_disaster"]
            })
    # save raw data to csv
    helper.to_csv_js(disasters, rawdatafile)

    # clean and transform data
    df = pd.DataFrame(disasters)
    df.drop_duplicates(inplace=True)
    df.drop(columns=["disaster_level"], inplace=True) # "kv_anhhuong", 
    df.dropna(subset=["name"], inplace=True)
    df["name"] = df["name"].str.strip()

    for col in ["type", "level"]:
        df[col] = df[col].astype("category")

    df["time_start"] = pd.to_datetime(df["time_start"]).dt.date
    df["name"] = df["name"].str.strip()

    df = field_edit(df)

    # save cleaned and transformed data to csv file
    df.to_csv(datafile)

    # save to SQLite
    connection = sqlite3.connect("vieDisasters.db")
    df.to_sql("disasters", connection, if_exists='replace')


def field_edit(df : pd.DataFrame) -> pd.DataFrame:
    provinces_and_east_Sea = [
    "An Giang", "Ba Ria - Vung Tau", "Bac Lieu", "Bac Giang", "Bac Kan",
    "Bac Ninh", "Ben Tre", "Binh Duong", "Binh Đinh", "Binh Phuoc",
    "Binh Thuan", "Ca Mau", "Cao Bang", "Can Tho", "Đa Nang",
    "Đak Lak", "Đak Nong", "Đien Bien", "Đong Nai", "Đong Thap",
    "Gia Lai", "Ha Giang", "Ha Nam", "Ha Noi", "Ha Tinh",
    "Hai Duong", "Hai Phong", "Hau Giang", "Hoa Binh", "Hung Yen",
    "Khanh Hoa", "Kien Giang", "Kon Tum", "Lai Chau", "Lang Son",
    "Lao Cai", "Lam Đong", "Long An", "Nam Dinh", "Nghe An",
    "Ninh Binh", "Ninh Thuan", "Phu Tho", "Phu Yen", "Quang Binh",
    "Quang Nam", "Quang Ngai", "Quang Ninh", "Quang Tri", "Soc Trang",
    "Son La", "Tay Ninh", "Thai Binh", "Thai Nguyen", "Thanh Hoa",
    "Thua Thien Hue", "Tien Giang", "TP. Ho Chi Minh", "Tra Vinh", "Tuyen Quang",
    "Vinh Long", "Vinh Phuc", "Yen Bai", "Bien Đong"
    ]

    df["province"] = df.apply(lambda x : extract_province2(x["kv_anhhuong"]), axis=1)
    filtered = [prov in provinces_and_east_Sea for prov in df["province"]]
    filtered = df[filtered]
    filtered.drop(columns=["kv_anhhuong"], inplace=True)
    return filtered


def remove_accents(text : str) -> str:#                                       test
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])


def normalize_text(text : str) -> str: #                                      test        
    text = re.sub(r"\s+", " ", text.strip())
    text = remove_accents(text)
    text = text.title()
    return text


def extract_province2(kv_anhhuong) -> str: #                                  test
    mat = re.search(r"tỉnh\s*(.*)", kv_anhhuong, re.IGNORECASE)
    if mat:
        return normalize_text(mat.group(1))
    
    mat = re.search(r"Tp\.*\s*(.*)", kv_anhhuong, re.IGNORECASE)
    if mat: 
        return normalize_text(mat.group(1))
    
    mat = re.search(r"Thành Phố\s*(.*)", kv_anhhuong, re.IGNORECASE)
    if mat:
        return normalize_text(mat.group(1))
    
    return normalize_text(kv_anhhuong)

 
def vie_disasters(datafile : str):
    return


def prov_disasters(datafile : str):
    return

if __name__ == "__main__":
    main()