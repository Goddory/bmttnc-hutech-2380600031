import socket
import struct
import threading

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad


HOST = "localhost"
PORT = 12345
RSA_KEY_SIZE = 2048
HEADER_SIZE = 4


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


def receive_messages(client_socket: socket.socket, aes_key: bytes) -> None:
    try:
        while True:
            encrypted_message = recv_packet(client_socket)
            message = decrypt_message(aes_key, encrypted_message)
            print("Received:", message)
    except (ConnectionError, OSError, ValueError):
        print("Disconnected from server.")


def main() -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_key = RSA.generate(RSA_KEY_SIZE)

    server_public_key = RSA.import_key(recv_packet(client_socket))
    send_packet(client_socket, client_key.publickey().export_key(format="PEM"))

    encrypted_aes_key = recv_packet(client_socket)
    cipher_rsa = PKCS1_OAEP.new(client_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket, aes_key),
        daemon=True,
    )
    receive_thread.start()

    try:
        while True:
            message = input("Enter message ('exit' to quit): ")
            encrypted_message = encrypt_message(aes_key, message)
            send_packet(client_socket, encrypted_message)
            if message.strip().lower() == "exit":
                break
    except KeyboardInterrupt:
        print("\nClient stopped by user.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
