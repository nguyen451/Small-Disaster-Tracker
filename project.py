from helper import helper

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import os
import sqlite3
import unicodedata
import re
import seaborn as sns


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
    

    # connect to the database
    cnn = sqlite3.connect('vieDisasters.db')
    db = cnn.cursor()
    
    # run the application:
    i = 0
    while True:
        print("Choose 1 choice: ")
        print("1. Vietnamese disaster statistics")
        print("2. One Vietnamese specific province")
        print("3. Exit")
        choice = int(input("Your choice: "))

        pdf = PdfPages(f"disaster_report_{i}.pdf")

        match choice:
            case 1: 
                # disaster by type:
                print("Disaster by types: ")
                order = int(input("Press 0 for ascending, 1 for descending order: "))
                helper.make_and_print_table(dst_by_type(db,"vie", order), ["disaster", "count"], "DISASTERS_IN_VIET_NAM")


                # print most freq disaster
                print("Most freq disaster: ")
                helper.make_and_print_table(most_freq_dst(db,"vie"), ["disaster", "count"], "MOST_FREQUENT_DISASTER_IN_VIET_NAM")

                # disaster by province
                print("Disaster by prov: ")
                while True:
                    try:
                        limit = int(input("Output limitation (press 0 for all results display): "))
                        order = int(input("Press 0 for ascending, 1 for descending order: "))
                        helper.make_and_print_table(dst_by_prov(db, limit, order), ["province", "count"], "DISASTER_BY_PROVINCE_IN_VIET_NAM")
                        break
                    except ValueError:
                        print("Invalid prompt, please try again")
                        continue
                    except KeyError:
                        print("Invalid province")

                # disaster trends
                disaster_trends(cnn, "vie")

                # print to pdf

            case 2:
                while True:
                    try: 
                        prov = input("Province (one province only): ")
                        # disaster by type
                        print("Disaster by types: ")
                        order = int(input("Press 0 for ascending, 1 for descending order: "))
                        helper.make_and_print_table(dst_by_type(db, prov, order), ["disaster", "count"], f"DISASTERS_IN_{prov.upper()}")

                        # print most freq disaster
                        print("Most freq disaster: ")
                        helper.make_and_print_table(most_freq_dst(db, prov), ["disaster", "count"], f"MOST_FREQUENT_DISASTER_IN_{prov.upper()}")

                        # print disaster trends
                        disaster_trends(cnn, prov)
                        break
                    except ValueError:
                        print("Invalid input")
                        continue
                    except KeyError:
                        print("Invalid province input, please try again")
                        continue

            case 3:
                break
            case _:
                print("Invalid choice")

    cnn.close()


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

    df["time_start"] = pd.to_datetime(df["time_start"])
    df = df[df["time_start"].dt.year >= 2022] # drop outlier
    df["time_start"] = df["time_start"].dt.date
    df["name"] = df["name"].str.strip()

    df = field_edit(df)

    # save cleaned and transformed data to csv file
    df.to_csv(datafile)

    # save to SQLite
    connection = sqlite3.connect("vieDisasters.db")
    df.to_sql("disasters", connection, if_exists='replace')
    connection.close()


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
    copy = filtered.copy()
    copy.drop(columns=["kv_anhhuong"], inplace=True)
    return copy


def remove_accents(text : str) -> str:#                                       test
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])


def normalize_text(text : str) -> str: #                                      test        
    text = re.sub(r"\s+", " ", text.strip().strip('"').strip("'"))
    text = remove_accents(text)
    text = text.title()
    return text


def extract_province2(kv_anhhuong) -> str: #                                  test
    mat = re.search(r"tỉnh\s*([^\/\-$%@#!&\*].*)", kv_anhhuong, re.IGNORECASE)
    if mat:
        return normalize_text(mat.group(1))
    
    mat = re.search(r"Tp\.*\s*(.*)", kv_anhhuong, re.IGNORECASE)
    if mat: 
        return normalize_text(mat.group(1))
    
    mat = re.search(r"Thành Phố\s*(.*)", kv_anhhuong, re.IGNORECASE)
    if mat:
        return normalize_text(mat.group(1))
    
    return normalize_text(kv_anhhuong)

 
def dst_by_type(db : sqlite3.Cursor, prov : str, order : int):
    if prov == "vie":
        if order == 1:
            db.execute('SELECT "type", COUNT("index") AS "count" FROM "disasters" GROUP BY "type" ORDER BY "count" DESC')
        else:
            db.execute('SELECT "type", COUNT("index") AS "count" FROM "disasters" GROUP BY "type" ORDER BY "count"')
    else :
        prov = normalize_text(prov)
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
        if not prov in provinces_and_east_Sea:
            raise KeyError
        else:
            if order == 1:
                db.execute('SELECT "type", COUNT("index") AS "count" FROM "disasters" WHERE "province" = ? GROUP BY "type" ORDER BY "count" DESC', (prov,))
            else:
                db.execute('SELECT "type", COUNT("index") AS "count" FROM "disasters" WHERE "province" = ? GROUP BY "type" ORDER BY "count"', (prov,))
    res = db.fetchall()
    return res


def most_freq_dst(db : sqlite3.Cursor, prov : str):
    if prov == "vie":
        db.execute('SELECT "type", "count" FROM (SELECT "type", COUNT("type") AS "count" FROM "disasters" GROUP BY "type") WHERE ("count" = (SELECT MAX("count") FROM (SELECT COUNT("type") AS "count" FROM "disasters" GROUP BY "type")))')
    else :
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
        prov = normalize_text(prov)
        if not prov in provinces_and_east_Sea:
            raise KeyError
        db.execute('SELECT "type", "count" FROM (SELECT "type", COUNT("type") AS "count" FROM "disasters" WHERE "province" = ? GROUP BY "type") WHERE ("count" = (SELECT MAX("count") FROM (SELECT COUNT("type") AS "count" FROM "disasters" WHERE "province" = ? GROUP BY "type")))', (prov, prov))
    
    res = db.fetchall()
    return res
        

def dst_by_prov(db : sqlite3.Cursor, limit, order):
    if not (isinstance(limit, int) and order in [0,1]):
        raise ValueError
    
    query = 'SELECT "province", COUNT("province") AS "count" FROM "disasters" GROUP BY "province"'
    if order == 1:
        query = query + ' ORDER BY "count" DESC'
    else :
        query = query + ' ORDER BY "count"'
    if limit != 0:
        query = query + ' LIMIT ' + str(limit)
    
    db.execute(query)
    res = db.fetchall()
    return res


def disaster_trends(cnn : sqlite3.Connection, prov : str):
    # check for proper input
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
    if prov != "vie" and not normalize_text(prov) in provinces_and_east_Sea:
        raise KeyError
    
    # plot for 5 most freq disaster
    # prepare data
    query=""
    if prov == "vie":
        query = 'SELECT "type", COUNT("type") as "count", strftime("%Y","time_start") as "year" FROM "disasters" WHERE "type" IN (SELECT "type" FROM "disasters" GROUP BY "type" ORDER BY COUNT("type") DESC LIMIT 5) AND strftime("%Y","time_start") < (SELECT MAX(strftime("%Y","time_start")) FROM "disasters") GROUP BY "type", "year"'
    else:
        prov = normalize_text(prov)
        query = f'SELECT "type", COUNT("type") as "count", strftime("%Y","time_start") as "year" FROM "disasters" WHERE "province" = "{prov}" AND "type" IN (SELECT "type" FROM "disasters" WHERE "province" = "{prov}" GROUP BY "type" ORDER BY COUNT("type") DESC LIMIT 5) AND strftime("%Y","time_start") < (SELECT MAX(strftime("%Y","time_start")) FROM "disasters") GROUP BY "type", "year"'
    df = pd.read_sql_query(query, cnn)
    # data for max freq:
    grouped = df.groupby("type")["count"].sum().reset_index()
    grouped = grouped.sort_values("count", ascending=True)
    # plot
    fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(18,5))
    fig.suptitle('5 most freq disaster and trends')
    sns.barplot(x="type", y="count", data=grouped, ax=ax1, palette="YlGnBu", hue="type")
    ax1.set_title("5 most freq disaster")
    sns.lineplot(data=df, x="year", y="count", hue="type", palette="YlGnBu", ax=ax2)
    ax2.set_title("Trends of disasters")
    ax3.axis('off')
    ax3.set_title("Data: disaster count per year")
    pd.plotting.table(ax=ax3, data=df, loc='center', cellLoc='center')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()