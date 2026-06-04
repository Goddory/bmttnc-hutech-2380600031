import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from ui.ecc import Ui_MainWindow


class ECCWindow(QMainWindow):
    api_root = "http://127.0.0.1:5000/api/ecc"

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._bind_actions()

    def _bind_actions(self):
        self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
        self.ui.btn_sign.clicked.connect(self.sign_message)
        self.ui.btn_verify.clicked.connect(self.verify_message)

    def _notify(self, title: str, text: str, icon=QMessageBox.Information):
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

    def _info(self) -> str:
        return self.ui.txt_info.toPlainText().strip()

    def _signature(self) -> str:
        return self.ui.txt_sign.toPlainText().strip()

    def generate_keys(self):
        try:
            data = self._request_json("get", "/generate_keys")
        except requests.RequestException as exc:
            self._notify("API error", f"Cannot generate keys:\n{exc}", QMessageBox.Critical)
            return
        self._notify("ECC", data.get("message", "Keys generated successfully"))

    def sign_message(self):
        info = self._info()
        if not info:
            self._notify("Input missing", "Please enter information first.", QMessageBox.Warning)
            return

        try:
            data = self._request_json("post", "/sign", {"message": info})
        except requests.RequestException as exc:
            self._notify("API error", f"Cannot sign:\n{exc}", QMessageBox.Critical)
            return

        self.ui.txt_sign.setPlainText(data.get("signature", ""))
        self._notify("ECC", "Signed successfully")

    def verify_message(self):
        info = self._info()
        signature = self._signature()
        if not info or not signature:
            self._notify("Input missing", "Please enter both information and signature.", QMessageBox.Warning)
            return

        try:
            data = self._request_json("post", "/verify", {"message": info, "signature": signature})
        except requests.RequestException as exc:
            self._notify("API error", f"Cannot verify:\n{exc}", QMessageBox.Critical)
            return

        if data.get("is_verified"):
            self._notify("ECC", "Verified successfully")
        else:
            self._notify("ECC", "Verification failed", QMessageBox.Warning)


def main():
    app = QApplication(sys.argv)
    window = ECCWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

