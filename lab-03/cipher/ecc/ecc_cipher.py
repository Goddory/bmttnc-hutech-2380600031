from __future__ import annotations

from pathlib import Path

import ecdsa


class ECCCipher:
    def __init__(self, keys_dir: Path | None = None):
        self.base_dir = Path(__file__).resolve().parent
        self.keys_dir = keys_dir or (self.base_dir / "keys")
        self.private_key_path = self.keys_dir / "privateKey.pem"
        self.public_key_path = self.keys_dir / "publicKey.pem"
        self.keys_dir.mkdir(parents=True, exist_ok=True)

    def generate_keys(self) -> None:
        signing_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        verifying_key = signing_key.get_verifying_key()

        self.private_key_path.write_bytes(signing_key.to_pem())
        self.public_key_path.write_bytes(verifying_key.to_pem())

    def load_keys(self):
        if not self.private_key_path.exists() or not self.public_key_path.exists():
            self.generate_keys()

        signing_key = ecdsa.SigningKey.from_pem(self.private_key_path.read_text(encoding="utf-8"))
        verifying_key = ecdsa.VerifyingKey.from_pem(self.public_key_path.read_text(encoding="utf-8"))
        return signing_key, verifying_key

    def sign(self, message: str, signing_key) -> bytes:
        return signing_key.sign(message.encode("ascii"))

    def verify(self, message: str, signature: bytes, verifying_key) -> bool:
        try:
            return verifying_key.verify(signature, message.encode("ascii"))
        except ecdsa.BadSignatureError:
            return False

