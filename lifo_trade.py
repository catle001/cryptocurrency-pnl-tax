import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta


def lifo_trade(df):
    wallet = defaultdict(list)
    trade_df = pd.DataFrame(columns=['buy_date', 'sell_date','is_long_term', 'currency',
                                     'amount', 'buy_rate', 'sell_rate',
                                     'buy_price', 'sell_price', 'admin_fee', 'pnl'])
    for index, row in df.iterrows():
        if row['type'].startswith('Buy'):
            wallet = buy_transaction(row, wallet)
        if row['type'].startswith('Sell'):
            trade_df = sell_transaction(row, wallet, trade_df)

    print trade_df.head(20)

    return trade_df, wallet


def buy_transaction(row, wallet):
    currency = row['currency']
    transaction = (row['amount'], row['timestamp'], row['exchange_rate'], row['admin_fee'])
    wallet[currency].append(transaction)
    return wallet


def sell_transaction(row, wallet, trade_df):
    currency = row['currency']
    sell_amount = row['amount']
    if wallet[currency]:
        pop_amount, date, buy_rate, buy_admin_fee = wallet[currency].pop() if wallet[currency] else (None, None, None, None)
        while pop_amount is not None and pop_amount < sell_amount:
            sell_amount = sell_amount - pop_amount
            buy_price = float(buy_rate)*pop_amount
            sell_price = pop_amount*float(row['exchange_rate'])
            admin_fee = buy_admin_fee + row['admin_fee']*pop_amount/row['amount']
            trade = {
                'currency': currency,
                'buy_date': date.strftime("%Y-%m-%d"),
                'sell_date': row['timestamp'].strftime("%Y-%m-%d"),
                'amount': pop_amount,
                'is_long_term': row['timestamp'] - date > timedelta(365),
                'buy_price': buy_price,
                'sell_price': sell_price,
                'pnl': sell_price - buy_price - admin_fee,
                'buy_rate': buy_rate,
                'sell_rate': row['exchange_rate'],
                'admin_fee': admin_fee
            }
            trade_df = trade_df.append(trade, ignore_index=True)
            pop_amount, date, buy_rate, buy_admin_fee = wallet[currency].pop() if wallet[currency] else (None, None, None, None)

        if pop_amount:
            buy_price = sell_amount*float(buy_rate)
            sell_price = sell_amount*float(row['exchange_rate'])
            admin_fee = buy_admin_fee*sell_amount/pop_amount + row['admin_fee']*sell_amount/row['amount']
            trade = {
                'currency': currency,
                'buy_date': date.strftime("%Y-%m-%d"),
                'sell_date': row['timestamp'].strftime("%Y-%m-%d"),
                'amount': sell_amount,
                'is_long_term': row['timestamp'] - date > timedelta(365),
                'buy_price': buy_price,
                'sell_price': sell_price,
                'pnl': sell_price - buy_price - admin_fee,
                'buy_rate': buy_rate,
                'sell_rate': row['exchange_rate'],
                'admin_fee': admin_fee
            }
            trade_df = trade_df.append(trade, ignore_index=True)

            left_amount = pop_amount - sell_amount
            left_admin_fee = buy_admin_fee*left_amount/pop_amount
            if left_amount > 0:
                transaction = (left_amount, date, buy_rate, left_admin_fee)
                wallet[currency].append(transaction)

    return trade_df


