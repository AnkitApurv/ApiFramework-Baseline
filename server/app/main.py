from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app import app

http_server = WSGIServer(('127.0.0.1', 5000), app.app)

if __name__ == '__main__':
    http_server.serve_forever()