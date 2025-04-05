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

def write_csv(sp_500, sp_details):
    
    with open('results.csv', 'w') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter = '|')
        header = ['Name','Previous Close', 'Open', 'Bid', 'Ask', "Day's Range", '52 Week Range', 'Volume', 'Avg. Volume', 'Market Cap (intraday)', 'Beta (5Y Monthly)', 'PE Ratio (TTM)', 'EPS (TTM)', 'Earnings Date', 'Forward Dividend & Yield', 'Ex-Dividend Date', '1y Target Est']
        csvWriter.writerow(header)
        
        for i in range(len(sp_500)):
            csvWriter.writerow([sp_500[i]]+sp_details[i])

if __name__ == "__main__":
    sp_500 = get_SP500()
    sp_details = extract_details(sp_500)
    write_csv(sp_500,sp_details)