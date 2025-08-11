import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.api_client import LeakCheckAPIClient

print("Import successful")
