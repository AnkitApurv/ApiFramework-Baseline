import pandas
# from sklearn.preprocessing import StandardScaler
from joblib import load

global classifier

def load_model():
    classifier = load('.\\app\\defaulter_classifier.joblib')
    return classifier

classifier = load_model()

# def etl(ccd: pandas.DataFrame) -> pandas.DataFrame:
#     ccdHistory = ccd[['PAY_1', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']]
#     ccdHistoryMode = ccdHistory.mode(axis = 'columns')
#     ccdHistorySeverest = ccdHistoryMode.apply(func = max, axis = 'columns')
#     ccd['PAY_MODE_SEVEREST'] = ccdHistorySeverest

#     ccdSpent = ccd[['BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6']]
#     ccd['BILL_AMT_MEAN'] = ccdSpent.mean(axis = 'columns').round().astype(int)

#     ccdSettled = ccd[['PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']]
#     ccd['PAY_AMT_MEAN'] = ccdSettled.mean(axis = 'columns').round().astype(int)

#     varsToScale = ['LIMIT_BAL', 'AGE', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6', 
#                 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'BILL_AMT_MEAN', 'PAY_AMT_MEAN']
#     scaler = StandardScaler(copy = True)

    # for var in varsToScale:
    #     ccd[var] = scaler.fit_transform(ccd[var].values.reshape(-1, 1))

    # filteredColumnsIndices = [ 0,  2,  5,  6,  7,  8,  9, 10, 11, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25]

    # ccdX = ccd.iloc[:, filteredColumnsIndices]
    # return ccdX

def predict(ccdX: pandas.DataFrame):
    ccdY = pandas.DataFrame(ccdX[['ID']])
    filteredColumnsIndices = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 17, 18, 19, 20, 21, 22, 23]

    ccdX = ccdX.iloc[:, filteredColumnsIndices]
    ccdY['default_payment_next_month'] = classifier.predict(ccdX)
    ccdY['score'] = classifier.score(ccdX, ccdY['default_payment_next_month'])
    ccdY[['probability_0', 'probability_1']] = classifier.predict_proba(ccdX)
    ccdY[['log_probability_0', 'log_probability_1']] = classifier.predict_log_proba(ccdX)
    return ccdY

def run(ccd: pandas.DataFrame):
    # ccdX = etl(ccd)
    results = predict(ccd)
    return results