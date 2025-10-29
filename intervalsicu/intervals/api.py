import base64
from datetime import date, timedelta
import logging
import requests


class IntervalsAPI(object):
    BASE = "https://intervals.icu/api/v1"
    BASE_URL = f"{BASE}/athlete"
    SUPPORTED_WORKOUT_TYPES = ['Run', 'Swim', 'Ride', 'Walk', 'WeightTraining', 'Other']

    """
    A class to interact with the Intervals.icu API for uploading training data.
    """
    # Encode "API_KEY:api_key" in Base64 for the Authorization header

    @staticmethod
    def format_sport(workout):
        sport = workout.config.get("sport", "").lower()
        if "cycl" in sport:
            return "Ride"
        if "run" in sport:
            return "Run"
        if "swim" in sport:
            return "Swim"
        if "walk" in sport:
            return "Walk"
        if "weight" in sport or "strength" in sport:
            return "WeightTraining"
        return "Other"

    @staticmethod
    def format_duration_string(h, m, s):
        # Fast string formatting, avoids unnecessary checks
        return (
            (f"{int(h)}h" if h else "") +
            (f"{int(m)}m" if m else "") +
            (f"{int(s)}s" if s else "")
        )

    @staticmethod
    def convert_duration(duration):
        if duration.endswith("km"):
            return float(duration[:-2]) * 1000  # km to meters
        if duration.endswith("m"):
            return int(duration[:-1]) * 60      # min to seconds
        if duration.endswith("s"):
            return int(duration[:-1])           # seconds
        try:
            return int(duration)
        except Exception:
            return 0

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

    # Upload training data to Intervals.icu
    def upload_workouts(self, data):
        url = f"{self.BASE_URL}/{self.athlete_id}/workouts/bulk"
        response = self.post(url, json=data)
        if response.status_code == 200:
            logging.info("Workouts uploaded successfully.")
        else:
            logging.error(f"Failed to upload workouts. Status code: {response.status_code}")

    # Upload training data to Intervals.icu
    def upload_events(self, data):
        url = f"{self.BASE_URL}/{self.athlete_id}/events/bulk"
        response = self.post(url, json=data)
        if response.status_code == 200:
            data[0].get('category', '').lower().capitalize()
            logging.info(f"{data[0].get('category', '').lower().capitalize()}s uploaded successfully.")
        else:
            logging.error(
                f"Failed to upload {data[0].get('category', '').lower()}s. "
                f"Status code: {response.status_code}"
            )

    def create_plan(self, plan_name: str, d: date, ctl: float = -1, atl: float = -1):
        """
        Create a new plan folder in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/folders"
        payload = {
            "auto_rollout_day": 7,
            "name": plan_name,
            "rollout_weeks": 2,
            "start_date_local": f"{d.isoformat()}T00:00:00",
            "starting_atl": atl,
            "starting_ctl": ctl,
            "type": "PLAN"
        }
        return self.post(url, json=payload).json()

    def delete_plan(self, plan_id: str):
        """
        Delete a plan folder in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/folders/{plan_id}"
        self.delete(url)

    def update_workout(self, workout_id: str, days_diff: int):
        """
        Update a workout in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/workouts/{workout_id}"
        payload = {
            "day": days_diff
        }
        self.put(url, json=payload)

    def list_workouts(self):
        url: str = f"{self.BASE_URL}/{self.athlete_id}/workouts"
        response = self.get(url)
        return response.json()

    def list_folders(self):
        url: str = f"{self.BASE_URL}/{self.athlete_id}/folders"
        response = self.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch folders. Status code: {response.status_code}")
            return []

    def delete_range_events(self, start_date: date | None = None, end_date: date | None = None):
        url: str = f"{self.BASE_URL}/{self.athlete_id}/events"
        start_date = start_date if start_date else (date.today() + timedelta(days=1))
        params = {
            'oldest': start_date.isoformat(),
            'newest': end_date.isoformat() if end_date else None,
            'category': ["WORKOUT", "TARGET"],
        }
        response = self.delete(url, params=params)
        if response.status_code == 200:
            logging.info("Events in range deleted successfully.")
        else:
            logging.error(f"Failed to delete events in range. Status code: {response.status_code}")
            logging.error(response.text)

    def get_sport_settings(self, sport):
        """
        Fetch the sport settings for the athlete.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/sport-settings"
        response = self.get(url)
        if response.status_code == 200:
            sport_settings = response.json()
            for s in sport_settings:
                if s.get("types")[0] == sport:
                    return s
                if s.get("types")[0] == 'Other':
                    return s
        else:
            logging.error(f"Failed to fetch sport settings. Status code: {response.status_code}")
            logging.error(response.text)
            return {}

    def update_threshold_pace(self, threshold_pace: float, id) -> None:
        """
        Update the threshold pace in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"threshold_pace": threshold_pace}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Threshold pace updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update threshold pace. Status code: {response.status_code}")
            logging.error(response.text)

    def update_max_hr(self, max_hr: int, id) -> None:
        """
        Update the maximum heart rate in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"max_hr": max_hr}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Maximum heart rate updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update maximum heart rate. Status code: {response.status_code}")
            logging.error(response.text)

    def update_resting_hr(self, resting_hr: int) -> None:
        """
        Update the resting heart rate in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}"
        payload = {"applyToAll": False, "icu_resting_hr": resting_hr, "localDate": date.today().isoformat()}
        response = self.put(url, json=payload)
        if response.status_code == 200:
            logging.info("Resting heart rate updated successfully.")
        else:
            logging.error(f"Failed to update resting heart rate. Status code: {response.status_code}")
            logging.error(response.text)

    def update_lthr(self, lthr: int, id) -> None:
        """
        Update the lactate threshold heart rate in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"lthr": lthr}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Lactate threshold heart rate updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update lactate threshold heart rate. Status code: {response.status_code}")
            logging.error(response.text)

    def update_hrrc_min_percent(self, hrrc_min_percent: float, id) -> None:
        """
        Update the heart rate reserve calculation minimum percentage in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"hrrc_min_percent": hrrc_min_percent}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Heart rate reserve calculation minimum percentage updated successfully. Id: %s", id)
        else:
            logging.error(
                f"Failed to update heart rate reserve calculation minimum percentage. "
                f"Status code: {response.status_code}"
            )
            logging.error(response.text)

    def update_ftp(self, ftp: int, indoor_ftp: int, id) -> None:
        """
        Update the functional threshold power in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"ftp": ftp, "indoor_ftp": indoor_ftp}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Functional threshold power updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update functional threshold power. Status code: {response.status_code}")
            logging.error(response.text)

    def update_wprime(self, wprime: int, id) -> None:
        """
        Update the W' (W prime) in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"wprime": wprime}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("W' (W prime) updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update W' (W prime). Status code: {response.status_code}")
            logging.error(response.text)

    def update_pmax(self, pmax: int, id) -> None:
        """
        Update the Pmax (Maximal Sprint Power) in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/sport-settings/{id}"
        payload = {"pmax": pmax}
        params = {"recalcHrZones": 'true'}
        response = self.put(url, json=payload, params=params)
        if response.status_code == 200:
            logging.info("Pmax (Maximal Sprint Power) updated successfully. Id: %s", id)
        else:
            logging.error(f"Failed to update Pmax (Maximal Sprint Power). Status code: {response.status_code}")
            logging.error(response.text)

    def set_target(self, monday, mileage, duration):
        """
        Set a target for the week in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/targets"
        payload = {
            "start_date_local": monday.isoformat() + "T00:00:00",
            "mileage": mileage,
            "duration": duration
        }
        response = self.post(url, json=payload)
        if response.status_code == 200:
            logging.info("Target set successfully.")
        else:
            logging.error(f"Failed to set target. Status code: {response.status_code}")
            logging.error(response.text)

    def get_wellness(self, date) -> dict:
        """
        Get wellness data from Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/wellness/{date.isoformat()}"
        response = self.get(url)
        if response.status_code == 200:
            logging.info("Wellness data retrieved successfully.")
            return response.json()
        else:
            logging.error(f"Failed to retrieve wellness data. Status code: {response.status_code}")
            logging.error(response.text)
            return {}

    def delete_workout(self, workout_id: str):
        """
        Delete a workout in Intervals.icu.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/workouts/{workout_id}"
        response = self.delete(url)
        if response.status_code == 200:
            logging.info("Workout %s deleted successfully.", workout_id)
        else:
            logging.error(f"Failed to delete workout. Status code: {response.status_code}")
            logging.error(response.text)

    def get_activities(self, start_date: date, end_date: date):
        """
        Get activities from Intervals.icu within a date range.
        """
        url = f"{self.BASE_URL}/{self.athlete_id}/activities"
        params = {
            "oldest": start_date.isoformat(),
            "newest": end_date.isoformat()
        }
        response = self.get(url, params=params)
        if response.status_code == 200:
            logging.info("Activities retrieved successfully.")
            # The API returns activities in oldest-first order. Many consumers
            # expect latest-first (reverse chronological). Return the reversed
            # list so callers receive activities newest -> oldest.
            data = response.json()
            if isinstance(data, list):
                return list(reversed(data))
            return data
        else:
            logging.error(f"Failed to retrieve activities. Status code: {response.status_code}")
            logging.error(response.text)
            return []

    def get_activity_stream(self, activity_id: str, stream_type: str):
        """
        Get activity stream data from Intervals.icu.
        """
        url = f"{self.BASE}/activity/{activity_id}/streams" + "{ext}"
        params = {
            'types': stream_type
        }
        response = self.get(url, params=params)
        if response.status_code == 200:
            logging.info("Activity stream data retrieved successfully.")
            if len(response.json()) == 0:
                return []
            else:
                return response.json()[0].get('data', [])
        else:
            logging.error(f"Failed to retrieve activity stream data. Status code: {response.status_code}")
            logging.error(response.text)
            return []
