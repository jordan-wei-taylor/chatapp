from chatapp.routes import app
from chatapp.events import socket

def serve(host = '0.0.0.0', port = 4000, **kwargs):
    print(f'hosting on: http://localhost:{port}')
    socket.run(app, host = host, port = port, **kwargs)
