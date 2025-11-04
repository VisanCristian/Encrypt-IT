import os
import base64
import zipfile

from PyQt5 import QtWidgets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from getpass import getpass

from library.generateUi import dialogManager

dm = dialogManager()

def generate_key(password:str, salt: bytes, iterations: int = 100000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def load_salt(saltfile):
    """Load the salt from the specified directory."""
    return open(saltfile + ".salt" if not saltfile.endswith(".salt") else saltfile, "rb").read()

def check_password(password: str) -> bool:
    if len(password) < 8:
        QtWidgets.QMessageBox.information(None, "Password Error", "Password must contain at least 8 characters.")
        return False
    if not any(char.isdigit() for char in password):
        QtWidgets.QMessageBox.information(None, "Password Error", "Password must contain at least one digit.")
        return False
    if not any(char.isupper() for char in password):
        QtWidgets.QMessageBox.information(None, "Password Error", "Password must contain at least one uppercase letter.")
        return False
    if not any(char.islower() for char in password):
        QtWidgets.QMessageBox.information(None, "Password Error", "Password must contain at least one lowercase letter.")
        return False
    if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for char in password):
        QtWidgets.QMessageBox.information(None, "Password Error", "Password must contain at least one special character.")
        return False
    return True


def encrypt(filename):
    """Encrypt a file using Fernet symmetric encryption."""
    if not os.path.exists(filename):
        dm.encryptFileNotFound()
        return None
    if filename.endswith('.enc'):
        dm.encryptAlreadyEncrypted()
        return None

    password = dm.encryptGetPassword();
    while not check_password(password):
        password = dm.encryptGetPassword();

    salt = os.urandom(32)
    key = generate_key(password, salt)


    folder = os.path.dirname(filename)
    saltfile = os.path.join(folder, os.path.basename(filename) + ".salt")
    encrypted_filename = os.path.join(folder, os.path.basename(filename) + ".enc")
    zip_filename = os.path.join(folder, os.path.basename(filename) + ".zip")


    count = 0
    while os.path.exists(zip_filename):
        zip_filename = filename + str(count) + ".zip"
        count += 1


    if os.path.exists(saltfile):
        overwrite = dm.encryptSaltFileExists();
        while overwrite != 'y' and overwrite != 'n':
            overwrite = dm.encryptSaltFileExists();
        if overwrite == 'y':
            os.remove(saltfile)

    with open(filename, "rb") as file_to_encrypt:
        data = file_to_encrypt.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(saltfile, "wb") as sf:
        sf.write(salt)
    os.chmod(saltfile, 0o600)
    dm.saltGenerated();


    with open(filename + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    os.chmod(filename + ".enc", 0o600)

    try:
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(encrypted_filename, arcname=os.path.basename(encrypted_filename))
            zipf.write(saltfile, arcname=os.path.basename(saltfile))
    except Exception:
        dm.encryptFailed()
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
    if os.path.exists(encrypted_filename):
        os.remove(encrypted_filename)
    if os.path.exists(saltfile):
        os.remove(saltfile)

    dm.encryptSuccessful()
    return None


def decrypt(filename, saltfile):
    """Decrypt a file using Fernet symmetric encryption."""
    if not os.path.exists(filename):
        dm.decryptFileNotFound()
        return None
    try:
        salt = load_salt(saltfile)
    except FileNotFoundError:
        dm.decryptSaltFileNotFound()
        return None
    password = dm.decryptGetPassword();
    key = generate_key(password, salt)
    fernet = Fernet(key)
    with open(filename, "rb") as file_to_decrypt:
        encrypted_data = file_to_decrypt.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(filename.replace(".enc", ""), "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
            dm.decryptSuccessful()
    except Exception:
        dm.decryptFailed();
        if os.path.exists(filename.replace(".enc", "")):
            os.remove(filename.replace(".enc", ""))
        return None
    return None

