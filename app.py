from src import create_app
from src.socket_server import sio

app = create_app()

if __name__ == '__main__':
    sio.run(app)

    