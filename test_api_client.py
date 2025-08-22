import unittest
from unittest.mock import patch, Mock
from api_client import LeakCheckAPIClient

class TestLeakCheckAPIClient(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.client = LeakCheckAPIClient(api_key=self.api_key)

    @patch('api_client.requests.get')
    def test_get_breach_info_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": [
                {"name": "Test Service", "date": "2023-01-01", "description": "Test breach"}
            ]
        }
        mock_get.return_value = mock_response

        email = "test@example.com"
        breaches = self.client.get_breach_info(email)

        self.assertEqual(len(breaches), 1)
        self.assertEqual(breaches[0]['service_name'], "Test Service")
        self.assertEqual(breaches[0]['breach_date'], "2023-01-01")
        self.assertEqual(breaches[0]['description'], "Test breach")

    @patch('api_client.requests.get')
    def test_get_breach_info_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout

        email = "test@example.com"
        with self.assertRaises(TimeoutError):
            self.client.get_breach_info(email)

    @patch('api_client.requests.get')
    def test_get_breach_info_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError

        email = "test@example.com"
        with self.assertRaises(ConnectionError):
            self.client.get_breach_info(email)

    @patch('api_client.requests.get')
    def test_get_breach_info_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        email = "test@example.com"
        with self.assertRaises(ValueError):
            self.client.get_breach_info(email)

    @patch('api_client.requests.get')
    def test_get_breach_info_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError
        mock_get.return_value = mock_response

        email = "test@example.com"
        breaches = self.client.get_breach_info(email)

        self.assertEqual(len(breaches), 0)

    @patch('api_client.requests.get')
    def test_get_breach_info_no_breaches(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": []
        }
        mock_get.return_value = mock_response

        email = "test@example.com"
        breaches = self.client.get_breach_info(email)

        self.assertEqual(len(breaches), 0)

    @patch('api_client.requests.get')
    def test_get_breach_info_by_username_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": [
                {"name": "Test Service", "date": "2023-01-01", "description": "Test breach"}
            ]
        }
        mock_get.return_value = mock_response

        username = "test_user"
        breaches = self.client.get_breach_info_by_username(username)

        self.assertEqual(len(breaches), 1)
        self.assertEqual(breaches[0]['service_name'], "Test Service")
        self.assertEqual(breaches[0]['breach_date'], "2023-01-01")
        self.assertEqual(breaches[0]['description'], "Test breach")

    @patch('api_client.requests.get')
    def test_get_breach_info_by_username_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout

        username = "test_user"
        with self.assertRaises(TimeoutError):
            self.client.get_breach_info_by_username(username)

    @patch('api_client.requests.get')
    def test_get_breach_info_by_username_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError

        username = "test_user"
        with self.assertRaises(ConnectionError):
            self.client.get_breach_info_by_username(username)

    @patch('api_client.requests.get')
    def test_get_breach_info_by_username_http_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        username = "test_user"
        with self.assertRaises(ValueError):
            self.client.get_breach_info_by_username(username)

    @patch('api_client.requests.get')
    def test_get_breach_info_by_username_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError
        mock_get.return_value = mock_response

        username = "test_user"
        breaches = self.client.get_breach_info_by_username(username)

        self.assertEqual(len(breaches), 0)

    @patch('api_client.requests.get')
    def test_get_breach_info_by_username_no_breaches(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": []
        }
        mock_get.return_value = mock_response

        username = "test_user"
        breaches = self.client.get_breach_info_by_username(username)

        self.assertEqual(len(breaches), 0)

if __name__ == '__main__':
    unittest.main()
