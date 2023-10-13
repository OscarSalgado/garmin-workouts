import pytest
from garminworkouts.garmin.garminclient import GarminClient
from datetime import date, timedelta
import sys
from typing import Any
from requests import Response


@pytest.mark.vcr
def test_external_workouts(authed_gclient: GarminClient) -> None:
    locale = 'en-US'
    url: str = f"web-data/workouts/{locale}/index_04_2022_d6f4482b-f983-4e55-9d8d-0061e160abe7.json"
    assert authed_gclient.garth.get("connect", url)


@pytest.mark.vcr
def test_get_external_workout(authed_gclient: GarminClient) -> None:
    locale = 'en-US'
    url: str = f"web-data/workouts/{locale}/index_04_2022_d6f4482b-f983-4e55-9d8d-0061e160abe7.json"
    workouts: Any = authed_gclient.garth.get("connect", url).json()['workouts']

    for workout in workouts:
        url: str = workout['filePath']
        assert authed_gclient.garth.get("connect", url)


@pytest.mark.vcr
def test_list_workouts(authed_gclient: GarminClient) -> None:
    batch_size = 100
    url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"
    for start_index in range(0, sys.maxsize, batch_size):
        params: dict[str, int] = {
            "start": start_index,
            "limit": batch_size
            }
        response: Response = authed_gclient.get(
            url,
            params=params, api=True)
        assert response
        if response.json() == []:
            break


@pytest.mark.vcr
def test_get_calendar(authed_gclient: GarminClient) -> None:
    year = str(date.today().year)
    month = str(date.today().month - 1)
    url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"

    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_list_events(authed_gclient: GarminClient) -> None:
    batch_size = 20
    url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/events"
    for start_index in range(1, sys.maxsize, batch_size):
        params: dict = {
            "startDate": date.today(),
            "pageIndex": start_index,
            "limit": batch_size
            }
        response: Response = authed_gclient.get(url, params=params)
        assert response
        if not response.json() or response.json() == []:
            break


@pytest.mark.vcr
def test_get_activities_by_date(authed_gclient: GarminClient) -> None:
    startdate: date = date.today() + timedelta(weeks=-4)
    enddate: str = date.today().isoformat()
    activitytype = None

    activities: list = []
    start = 0
    limit = 20

    url: str = f"{GarminClient._ACTIVITY_LIST_SERVICE_ENDPOINT}/activities/search/activities"
    params: dict[str, str] = {
        "startDate": str(startdate),
        "endDate": str(enddate),
        "start": str(start),
        "limit": str(limit),
    }
    if activitytype:
        params["activityType"] = str(activitytype)

    print(f"Requesting activities by date from {startdate} to {enddate}")
    while True:
        params["start"] = str(start)
        print(f"Requesting activities {start} to {start+limit}")
        act: Response = authed_gclient.get(url, params=params)
        assert act
        if act.json() != []:
            activities.extend(act)
            start = start + limit
        else:
            break


@pytest.mark.vcr
def test_list_workout_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/types"
    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_get_activity_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/activityTypes"
    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_get_event_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/eventTypes"
    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_get_golf_types(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._GOLF_COMMUNITY_ENDPOINT}/types"
    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_get_strength_types(authed_gclient: GarminClient) -> None:
    url: str = "/web-data/exercises/Exercises.json"
    assert authed_gclient.garth.get("connect", url)


@pytest.mark.vcr
def test_get_RHR(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._WELLNESS_SERVICE_ENDPOINT}/wellness/dailyHeartRate"
    params: dict = {
       "date": date.today(),
    }
    assert authed_gclient.get(url, params=params)


@pytest.mark.vcr
def test_get_hr_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_save_hr_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/heartRateZones"
    zones: Any = authed_gclient.get(url).json()
    assert authed_gclient.put(url, json=zones)


@pytest.mark.vcr
def test_get_power_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/sports/all"
    assert authed_gclient.get(url)


@pytest.mark.vcr
def test_save_power_zones(authed_gclient: GarminClient) -> None:
    url: str = f"{GarminClient._BIOMETRIC_SERVICE_ENDPOINT}/powerZones/all"
    zones: list[dict[str, Any]] = [
        {
            "sport": "CYCLING",
            "functionalThresholdPower": str(275),
            "zone1Floor": str(179),
            "zone2Floor": str(220),
            "zone3Floor": str(248),
            "zone4Floor": str(275),
            "zone5Floor": str(316),
            "zone6Floor": str(358),
            "zone7Floor": str(412),
            "userLocalTime": None
        },
        {
            "sport": "RUNNING",
            "functionalThresholdPower": str(380),
            "zone1Floor": str(247),
            "zone2Floor": str(304),
            "zone3Floor": str(342),
            "zone4Floor": str(380),
            "zone5Floor": str(437),
            "zone6Floor": str(0.0),
            "zone7Floor": str(0.0),
            "userLocalTime": None
        }
    ]
    assert authed_gclient.put(url, json=zones)