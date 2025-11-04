from PyQt5 import QtWidgets, QtCore

class DecryptPasswordDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Password")
        self.setFixedSize(350, 120)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Label
        self.label = QtWidgets.QLabel("Please enter the password to decrypt the file:")
        layout.addWidget(self.label)

        # Password input
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Buttons
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_password(self):
        """Executes the dialog and returns the password if OK pressed, else None."""
        result = self.exec_()
        if result == QtWidgets.QDialog.Accepted:
            return self.password_input.text()
        return None
