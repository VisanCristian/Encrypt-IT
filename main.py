import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from gui.main_ui import Ui_Dialog
import sys
from library.encrypt import encrypt, decrypt
#
class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  # 'self' este QDialog, self.ui e UI-ul

        # Conectează butoanele
        self.ui.pushButton.clicked.connect(self.encrypt_file)
        self.ui.pushButton_2.clicked.connect(self.decrypt_file)

    def encrypt_file(self):
        file_path = self.ui.lineEdit.text()
        salt = self.ui.lineEdit_2.text()
        encrypt(file_path)

    def decrypt_file(self):
        file_path = self.ui.lineEdit.text()
        salt = self.ui.lineEdit_2.text()
        decrypt(file_path, salt)

# Run
app = QtWidgets.QApplication(sys.argv)
dialog = MyDialog()
dialog.show()
sys.exit(app.exec_())


app = QtWidgets.QApplication(sys.argv)
dialog = myDialog()
dialog.show()
sys.exit(app.exec_())
