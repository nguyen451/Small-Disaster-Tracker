from bs4 import BeautifulSoup
import requests
import csv
import os

def get_page_text(page: int):   # return html for each page
    url = f"http://www.dmc.gov.vn/Ajax.aspx?ctrl=/Modules/DMC/Web/ListDisasterContent&keyword=&typeid=0&startdate=&enddate=&lang=vi-VN&cPage={page}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    return None

def scrape_disaster_data():
    url = "http://www.dmc.gov.vn/thong-tin-thien-tai-pt32.html?lang=vi-VN"
    response = requests.get(url)
    # check if the web is available
    if response.status_code != 200:
        print("Cannot access page")
        return 404
    # getting the number of pages
    soup = BeautifulSoup(response.text, "html.parser")
    pages = soup.select("li[id*='PaginationAjax1_rptPaging_liPageBreak']")[-1].text

    # loop through the pages and get the disaster data
    disasters = []

    for i in range(1,37):
        soup = BeautifulSoup(get_page_text(i), "html.parser")
        tbodies = soup.find_all("tbody")
        for tbody in tbodies:
            for rows in tbody.find_all("tr"):
                cols = rows.find_all("td")
                disasters.append({
                    "name" : cols[1].text.strip(),
                    "type" : cols[2].text.strip(),
                    "start_date" : cols[3].text.strip(),
                    "end_date" : cols[4].text.strip(),
                    "influence_area" : cols[5].text.strip()
                })
    return disasters

def to_csv(disasters):
    file = "disasters.csv"
    with open(file, 'w') as csvfile:
        fieldname = ["name", "type", "start_date", "end_date", "influence_area"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)

        writer.writeheader()
        writer.writerows(disasters)


to_csv(scrape_disaster_data())
