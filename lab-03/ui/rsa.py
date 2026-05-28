# -*- coding: utf-8 -*-

import os
from pathlib import Path

os.environ.setdefault(
    "QT_QPA_PLATFORM_PLUGIN_PATH",
    str(Path(__file__).resolve().parent.parent / "platforms"),
)

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 760)
        MainWindow.setMinimumSize(QtCore.QSize(840, 760))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.root_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.root_layout.setContentsMargins(24, 20, 24, 20)
        self.root_layout.setSpacing(14)

        self.title = QtWidgets.QLabel(self.centralwidget)
        title_font = QtGui.QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        self.title.setFont(title_font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.root_layout.addWidget(self.title)

        self.form_layout = QtWidgets.QGridLayout()
        self.form_layout.setHorizontalSpacing(14)
        self.form_layout.setVerticalSpacing(12)

        self.label_plain = QtWidgets.QLabel(self.centralwidget)
        self.label_plain.setObjectName("label_plain")
        self.label_plain.setMinimumWidth(110)
        self.form_layout.addWidget(self.label_plain, 0, 0, QtCore.Qt.AlignTop)

        self.txt_plain_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_plain_text.setObjectName("txt_plain_text")
        self.txt_plain_text.setMinimumHeight(120)
        self.form_layout.addWidget(self.txt_plain_text, 0, 1)

        self.label_cipher = QtWidgets.QLabel(self.centralwidget)
        self.label_cipher.setObjectName("label_cipher")
        self.label_cipher.setMinimumWidth(110)
        self.form_layout.addWidget(self.label_cipher, 1, 0, QtCore.Qt.AlignTop)

        self.txt_cipher_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_cipher_text.setObjectName("txt_cipher_text")
        self.txt_cipher_text.setMinimumHeight(120)
        self.form_layout.addWidget(self.txt_cipher_text, 1, 1)

        self.label_info = QtWidgets.QLabel(self.centralwidget)
        self.label_info.setObjectName("label_info")
        self.label_info.setMinimumWidth(110)
        self.form_layout.addWidget(self.label_info, 2, 0, QtCore.Qt.AlignTop)

        self.txt_info = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_info.setObjectName("txt_info")
        self.txt_info.setMinimumHeight(80)
        self.form_layout.addWidget(self.txt_info, 2, 1)

        self.label_sign = QtWidgets.QLabel(self.centralwidget)
        self.label_sign.setObjectName("label_sign")
        self.label_sign.setMinimumWidth(110)
        self.form_layout.addWidget(self.label_sign, 3, 0, QtCore.Qt.AlignTop)

        self.txt_sign = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_sign.setObjectName("txt_sign")
        self.txt_sign.setMinimumHeight(90)
        self.form_layout.addWidget(self.txt_sign, 3, 1)

        self.root_layout.addLayout(self.form_layout)

        self.button_row = QtWidgets.QHBoxLayout()
        self.button_row.setSpacing(12)

        self.btn_gen_keys = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gen_keys.setObjectName("btn_gen_keys")
        self.button_row.addWidget(self.btn_gen_keys)

        self.btn_encrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_encrypt.setObjectName("btn_encrypt")
        self.button_row.addWidget(self.btn_encrypt)

        self.btn_decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_decrypt.setObjectName("btn_decrypt")
        self.button_row.addWidget(self.btn_decrypt)

        self.btn_sign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sign.setObjectName("btn_sign")
        self.button_row.addWidget(self.btn_sign)

        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setObjectName("btn_verify")
        self.button_row.addWidget(self.btn_verify)

        self.root_layout.addLayout(self.button_row)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(translate("MainWindow", "RSAWindow"))
        self.title.setText(translate("MainWindow", "RSA Cipher"))
        self.label_plain.setText(translate("MainWindow", "Plaintext:"))
        self.label_cipher.setText(translate("MainWindow", "Ciphertext:"))
        self.label_info.setText(translate("MainWindow", "Information:"))
        self.label_sign.setText(translate("MainWindow", "Signature:"))
        self.btn_gen_keys.setText(translate("MainWindow", "Gen Keys"))
        self.btn_encrypt.setText(translate("MainWindow", "Encrypt"))
        self.btn_decrypt.setText(translate("MainWindow", "Decrypt"))
        self.btn_sign.setText(translate("MainWindow", "Sign"))
        self.btn_verify.setText(translate("MainWindow", "Verify"))
