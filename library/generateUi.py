import sys

from PyQt5 import QtWidgets
from gui.encryptFileNotFound import Ui_Dialog
from gui.encryptFileAlreadyEncrypted import AlreadyEncrypted_dialog
from gui.encryptGetPassword import Ui_getPasswordDialog

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
