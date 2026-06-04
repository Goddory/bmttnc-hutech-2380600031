import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui.rsa import Ui_MainWindow


class RSAWindow(QMainWindow):
    api_root = "http://127.0.0.1:5000/api/rsa"

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._bind_actions()

    def _bind_actions(self):
        self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
        self.ui.btn_encrypt.clicked.connect(self.encrypt_message)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_message)
        self.ui.btn_sign.clicked.connect(self.sign_message)
        self.ui.btn_verify.clicked.connect(self.verify_message)

    def _message_box(self, title: str, text: str, icon=QMessageBox.Information):
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setIcon(icon)
        box.setText(text)
        box.exec_()

    def _request_json(self, method: str, endpoint: str, payload=None):
        url = f"{self.api_root}{endpoint}"
        request_fn = getattr(requests, method.lower())
        response = request_fn(url, json=payload, timeout=10) if payload is not None else request_fn(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def _plain_text(self) -> str:
        return self.ui.txt_plain_text.toPlainText().strip()

    def _cipher_text(self) -> str:
        return self.ui.txt_cipher_text.toPlainText().strip()

    def _message_text(self) -> str:
        return self.ui.txt_info.toPlainText().strip()

    def _signature_text(self) -> str:
        return self.ui.txt_sign.toPlainText().strip()

    def generate_keys(self):
        try:
            data = self._request_json("get", "/generate_keys")
        except requests.RequestException as exc:
            self._message_box("API error", f"Cannot generate keys:\n{exc}", QMessageBox.Critical)
            return
        self._message_box("Keys", data.get("message", "Keys generated"))

    def encrypt_message(self):
        message = self._plain_text()
        if not message:
            self._message_box("Input missing", "Please enter plaintext first.", QMessageBox.Warning)
            return

        try:
            data = self._request_json("post", "/encrypt", {"message": message, "key_type": "public"})
        except requests.RequestException as exc:
            self._message_box("API error", f"Cannot encrypt:\n{exc}", QMessageBox.Critical)
            return

        self.ui.txt_cipher_text.setPlainText(data.get("encrypted_message", ""))
        self._message_box("Encrypt", "Encrypted successfully")

    def decrypt_message(self):
        ciphertext = self._cipher_text()
        if not ciphertext:
            self._message_box("Input missing", "Please enter ciphertext first.", QMessageBox.Warning)
            return

        try:
            data = self._request_json("post", "/decrypt", {"ciphertext": ciphertext, "key_type": "private"})
        except requests.RequestException as exc:
            self._message_box("API error", f"Cannot decrypt:\n{exc}", QMessageBox.Critical)
            return

        self.ui.txt_plain_text.setPlainText(data.get("decrypted_message", ""))
        self._message_box("Decrypt", "Decrypted successfully")

    def sign_message(self):
        message = self._message_text()
        if not message:
            self._message_box("Input missing", "Please enter a message to sign.", QMessageBox.Warning)
            return

        try:
            data = self._request_json("post", "/sign", {"message": message})
        except requests.RequestException as exc:
            self._message_box("API error", f"Cannot sign:\n{exc}", QMessageBox.Critical)
            return

        self.ui.txt_sign.setPlainText(data.get("signature", ""))
        self._message_box("Sign", "Signed successfully")

    def verify_message(self):
        message = self._message_text()
        signature = self._signature_text()
        if not message or not signature:
            self._message_box("Input missing", "Please enter both message and signature.", QMessageBox.Warning)
            return

        try:
            data = self._request_json("post", "/verify", {"message": message, "signature": signature})
        except requests.RequestException as exc:
            self._message_box("API error", f"Cannot verify:\n{exc}", QMessageBox.Critical)
            return

        if data.get("is_verified"):
            self._message_box("Verify", "Verified successfully")
        else:
            self._message_box("Verify", "Verification failed", QMessageBox.Warning)


def main():
    app = QApplication(sys.argv)
    window = RSAWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

