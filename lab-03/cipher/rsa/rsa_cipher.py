from __future__ import annotations

from pathlib import Path

import rsa


class RSACipher:
    def __init__(self, keys_dir: Path | None = None):
        self.base_dir = Path(__file__).resolve().parent
        self.keys_dir = keys_dir or (self.base_dir / "keys")
        self.private_key_path = self.keys_dir / "private.pem"
        self.public_key_path = self.keys_dir / "public.pem"
        self.keys_dir.mkdir(parents=True, exist_ok=True)

    def generate_keys(self, key_size: int = 2048) -> None:
        public_key, private_key = rsa.newkeys(key_size)
        self.public_key_path.write_bytes(public_key.save_pkcs1("PEM"))
        self.private_key_path.write_bytes(private_key.save_pkcs1("PEM"))

    def load_keys(self):
        if not self.private_key_path.exists() or not self.public_key_path.exists():
            self.generate_keys()

        public_key = rsa.PublicKey.load_pkcs1(self.public_key_path.read_bytes())
        private_key = rsa.PrivateKey.load_pkcs1(self.private_key_path.read_bytes())
        return private_key, public_key

    @staticmethod
    def _select_encrypt_key(key_type: str, private_key, public_key):
        return public_key if key_type == "public" else private_key

    @staticmethod
    def _select_decrypt_key(key_type: str, private_key, public_key):
        if key_type == "public":
            raise ValueError("Decrypting with a public key is not supported.")
        return private_key

    @staticmethod
    def _encrypt_with_key(message: str, key) -> bytes:
        return rsa.encrypt(message.encode("utf-8"), key)

    @staticmethod
    def _decrypt_with_key(ciphertext: bytes, key) -> str:
        return rsa.decrypt(ciphertext, key).decode("utf-8")

    def encrypt(self, message: str, key) -> bytes:
        return self._encrypt_with_key(message, key)

    def decrypt(self, ciphertext: bytes, key) -> str:
        return self._decrypt_with_key(ciphertext, key)

    def sign(self, message: str, private_key) -> bytes:
        return rsa.sign(message.encode("utf-8"), private_key, "SHA-256")

    def verify(self, message: str, signature: bytes, public_key) -> bool:
        try:
            rsa.verify(message.encode("utf-8"), signature, public_key)
            return True
        except rsa.VerificationError:
            return False

    def encrypt_for_key_type(self, message: str, key_type: str) -> bytes:
        private_key, public_key = self.load_keys()
        key = self._select_encrypt_key(key_type, private_key, public_key)
        return self.encrypt(message, key)

    def decrypt_for_key_type(self, ciphertext_hex: str, key_type: str) -> str:
        private_key, public_key = self.load_keys()
        key = self._select_decrypt_key(key_type, private_key, public_key)
        ciphertext = bytes.fromhex(ciphertext_hex)
        return self.decrypt(ciphertext, key)

