import pandas

def main():
    df = pandas.read_parquet('.\\data\\default_of_credit_card_clients_y.parquet')
    print(df.sample(5))
    return

if __name__ == '__main__':
    main()