import unittest
import json
from quart import Quart
from app import app as test_app

class TestApp(unittest.IsolatedAsyncioTestCase):
    async def test_create_card(self):
        # instantiate the test_client
        test_client = test_app.test_client()

        # call the api endpoint
        test_endpoint = await test_client.post('/cards/',
                            {"question":"test_question", "answer":"test_answer"}
        )
        self.assertEqual(test_endpoint.status_code, 200)

        

if __name__ == "__main__":
    unittest.main()