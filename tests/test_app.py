import unittest
from unittest.mock import patch
from flask import json
from app import app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the test client for Flask app."""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_home_status_code(self):
        """Test the home route ('/') for GET request."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<html>", response.data)

    def test_post_home_status_code(self):
        """Test the home route ('/') for POST request (should return 405)."""
        response = self.app.post('/')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    @patch('api.gemini_api.generate_email')  # Mock the generate_email function
    def test_generate_email_route_success(self, mock_generate_email):
        """Test the /generate-email route with valid input."""
        # Mock the response of generate_email function
        mock_generate_email.return_value = "Generated email content here."

        # Test data for the POST request
        test_data = {
            "to": "test@example.com",
            "message": "Hello!",
            "tone": "friendly"
        }

        response = self.app.post('/generate-email', json=test_data)
        self.assertEqual(response.status_code, 200)

        # Check the response JSON
        data = json.loads(response.data)
        self.assertIn("email", data)
        self.assertEqual(data["email"], "Generated email content here.")

    @patch('api.gemini_api.generate_email')  # Mock the generate_email function
    def test_generate_email_route_missing_fields(self, mock_generate_email):
        """Test the /generate-email route with missing fields."""
        test_data = {"to": "test@example.com"}  # Missing 'message' and 'tone'

        response = self.app.post('/generate-email', json=test_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_generate_email_route_no_json(self):
        """Test the /generate-email route with no JSON input."""
        response = self.app.post('/generate-email')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
