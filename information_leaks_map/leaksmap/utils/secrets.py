from cryptography.fernet import Fernet
import base64
import os

class EncryptedSecrets:
    """Класс для работы с зашифрованными секретами."""

    def __init__(self, key: bytes | None = None):
        """Инициализация с ключом шифрования или генерацией нового."""
        if key:
            self.key = key
        else:
            self.key = self._generate_key()
        self.cipher_suite = Fernet(self.key)

    def _generate_key(self) -> bytes:
        """Генерация нового ключа шифрования."""
        return Fernet.generate_key()

    def encrypt(self, data: str) -> str:
        """Шифрование данных."""
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        """Дешифрование данных."""
        return self.cipher_suite.decrypt(token.encode()).decode()

    def save_key_to_file(self, file_path: str):
        """Сохранение ключа в файл."""
        with open(file_path, "wb") as key_file:
            key_file.write(self.key)

    def load_key_from_file(self, file_path: str):
        """Загрузка ключа из файла."""
        with open(file_path, "rb") as key_file:
            self.key = key_file.read()
        self.cipher_suite = Fernet(self.key)

    @staticmethod
    def generate_secure_key() -> str:
        """Генерация безопасного ключа для .env.example."""
        key = base64.urlsafe_b64encode(os.urandom(32)).decode()
        return f"ENCRYPTED[{key}]"
