from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh


def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key


def derive_shared_secret(private_key, server_public_key):
    return private_key.exchange(server_public_key)


def main():
    with open("server_public_key.pem", "rb") as public_file:
        server_public_key = serialization.load_pem_public_key(public_file.read())

    parameters = server_public_key.parameters()
    private_key, public_key = generate_client_key_pair(parameters)
    shared_secret = derive_shared_secret(private_key, server_public_key)

    with open("client_public_key.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    print("Client DH key pair generated successfully.")
    print("Shared Secret:", shared_secret.hex())


if __name__ == "__main__":
    main()
