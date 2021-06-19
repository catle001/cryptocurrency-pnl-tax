import pandas as pd


def filter_df():
    # read data, get rates
    query_type = ['Buy_Trade', 'Sell_Trade']

    df = pd.read_csv('data/transformed.csv')
    filtered_df = df[df.type.isin(query_type)]
    print write_file_csv(filtered_df)


def write_file_csv(df):
    df.to_csv("data/filtered_df.csv", encoding='utf-8', index=False)


if __name__ == '__main__':
    filter_df()
