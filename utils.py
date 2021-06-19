def write_file_csv(path, df):
    df.to_csv(path, encoding='utf-8', index=False)