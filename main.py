from PySide6.QtWidgets import QApplication
import sys
import os
import json
import hashlib
from typing import Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui import LeakMapGUI

CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache_file_path(email: str) -> str:
    """
    Generate the cache file path for a given email.

    :param email: The email address to generate the cache file path for.
    :return: The cache file path.
    """
    email_hash = hashlib.md5(email.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{email_hash}.json")

def load_cache(email: str) -> Dict[str, str]:
    """
    Load the cache data for a given email.

    :param email: The email address to load the cache data for.
    :return: The cache data, or an empty dictionary if the cache file does not exist or is invalid.
    """
    cache_file = get_cache_file_path(email)
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_cache(email: str, data: Dict[str, str]) -> None:
    """
    Save the cache data for a given email.

    :param email: The email address to save the cache data 
    for.
    :param data: The cache data to save.
    """
    cache_file = get_cache_file_path(email)
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    except IOError:
        pass

def main():
    """
    Entry point of the program.

    Initializes and runs the LeakMapGUI application.
    """
    print("Starting the application...")
    app = QApplication(sys.argv)
    window = LeakMapGUI()
    window.show()
    print("Application started.")
    sys.exit(app.exec())

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()
