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

def to_csv_js(disasters : dict, outfile : str) -> None:  #_____________________________________________FILE NOT FOUND_____________________________________________
    file = outfile
    with open(file, 'w') as csvfile:
        fieldname = ["name", "kv_anhhuong", "time_start", "lon", "lat", "level", "disaster_level", "type"]
        writer = csv.DictWriter(csvfile, fieldnames= fieldname)

        writer.writeheader()
        writer.writerows(disasters)
