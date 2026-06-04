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
        MainWindow.resize(780, 440)
        MainWindow.setMinimumSize(QtCore.QSize(780, 440))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.root_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.root_layout.setContentsMargins(24, 18, 24, 18)
        self.root_layout.setSpacing(14)

        self.top_row = QtWidgets.QHBoxLayout()
        self.top_row.setSpacing(14)

        self.title = QtWidgets.QLabel(self.centralwidget)
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        self.title.setFont(title_font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.top_row.addStretch(1)
        self.top_row.addWidget(self.title)
        self.top_row.addStretch(1)

        self.btn_gen_keys = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gen_keys.setObjectName("btn_gen_keys")
        self.top_row.addWidget(self.btn_gen_keys)

        self.root_layout.addLayout(self.top_row)

        self.form_layout = QtWidgets.QGridLayout()
        self.form_layout.setHorizontalSpacing(14)
        self.form_layout.setVerticalSpacing(12)

        self.label_info = QtWidgets.QLabel(self.centralwidget)
        self.label_info.setMinimumWidth(110)
        self.label_info.setObjectName("label_info")
        self.form_layout.addWidget(self.label_info, 0, 0, QtCore.Qt.AlignTop)

        self.txt_info = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_info.setObjectName("txt_info")
        self.txt_info.setMinimumHeight(120)
        self.form_layout.addWidget(self.txt_info, 0, 1)

        self.label_sign = QtWidgets.QLabel(self.centralwidget)
        self.label_sign.setMinimumWidth(110)
        self.label_sign.setObjectName("label_sign")
        self.form_layout.addWidget(self.label_sign, 1, 0, QtCore.Qt.AlignTop)

        self.txt_sign = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_sign.setObjectName("txt_sign")
        self.txt_sign.setMinimumHeight(120)
        self.form_layout.addWidget(self.txt_sign, 1, 1)

        self.root_layout.addLayout(self.form_layout)

        self.button_row = QtWidgets.QHBoxLayout()
        self.button_row.setSpacing(12)

        self.btn_sign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sign.setObjectName("btn_sign")
        self.button_row.addStretch(1)
        self.button_row.addWidget(self.btn_sign)

        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setObjectName("btn_verify")
        self.button_row.addWidget(self.btn_verify)
        self.button_row.addStretch(1)

        self.root_layout.addLayout(self.button_row)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(translate("MainWindow", "ECCWindow"))
        self.title.setText(translate("MainWindow", "ECC Cipher"))
        self.btn_gen_keys.setText(translate("MainWindow", "Generate Keys"))
        self.label_info.setText(translate("MainWindow", "Information:"))
        self.label_sign.setText(translate("MainWindow", "Signature:"))
        self.btn_sign.setText(translate("MainWindow", "Sign"))
        self.btn_verify.setText(translate("MainWindow", "Verify"))


if __name__ == "__main__":
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from ecc_cipher import ECCWindow

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ECCWindow()
    MainWindow.show()
    sys.exit(app.exec_())
