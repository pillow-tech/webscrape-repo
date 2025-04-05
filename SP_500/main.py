import requests
import csv
from bs4 import BeautifulSoup

def get_SP500():

    source_url = "https://www.slickcharts.com/sp500"
    headers = {'User-agent': 'Not a bot'}

    response = requests.get(source_url, headers= headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    table_extract = soup.find_all("tbody")
    rows=table_extract[0].find_all('tr')
    symbols_arr = []
    for row in rows:
        symbol = row.contents[5].text
        symbols_arr.append(symbol)
    return symbols_arr


if __name__ == "__main__":
    sp_500 = get_SP500()