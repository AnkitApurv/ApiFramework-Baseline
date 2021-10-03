from datetime import datetime
from typing import List
import pycurl
from io import BytesIO
import pandas
import concurrent.futures as cf

x_path = '.\\data\\default_of_credit_card_clients.parquet'
y_path = '.\\data\\default_of_credit_card_clients_y.parquet'
endpoint = 'http://127.0.0.1:5000'

def load_data(filepath: str) -> pandas.DataFrame:
    df = pandas.read_parquet(filepath)
    return df

def prepare_variables(df_x: pandas.DataFrame) -> List[str]:
    request_xmls = []
    for idx in df_x.index:
        request_xmls.append(df_x.iloc[[idx]].to_xml(index = False))
    return request_xmls

def make_request(request_xml: str) -> str:
    c = pycurl.Curl()
    buffer = BytesIO()
    c.setopt(pycurl.URL, endpoint)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: text/xml' , 'Accept: text/xml'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, request_xml.encode())
    c.setopt(pycurl.WRITEDATA, buffer)
    c.perform()
    response_xml = buffer.getvalue().decode('utf-8')
    return response_xml

def save_data(y: List[str], filepath: str):
    dfs = []
    for datapoint in y:
        dfs.append(pandas.read_xml(datapoint))
    df = pandas.concat(dfs)
    df.to_parquet(filepath, index = False, compression = None)
    return

def main():
    init = datetime.utcnow()

    df_x = load_data(x_path)
    request_xmls = prepare_variables(df_x)

    start = datetime.utcnow()
    print(f'Prepare requests: {start - init}')

    with cf.ThreadPoolExecutor(max_workers=20) as executor:
        response_xmls = list(executor.map(make_request, request_xmls))

    end = datetime.utcnow()
    print(f'Requests-responses: {end - start}')

    save_data(response_xmls, y_path)

    finish = datetime.utcnow()
    print(f'Save responses: {finish - end}')
    return


if __name__ == "__main__":
    main()