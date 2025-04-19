from datetime import date, timedelta
import logging
from typing import Any
from requests import Response
from garminworkouts.garmin.garmindownload import GarminDownload


class GarminActivity(GarminDownload):
    _ACTIVITY_LIST_SERVICE_ENDPOINT = "/activitylist-service"

    def get_activity(self, activity_id: str) -> dict:
        """
        Fetch detailed information about a specific activity by its ID.

        :param activity_id: The unique identifier of the activity.
        :return: A dictionary containing the activity details.
        """
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}"
        return self.get(url).json()

    def get_activity_workout(self, activity_id) -> Any:
        """
        Retrieves the workout associated with a specific activity.

        Args:
            activity_id (str): The unique identifier of the activity.

        Returns:
            Any: The first workout associated with the activity if available,
            otherwise an empty list.
        """
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}/workouts"
        a: dict = self.get(url).json()
        return [] if len(a) == 0 else a[0]

    def get_activities_by_date(self,
                               startdate=None, enddate=None,
                               activitytype=None,
                               minDistance=None, maxDistance=None,  # meters
                               minDuration=None, maxDuration=None,  # seconds
                               minElevation=None, maxElevation=None,  # meters
                               ) -> list[dict]:
        """
        Fetch available activities between specific dates with optional filters.
                            This method retrieves a list of activities from the Garmin API based on the
                            specified date range and optional filtering criteria such as activity type,
                            distance, duration, and elevation.
                            Parameters:
                                startdate (str, optional): The start date for filtering activities in
                                    the format 'YYYY-MM-DD'. Defaults to None.
                                enddate (str, optional): The end date for filtering activities in the
                                    format 'YYYY-MM-DD'. Defaults to None.
                                activitytype (str, optional): The type of activity to filter by.
                                    Possible values include 'cycling', 'running', 'swimming',
                                    'multi_sport', 'fitness_equipment', 'hiking', 'walking', and 'other'.
                                    Defaults to None.
                                minDistance (int, optional): The minimum distance (in meters) for
                                    filtering activities. Defaults to None.
                                maxDistance (int, optional): The maximum distance (in meters) for
                                    filtering activities. Defaults to None.
                                minDuration (int, optional): The minimum duration (in seconds) for
                                    filtering activities. Defaults to None.
                                maxDuration (int, optional): The maximum duration (in seconds) for
                                    filtering activities. Defaults to None.
                                minElevation (int, optional): The minimum elevation gain (in meters)
                                    for filtering activities. Defaults to None.
                                maxElevation (int, optional): The maximum elevation gain (in meters)
                                    for filtering activities. Defaults to None.
                            Returns:
                                list[dict]: A list of JSON objects representing the activities that
                                match the specified criteria.
                            Notes:
                                - The method fetches activities in batches of 20, mimicking the behavior
                                  of the web interface that loads more activities on scroll.
                                - If no activities are found, an empty list is returned.
        """

        activities: list = []
        start = 0
        limit = 20
        # mimicking the behavior of the web interface that fetches 20 activities at a time
        # and automatically loads more on scroll
        url: str = f"{self._ACTIVITY_LIST_SERVICE_ENDPOINT}/activities/search/activities"

        params: dict = {
            "startDate": str(startdate) if startdate else None,
            "endDate": str(enddate) if enddate else None,
            "start": str(start),
            "limit": str(limit),
            "activityType": str(activitytype) if activitytype else None,
            "minDistance": int(minDistance) if minDistance else None,
            "maxDistance": int(maxDistance) if maxDistance else None,
            "minDuration": int(minDuration) if minDuration else None,
            "maxDuration": int(maxDuration) if maxDuration else None,
            "minElevation": int(minElevation) if minElevation else None,
            "maxElevation": int(maxElevation) if maxElevation else None,
        }

        logging.info(f"Requesting activities by date from {startdate} to {enddate}")
        while True:
            params["start"] = str(start)
            logging.info(f"Requesting activities {start} to {start+limit}")
            act: Response = self.get(url, params=params).json()
            if act:
                activities.extend(act)
                start: int = start + limit
            else:
                break

        return activities

    def activity_list(self) -> None:
        """
        Retrieves a list of running activities within the last 7 days and downloads each activity.

        This method calculates the date range for the past week, fetches running activities
        within that range using `get_activities_by_date`, and downloads each activity by its ID.

        Returns:
            None
        """
        start_date: date = date.today() - timedelta(days=7)
        end_date: date = date.today()
        activities: list[dict] = self.get_activities_by_date(
            startdate=start_date, enddate=end_date, activitytype='running')
        for activity in activities:
            id: str = activity.get('activityId', '')
            logging.info("Downloading activity '%s'", id)
            self.download_activity(id)
