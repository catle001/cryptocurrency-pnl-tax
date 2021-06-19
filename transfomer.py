import pandas as pd
import csv


def import_file():
    old_df = pd.read_csv('data/original.csv')
    old_df['timestamp'] = pd.to_datetime(old_df['Date'])
    old_df = old_df.sort_values(by=['timestamp'])
    rate_dict = get_rate_dict()
    old_df['Fee Amount'].fillna(0, inplace= True)

    df = pd.DataFrame(columns=['timestamp', 'type', 'amount', 'currency', 'exchange_rate', 'admin_fee'])
    for index, row in old_df.iterrows():
        admin_fee = row['Fee Amount']
        if row['Type'] in ('Buy', 'Trade', 'Receive'):
            type = 'Buy_' + row['Type']
            buy_row = {
                'type': type,
                'timestamp': row['timestamp'],
                'amount': row['Received Quantity'],
                'currency': row['Received Currency'],
                'exchange_rate': get_exchange_rate(type, row, rate_dict),
                'admin_fee': admin_fee
            }
            df = df.append(buy_row, ignore_index=True)

        if row['Type'] in ('Sell', 'Trade'):
            type = 'Sell_' + row['Type']
            sell_row = {
                'type': type,
                'timestamp': row['timestamp'],
                'amount': row['Sent Quantity'],
                'currency': row['Sent Currency'],
                'exchange_rate': get_exchange_rate(type, row, rate_dict),
                'admin_fee': admin_fee
            }
            df = df.append(sell_row, ignore_index=True)

    return df


def get_rate_dict():
    with open('data/exchange_rates.csv', mode='r') as infile:
        reader = csv.reader(infile)
        rates = {(row[0], row[1]): row[2] for row in reader}
        return rates


def get_exchange_rate(type, row, rate_dict):
    rate = 0
    if type == 'Buy_Buy':
        rate = row['Sent Quantity']/row['Received Quantity']
    if type == 'Sell_Sell':
        rate = row['Received Quantity']/row['Sent Quantity']
    if type == 'Buy_Receive':
        rate = 0
    if type == 'Buy_Trade':
        rate = rate_dict[(str(row['timestamp']), row['Received Currency'])]
    if type == 'Sell_Trade':
        rate = rate_dict[(str(row['timestamp']), row['Sent Currency'])]
    return rate


if __name__ == '__main__':
    import_file()