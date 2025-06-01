import base64

import requests


class IntervalsAPI:
    """
    A class to interact with the Intervals.icu API for uploading training data.
    """

    ZONE_TYPE = "HR"  # "Pace"
    BASE_URL = "https://intervals.icu/api/v1/athlete"
    # Encode "API_KEY:api_key" in Base64 for the Authorization header

    def __init__(self, athlete_id, api_key):
        self.athlete_id = athlete_id
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Basic {self.encode_auth(api_key)}",
            "Content-Type": "application/json"
        }

    def encode_auth(self, api_key):
        token = f"API_KEY:{api_key}".encode("utf-8")
        return base64.b64encode(token).decode("utf-8")

    def get(self, *args, **kwargs):
        """
        Make a GET request to the Intervals.icu API.
        """
        return requests.get(headers=self.headers, *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Make a POST request to the Intervals.icu API.
        """
        return requests.post(headers=self.headers, *args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Make a PUT request to the Intervals.icu API.
        """
        return requests.put(headers=self.headers, *args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Make a DELETE request to the Intervals.icu API.
        """
        return requests.delete(headers=self.headers, *args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Make a PATCH request to the Intervals.icu API.
        """
        return requests.patch(headers=self.headers, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None
