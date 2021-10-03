
from flask import Flask, request, make_response
from app import ml_model
import pandas


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def serve():
    if request.mimetype == 'text/xml':
        response_data = do_work(request.data)
        response = make_response(response_data)
        response.headers['Content-type'] = 'text/xml'
        return response
    else:
        response_data = """<?xml version="1.0" encoding="UTF-8"?>
        <data>
            <row>
                <error>No Data Provided!</error>
            </row>
        </data>
        """
        response = make_response(response_data.encode())
        response.headers['Content-type'] = 'text/xml'
        return response


def do_work(xml: bytes) -> bytes:
    df_x = pandas.read_xml(xml.decode('utf-8'))
    df_y = ml_model.run(df_x)
    return df_y.to_xml(index = False).encode()