import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from getpass import getpass

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

def check_password(password: str, confirm_password: str) -> bool:
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return False
    if len(password) < 8:
        print("Password is too short. Please use at least 8 characters.")
        return False
    if not any (char.isdigit() for char in password):
        print("Password must contain at least one digit.")
        return False
    if not any (char.isupper() for char in password):
        print("Password must contain at least one uppercase letter.")
        return False
    if not any (char.islower() for char in password):
        print("Password must contain at least one lowercase letter.")
        return False
    if not any (char in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for char in password):
        print("Password must contain at least one special character.")
        return False
    return True

def encrypt(filename):
    """Encrypt a file using Fernet symmetric encryption."""
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        return None
    if filename.endswith('.enc'):
        print("You have already previously encrypted this file.")
        return None

    password = getpass("Please input a strong password to generate the key for encryption: ")
    confirm_password = getpass("Please confirm your password: ")
    while not check_password(password, confirm_password):
        password = getpass("Please input a strong password to generate the key for encryption: ")
        confirm_password = getpass("Please confirm your password: ")
    salt = os.urandom(32)
    key = generate_key(password, salt)
    saltfile = filename + ".salt"
    if os.path.exists(saltfile):
        print(f"Salt file {saltfile} already exists. Do you want to Overwrite it? (y/n)")
        overwrite = input().lower()
        while overwrite != 'y' and overwrite != 'n':
            print("This is not a valid option. Please choose (y)es or (n)o:")
            overwrite = input().lower()
        if overwrite == 'y':
            os.remove(saltfile)

    with open(filename, "rb") as file_to_encrypt:
        data = file_to_encrypt.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(saltfile, "wb") as sf:
        sf.write(salt)
    os.chmod(saltfile, 0o600)
    print(f"Salt saved to '{saltfile}'. You need this file in order to decrypt the file later.")
    with open(filename + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    os.chmod(filename + ".enc", 0o600)
    print("Encryption successful.")
    return None


def decrypt(filename):
    """Decrypt a file using Fernet symmetric encryption."""
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return None
    if not filename.endswith('.enc'):
        print("The file is not encrypted (missing .enc extension).")
        return None
    print("Please input the saltfile you want to use to decrypt the file:")
    try:
        saltfile = input()
        salt = load_salt(saltfile)
    except FileNotFoundError:
        print("Salt file not found. Decryption cannot proceed.")
        return None
    password = getpass("Please input the password:")
    key = generate_key(password, salt)
    fernet = Fernet(key)
    with open(filename, "rb") as file_to_decrypt:
        encrypted_data = file_to_decrypt.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(filename.replace(".enc", ""), "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
        print("Decryption successful.")
    except Exception:
        print("Decryption failed. Please check your password and salt file.")
        if os.path.exists(filename.replace(".enc", "")):
            os.remove(filename.replace(".enc", ""))
        return None
    return None


if __name__ == "__main__":
    while True:
        print("Would you like to (e)ncrypt or (d)ecrypt a file? (Type 'exit' to quit)")
        action = input().lower()
        if action == 'exit':
            break
        while action != 'e' and action != 'd':
            print("This is not a valid option. Please choose (e)ncrypt or (d)ecrypt:")
            action = input().lower()
        print(f"Please input the filename you would like to {'encrypt' if action == 'e' else 'decrypt'}:")
        file = input()
        if action == 'e':
            encrypt(file)
        else:
            decrypt(file)
