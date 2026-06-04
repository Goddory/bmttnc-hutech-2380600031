import socket
import struct
import threading

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


HOST = "localhost"
PORT = 12345
RSA_KEY_SIZE = 2048
AES_KEY_SIZE = 16
HEADER_SIZE = 4


server_key = RSA.generate(RSA_KEY_SIZE)
clients = []
clients_lock = threading.Lock()


def send_packet(sock, payload: bytes) -> None:
    sock.sendall(struct.pack("!I", len(payload)) + payload)


def recv_exact(sock, size: int) -> bytes:
    buffer = b""
    while len(buffer) < size:
        chunk = sock.recv(size - len(buffer))
        if not chunk:
            raise ConnectionError("Socket connection closed unexpectedly.")
        buffer += chunk
    return buffer


def recv_packet(sock) -> bytes:
    header = recv_exact(sock, HEADER_SIZE)
    payload_size = struct.unpack("!I", header)[0]
    return recv_exact(sock, payload_size)


def encrypt_message(aes_key: bytes, message: str) -> bytes:
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode("utf-8"), AES.block_size))
    return cipher.iv + ciphertext


def decrypt_message(aes_key: bytes, encrypted_message: bytes) -> str:
    iv = encrypted_message[: AES.block_size]
    ciphertext = encrypted_message[AES.block_size :]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")


def remove_client(client_socket: socket.socket) -> None:
    with clients_lock:
        for index, (sock, _, _) in enumerate(clients):
            if sock is client_socket:
                clients.pop(index)
                break


def broadcast_message(sender_socket: socket.socket, message: str) -> None:
    with clients_lock:
        recipients = list(clients)

    for client_socket, aes_key, client_address in recipients:
        if client_socket is sender_socket:
            continue

        try:
            encrypted_message = encrypt_message(aes_key, message)
            send_packet(client_socket, encrypted_message)
        except OSError:
            print(f"Failed to send message to {client_address}")


def handle_client(client_socket: socket.socket, client_address) -> None:
    print(f"Connected with {client_address}")

    try:
        send_packet(client_socket, server_key.publickey().export_key(format="PEM"))

        client_public_key = RSA.import_key(recv_packet(client_socket))
        aes_key = get_random_bytes(AES_KEY_SIZE)

        cipher_rsa = PKCS1_OAEP.new(client_public_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        send_packet(client_socket, encrypted_aes_key)

        with clients_lock:
            clients.append((client_socket, aes_key, client_address))

        while True:
            encrypted_message = recv_packet(client_socket)
            message = decrypt_message(aes_key, encrypted_message)
            print(f"Received from {client_address}: {message}")

            broadcast_message(client_socket, f"{client_address}: {message}")
            if message.strip().lower() == "exit":
                break
    except (ConnectionError, OSError, ValueError) as exc:
        print(f"Connection error with {client_address}: {exc}")
    finally:
        remove_client(client_socket)
        client_socket.close()
        print(f"Connection with {client_address} closed")


def main() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
