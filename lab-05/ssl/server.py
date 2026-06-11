import socket
import ssl
import threading
from pathlib import Path


SERVER_ADDRESS = ("localhost", 12345)
BASE_DIR = Path(__file__).resolve().parent
CERT_FILE = BASE_DIR / "certificates" / "server-cert.crt"
KEY_FILE = BASE_DIR / "certificates" / "server-key.key"
clients = []


def handle_client(client_socket):
    clients.append(client_socket)
    print("Da ket noi voi:", client_socket.getpeername())

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            print("Nhan:", data.decode("utf-8"))
            for client in list(clients):
                if client is client_socket:
                    continue
                try:
                    client.send(data)
                except OSError:
                    if client in clients:
                        clients.remove(client)
    except OSError:
        pass
    finally:
        print("Da ngat ket noi:", client_socket.getpeername())
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(5)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=str(CERT_FILE), keyfile=str(KEY_FILE))

    print("Server dang cho ket noi...")
    while True:
        client_socket, _ = server_socket.accept()
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        client_thread = threading.Thread(target=handle_client, args=(ssl_socket,), daemon=True)
        client_thread.start()


if __name__ == "__main__":
    main()
