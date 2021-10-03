import pandas
import numpy as np
from os import getcwd

def main():
    url = getcwd() + '\\data\\default of credit card clients.xls'
    ccd = pandas.read_excel(io = url, sheet_name='Data', header = 1, index_col = None, 
        dtype = {'LIMIT_BAL': np.int32, 'AGE': np.int32, 'BILL_AMT1': np.int32, 'BILL_AMT2': np.int32, 'BILL_AMT3': np.int32, 'BILL_AMT4': np.int32, 'BILL_AMT5': np.int32, 'BILL_AMT6': np.int32, 'PAY_AMT1': np.int32, 'PAY_AMT2': np.int32, 'PAY_AMT3': np.int32, 'PAY_AMT4': np.int32, 'PAY_AMT5': np.int32, 'PAY_AMT6': np.int32})


    ccd.rename(columns = {'PAY_0': 'PAY_1'}, inplace = True)
    ccd.rename(columns = {'default payment next month': 'default_payment_next_month'}, inplace = True)

    # ccdY = pandas.DataFrame(ccd['default_payment_next_month'])
    ccdX = ccd.drop(['default_payment_next_month'], axis = 'columns')
    ccdX.to_parquet('.\\data\\default_of_credit_card_clients.parquet', index = False, compression = None)
    return

if __name__ == '__main__':
    main()