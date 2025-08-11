import sys
import os




import unittest
from api_client import LeakCheckAPIClient
from cache.cache_manager import CacheManager
import logging
from typing import List, Dict

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.api_key = "your_api_key_here"  # Replace with a valid API key
        self.client = LeakCheckAPIClient(self.api_key)
        self.cache_manager = CacheManager()

    def test_get_breach_info(self):
        """
        Test retrieving breach information for a given email.
        """
        email = "test@example.com"
        breaches = self.client.get_breach_info(email)
        self.assertIsInstance(breaches, list)
        self.assertTrue(all(isinstance(breach, dict) for breach in breaches))

    def test_cache_mechanism(self):
        """
        Test the caching mechanism for API responses.
        """
        email = "test@example.com"
        params = {
            "key": self.api_key,
            "check": email,
        }
        # Clear cache before test
        self.cache_manager.clear()
        # First request should not be cached
        breaches = self.client.get_breach_info(email)
        self.assertIsInstance(breaches, list)
        # Second request should be cached
        cached_breaches = self.client.get_breach_info(email)
        self.assertEqual(breaches, cached_breaches)

    def test_logging(self):
        """
        Test logging for invalid email format.
        """
        with self.assertLogs(level='DEBUG') as log:
            email = "invalid_email_format"
            self.client.get_breach_info(email)
            self.assertIn("Invalid email format", log.output[0])

if __name__ == "__main__":
    unittest.main()
