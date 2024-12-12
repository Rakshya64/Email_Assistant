import unittest
from app import app  # Import the application object


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create the test client here
        self.app.testing = True  # Set testing flag

    # Test the /generate-email route for a POST request
    def test_generate_email_post(self):
        # Send a POST request to the route
        data = {"data": "Generate email for scholarship"}  # Fix data format
        response = self.app.post('/generate-email', json=data)

        # Check the status code
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    unittest.main()