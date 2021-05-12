import pandas as pd
import yfinance as yf
import json


def get_info():
    df = pd.read_csv(r'../data/all_submission_files2.csv')
    list_of_info = {}
    unique_list_of_tickers = list(dict.fromkeys(df['ticker']))
    for i, ticker in enumerate(unique_list_of_tickers):
        print(f'{i}/{len(unique_list_of_tickers)}')
        if ticker is not None:
            stock = yf.Ticker(str(ticker))
            info = stock.info
            #print(info)
            list_of_info[ticker] = info
    with open(r'../data/stock_info.json', 'w') as js:
        json.dump(list_of_info, js)


get_info()
