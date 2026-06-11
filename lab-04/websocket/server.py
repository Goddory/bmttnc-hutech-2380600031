import random

import tornado.ioloop
import tornado.web
import tornado.websocket


class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketServer.clients.add(self)
        print(f"Client connected. Total clients: {len(WebSocketServer.clients)}")

    def on_close(self):
        WebSocketServer.clients.discard(self)
        print(f"Client disconnected. Total clients: {len(WebSocketServer.clients)}")

    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message '{message}' to {len(cls.clients)} client(s).")
        disconnected_clients = []
        for client in cls.clients:
            try:
                client.write_message(message)
            except tornado.websocket.WebSocketClosedError:
                disconnected_clients.append(client)

        for client in disconnected_clients:
            cls.clients.discard(client)


class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list

    def sample(self):
        return random.choice(self.word_list)


def main():
    app = tornado.web.Application(
        [(r"/websocket/", WebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)

    io_loop = tornado.ioloop.IOLoop.current()
    word_selector = RandomWordSelector(["apple", "banana", "orange", "grape", "melon"])

    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()),
        3000,
    )
    periodic_callback.start()

    print("WebSocket server is running at ws://localhost:8888/websocket/")
    io_loop.start()


if __name__ == "__main__":
    main()
