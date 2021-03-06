import unittest
import requests


api_records_url = 'https://rnlgztvokc.execute-api.eu-west-1.amazonaws.com/v1/records'


class TestRecordsRestClient(unittest.TestCase):

    def test_get(self):
        resp = requests.get(api_records_url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET {} response:  {}'.format(api_records_url, resp.status_code))
        print(resp.json())


if __name__ == '__main__':
    unittest.main()