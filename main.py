import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from gui.main import Ui_main
import sys
from library.encrypt import encrypt, decrypt

class EncryptionApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.browseFile)
        self.ui.pushButton_4.clicked.connect(self.browseSalt)
        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)

    def browseFile(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
        self.ui.textEdit.setText(self.file[0])

    def browseSalt(self):
        self.salt = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
        self.ui.textEdit_2.setText(self.salt[0])

    def encrypt(self):
        file_path = self.ui.textEdit.toPlainText()
        encrypt(file_path)

    def decrypt(self):
        file_path = self.ui.textEdit.toPlainText()
        salt_path = self.ui.textEdit_2.toPlainText()

        decrypt(file_path, salt_path)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EncryptionApp()
    window.show()
    sys.exit(app.exec_())