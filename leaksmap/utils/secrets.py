import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# Генерация ключа шифрования
def generate_encryption_key(password: str, salt: bytes) -> bytes:
    """
    Генерирует ключ шифрования на основе пароля и соли.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# Шифрование данных
def encrypt_data(data: str, key: bytes) -> str:
    """
    Шифрует данные с использованием ключа Fernet.
    """
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

# Дешифрование данных
def decrypt_data(encrypted_data: str, key: bytes) -> str:
    """
    Дешифрует данные с использованием ключа Fernet.
    """
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

# Загрузка ключа шифрования из переменной окружения
def load_encryption_key(password: str) -> bytes:
    """
    Загружает ключ шифрования из переменной окружения или генерирует новый.
    """
    salt = os.getenv("ENCRYPTION_SALT", "default_salt_value").encode()
    key = generate_encryption_key(password, salt)
    return key
