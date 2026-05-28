import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui.caesar import Ui_MainWindow


class CaesarWindow(QMainWindow):
    api_root = "http://127.0.0.1:5000/api/caesar"

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._wire_events()

    def _wire_events(self):
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

    def _get_plain_text(self) -> str:
        return self.ui.txt_plain_text.toPlainText().strip()

    def _get_cipher_text(self) -> str:
        return self.ui.txt_cipher_text.toPlainText().strip()

    def _get_key(self) -> str:
        return self.ui.txt_key.text().strip()

    def _set_plain_text(self, text: str):
        self.ui.txt_plain_text.setPlainText(text)

    def _set_cipher_text(self, text: str):
        self.ui.txt_cipher_text.setPlainText(text)

    def _notify(self, title: str, message: str, icon=QMessageBox.Information):
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setIcon(icon)
        box.setText(message)
        box.exec_()

    def _post_json(self, endpoint: str, payload: dict) -> dict:
        response = requests.post(f"{self.api_root}{endpoint}", json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def encrypt_text(self):
        plain_text = self._get_plain_text()
        key = self._get_key()
        if not plain_text or not key:
            self._notify("Missing data", "Please enter both plaintext and key.", QMessageBox.Warning)
            return

        try:
            result = self._post_json("/encrypt", {"text": plain_text, "key": key})
        except requests.RequestException as exc:
            self._notify("Request failed", f"Cannot encrypt right now:\n{exc}", QMessageBox.Critical)
            return

        encrypted_text = result.get("encrypted_text", "")
        self._set_cipher_text(encrypted_text)
        self._notify("Success", "Encrypted successfully.")

    def decrypt_text(self):
        cipher_text = self._get_cipher_text()
        key = self._get_key()
        if not cipher_text or not key:
            self._notify("Missing data", "Please enter both ciphertext and key.", QMessageBox.Warning)
            return

        try:
            result = self._post_json("/decrypt", {"text": cipher_text, "key": key})
        except requests.RequestException as exc:
            self._notify("Request failed", f"Cannot decrypt right now:\n{exc}", QMessageBox.Critical)
            return

        decrypted_text = result.get("decrypted_text", "")
        self._set_plain_text(decrypted_text)
        self._notify("Success", "Decrypted successfully.")


def main():
    app = QApplication(sys.argv)
    window = CaesarWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
