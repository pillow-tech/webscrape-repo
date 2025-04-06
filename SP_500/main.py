import requests
import csv
import logging
from bs4 import BeautifulSoup

def get_SP500():
    logging.info("Extracting S&P 500 Companies List ")
    source_url = "https://www.slickcharts.com/sp500"
    headers = {'User-agent': 'Mozilla/5.0'}

    logging.info(f"Source URL: {source_url}")

    response = requests.get(source_url, headers= headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    table_extract = soup.find_all("tbody")
    rows=table_extract[0].find_all('tr')
    symbols_arr = []
    for row in rows:
        symbol = row.contents[5].text
        
        if '.' in symbol:
            symbol = symbol.replace('.','-')

        symbols_arr.append(symbol)
    logging.info("Extract List Complete")
    return symbols_arr

def extract_details(stock_symbols):
    logging.info("Extracting Stock Details in Yahoo Finance")
    stock_arr = []
    i = 0
    for symbol in stock_symbols:
        logging.info(f"{symbol}: {i+1}/{len(stock_symbols)}")
        stock_values = []
        url = "https://finance.yahoo.com/quote/" + symbol
        headers = {'User-agent': 'Mozilla/5.0'}

        response = requests.get(url, headers= headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        li_extract = soup.find_all("li", class_="yf-1jj98ts")

        for tag in li_extract:
            value = tag.contents[2].text
            stock_values.append(value)
        
        stock_arr.append(stock_values) 
        i += 1
    logging.info("Stock Details Extraction Complete")
    return stock_arr

def write_csv(sp_500, sp_details):
    logging.info("Writing data to csv file ...")
    with open('results.csv', 'w') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter = '|')
        header = ['Name','Previous Close', 'Open', 'Bid', 'Ask', "Day's Range", '52 Week Range', 'Volume', 'Avg. Volume', 'Market Cap (intraday)', 'Beta (5Y Monthly)', 'PE Ratio (TTM)', 'EPS (TTM)', 'Earnings Date', 'Forward Dividend & Yield', 'Ex-Dividend Date', '1y Target Est']
        csvWriter.writerow(header)
        
        for i in range(len(sp_500)):
            csvWriter.writerow([sp_500[i]]+sp_details[i])
    logging.info("Writing Complete")

def setup_logging():
    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO)

if __name__ == "__main__":
    setup_logging()
    logging.info("S&P 500 WebScraping Start ..")
    sp_500 = get_SP500()
    sp_details = extract_details(sp_500)
    write_csv(sp_500,sp_details)
    logging.info("S&P 500 WebScraping Job Done")