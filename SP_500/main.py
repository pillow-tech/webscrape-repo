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

def extract_details(stock_symbols):
    
    stock_arr = []
    for symbol in stock_symbols:
        stock_values = []
        url = "https://finance.yahoo.com/quote/" + symbol
        headers = {'User-agent': 'Not a bot'}

        response = requests.get(url, headers= headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        li_extract = soup.find_all("li", class_="yf-1jj98ts")

        for tag in li_extract:
            value = tag.contents[2].text
            stock_values.append(value)
        
        stock_arr.append(stock_values)
    return stock_arr


if __name__ == "__main__":
    sp_500 = get_SP500()