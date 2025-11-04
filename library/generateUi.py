import sys

from PyQt5 import QtWidgets
from gui.encryptFileNotFound import Ui_Dialog
from gui.encryptFileAlreadyEncrypted import AlreadyEncrypted_dialog
from gui.encryptGetPassword import Ui_getPasswordDialog
from gui.UI_decryptGetPassword import DecryptPasswordDialog

class dialogManager:
    def __init__(self):
        self.app = QtWidgets.QApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication([])



    def encryptFileNotFound(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(dialog)
        ui.pushButton.clicked.connect(dialog.close)
        dialog.exec_()

    def encryptAlreadyEncrypted(self):
        dialog = QtWidgets.QDialog()
        ui = AlreadyEncrypted_dialog()
        ui.setupUi(dialog)
        ui.pushButton.clicked.connect(dialog.close)
        dialog.exec_()

    def encryptGetPassword(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_getPasswordDialog()
        ui.setupUi(dialog)
        ui.pushButton.clicked.connect(
            lambda:(
            QtWidgets.QMessageBox.warning("Warning", "Please enter both fields") if not ui.lineEdit.text() or not ui.lineEdit.text()
            else QtWidgets.QMessageBox.warning("Error", "Passwords must match") if ui.lineEdit.text() != ui.lineEdit.text()
            else dialog.accept())
        )
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            return ui.lineEdit.text()
        return None
    def encryptSaltExists(self):
        dialog = QtWidgets.QDialog()
        ui = QtWidgets.QMessageBox()
        ui.setIcon(QtWidgets.QMessageBox.Information)
        ui.setText("A salt file already exists. Do you want to overwrite it?")
        ui.setWindowTitle("Warning")
        ui.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        result = ui.exec_()
        if result == QtWidgets.QMessageBox.Yes:
            return True
    def saltGenerated(self):
        dialog = QtWidgets.QDialog()
        ui = QtWidgets.QMessageBox()
        ui.setIcon(QtWidgets.QMessageBox.Information)
        ui.setText("Salt file has been generated. Use this file next time you want to decrypt your file")
        ui.setWindowTitle("Information")
        ui.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result = ui.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            return True

    def encryptSuccessful(self):
        dialog = QtWidgets.QDialog()
        ui = QtWidgets.QMessageBox()
        ui.setIcon(QtWidgets.QMessageBox.Information)
        ui.setText("File has been encrypted successfully")
        ui.setWindowTitle("Information")
        ui.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result = ui.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            return True

    def decryptFileNotFound(self):
        dialog = QtWidgets.QDialog()
        ui = QtWidgets.QMessageBox()
        ui.setIcon(QtWidgets.QMessageBox.Information)
        ui.setText("File to decrypt not found")
        ui.setWindowTitle("Information")
        ui.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result = ui.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            return True

    def decryptSaltNotFound(self):
        dialog = QtWidgets.QDialog()
        ui = QtWidgets.QMessageBox()
        ui.setIcon(QtWidgets.QMessageBox.Information)
        ui.setText("Salt file not found")
        ui.setWindowTitle("Information")
        ui.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result = ui.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            return True
    def decryptSuccessful(self):
        dialog = QtWidgets.QDialog()
        ui = QtWidgets.QMessageBox()
        ui.setIcon(QtWidgets.QMessageBox.Information)
        ui.setText("File has been decrypted successfully")
        ui.setWindowTitle("Information")
        ui.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result = ui.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            return True
    def decryptFailed(self):
        dialog = QtWidgets.QDialog()
        ui = QtWidgets.QMessageBox()
        ui.setIcon(QtWidgets.QMessageBox.Information)
        ui.setText("Wrong password")
        ui.setWindowTitle("Information")
        ui.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result = ui.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            return True
    def decryptGetPassword(self):
        ui = DecryptPasswordDialog()
        result = ui.exec_()
        if result == QtWidgets.QDialog.Accepted:
            return ui.password_input.text()
        return None
