import requests
import json
import csv

def get_js(year: int):
    """
        this function go to the url and get json data, return list of disaster
    """
    url=f"http://vndms.dmptc.gov.vn/EventDisaster/TotalEvent?year={year}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    #                                                                                        else raising exception


def scrap_js():
    # get data from year 2022 to 2025
    year_start = 2022
    year_stop = 2026

    #                                                                                        how to handling exception in this? (case respone code != 0)
    disasters = []
    for i in range(year_start, year_stop):
        # data is a list of disaster
        data = get_js(i)
        for disaster in data:
            disasters.append({
                "kv_anhhuong" : disaster["kv_anhhuong"],
                "time_start" : disaster["time_start"],
                "lon" : disaster["lon"],
                "lat" : disaster["lat"],
                "level" : disaster["level"],
                "disaster_level" : disaster["disaster_level"],
                "type" : disaster["disaster"]["name_disaster"]
            })
    
    # store the data in the csv file
    to_csv_js(disasters)


def to_csv_js(disasters):
    file = "disasters_2.csv"
    with open(file, 'w') as csvfile:
        fieldname = ["kv_anhhuong", "time_start", "lon", "lat", "level", "disaster_level", "type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)

        writer.writeheader()
        writer.writerows(disasters)


if __name__ == "__main__":
    scrap_js()