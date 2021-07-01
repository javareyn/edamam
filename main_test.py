import unittest
from unittest.mock import patch
import main
import os.path
from os import path


NUTRITION_APP_ID = 'a409daa4'
NUTRITION_APP_KEY = 'ca9c243e5f2d70cff4d6a4997ea55d83'
BASE_URL = 'https://api.edamam.com'


class TestMain(unittest.TestCase):
    def test_create_url(self):
        self.assertEqual(
            main.create_url('/test'),
            f'{BASE_URL}/test'
            f'?app_id={NUTRITION_APP_ID}'
            f'&app_key={NUTRITION_APP_KEY}'
        )

    def test_transport_df_to_csv(self):
        data = {
            'test_key': 'test value'
        }
        file_name = main.transport_df_to_csv(data)
        self.assertTrue(path.exists(file_name))

    def test_fetch_response_if_1(self):
        with patch('main.requests.post') as mocked_post:
            mocked_post.return_value.ok = True


if __name__ == '__main__':
    unittest.main()
