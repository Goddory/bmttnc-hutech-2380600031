import socket
import ssl
import threading


SERVER_ADDRESS = ("localhost", 12345)


def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("Nhan:", data.decode("utf-8"))
    except OSError:
        pass
    finally:
        ssl_socket.close()
        print("Ket noi da dong.")


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    ssl_socket = context.wrap_socket(client_socket, server_hostname="localhost")
    ssl_socket.connect(SERVER_ADDRESS)

    receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,), daemon=True)
    receive_thread.start()

    try:
        while True:
            message = input("Nhap tin nhan: ")
            ssl_socket.send(message.encode("utf-8"))
    except KeyboardInterrupt:
        pass
    finally:
        ssl_socket.close()


if __name__ == "__main__":
    main()
