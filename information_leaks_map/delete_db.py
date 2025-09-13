import os
import time

def delete_db_file(file_path, retries=5, delay=2):
    for attempt in range(retries):
        try:
            os.remove(file_path)
            print(f"Successfully deleted {file_path}")
            return
        except PermissionError:
            print(f"PermissionError: Unable to delete {file_path}. The file is likely in use by another process. Retrying... (Attempt {attempt + 1}/{retries})")
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        time.sleep(delay)
    print(f"Failed to delete {file_path} after {retries} attempts.")

if __name__ == "__main__":
    db_path = "db.sqlite3"
    delete_db_file(db_path)
