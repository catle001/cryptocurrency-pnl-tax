from transfomer import import_file
from lifo_trade import lifo_trade
from utils import write_file_csv


def main():
    df = import_file()
    trade_df, wallet = lifo_trade(df)
    write_file_csv('data/transformed.csv', df)
    write_file_csv('data/pnl.csv', trade_df)
    print wallet


if __name__ == '__main__':
    main()
