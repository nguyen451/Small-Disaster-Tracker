from bs4 import BeautifulSoup
import requests

html_text = requests.get('http://www.dmc.gov.vn/thong-tin-thien-tai-pt32.html?lang=vi-VN').text
soup = BeautifulSoup(html_text, 'lxml')
tables = soup.find('table', class_='table table-bordered')
print(tables)