import asyncio
from websockets.sync.client import connect


def hello():
    with connect("ws://localhost:8765") as websocket:
        message = websocket.recv()
        print(f"Received: {message}")


if __name__ == '__main__':
    while True:
        hello()
