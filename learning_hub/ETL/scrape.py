import requests
import csv

def get_js(year: int):              #____________________________________test throw exceptions__________________________________
    """
        @param: int year
        Get json data from url with related year
    """
    url = f"http://vndms.dmptc.gov.vn/EventDisaster/TotalEvent?year={year}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    # else raise exception

def scrap_js(outfile : str) -> None:
    # get data from year_start to year_stop
    start = 2022
    stop = 2026

    disasters = []
    for i in range(start, stop):
        # data is a list of disaster
        data = get_js(i)
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

    to_csv_js(disasters, outfile)


def to_csv_js(disasters : dict, outfile : str) -> None:  #_____________________________________________FILE NOT FOUND_____________________________________________
    file = outfile
    with open(file, 'w') as csvfile:
        fieldname = ["name", "kv_anhhuong", "time_start", "lon", "lat", "level", "disaster_level", "type"]
        writer = csv.DictWriter(csvfile, fieldnames= fieldname)

        writer.writeheader()
        writer.writerows(disasters)


if __name__ == "__main__":
    scrap_js()
