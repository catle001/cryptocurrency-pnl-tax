import pandas as pd
import requests
import time
from secret.constants import COIN_API_KEY_2


def rate():
    data_df = pd.read_csv('data/filtered_df.csv')
    rates = {}
    for _, row in data_df.iterrows():
        rates[(row['timestamp'], row['currency'])] = get_rate(row['currency'], row['timestamp'])
    update_file(rates)


def get_rate(currency, date):
    response = get_response(currency, date)
    r = response.json()['rate']
    print r
    return response.json()['rate']


def update_file(rates):
    with open('data/exchange_rates.csv', 'a') as f:
        f.write('\n')
        for key in rates:
            date, currency = key
            f.write("{},{},{}\n".format(
                date,
                currency,
                rates[key]
            ))


def get_request(currency, date):
    url = 'https://rest.coinapi.io/v1/exchangerate/'+currency+'/USD'
    headers = {'X-CoinAPI-Key' : COIN_API_KEY_2}
    params = {'time': convert_time(date)}

    return requests.get(url=url, headers=headers, params= params)


def get_response(currency, date):
    count = 0
    while True:
        try:
            response = get_request(currency, date)
            if response.status_code == 200:
                break
            else:
                raise
        except:
            if count > 5:
                raise Exception("Too many API failures " + currency + + " on " + date)
            time.sleep(10 * count)
            count += 1
            continue
    return response


def convert_time(date):
    return date.replace(' ', 'T') + '-04:00'


def main():
    rate()


if __name__ == '__main__':
    main()
