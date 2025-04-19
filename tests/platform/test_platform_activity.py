from garminworkouts.garmin.garminclient import GarminClient
from unittest.mock import patch, MagicMock
import os
import shutil


def custom_get_side_effect(url, params) -> MagicMock:
    a = MagicMock(status_code=404)
    if url == "/activitylist-service/activities/search/activities" and params.get('start') == '0':
        a = MagicMock(json=lambda: {'uuid': '123'})
    elif url == "/activitylist-service/activities/search/activities":
        a = MagicMock(json=lambda: None)
    return a


def test_get_activities_by_date(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        mock_get.side_effect = custom_get_side_effect
        act_list: list[dict] = authed_gclient.get_activities_by_date()
        assert len(act_list) >= 0


def test_get_activity(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        activity_id = '123'
        mock_get.return_value.json.return_value = [{'uuid': '123'}]

        act: dict = authed_gclient.get_activity(activity_id)
        mock_get.assert_called_once_with(f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}")
        assert act


def test_get_activity_workout(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'get') as mock_get:
        activity_id = 123
        mock_get.return_value.json.return_value = [{'uuid': '123'}]

        act: dict = authed_gclient.get_activity_workout(activity_id)
        mock_get.assert_called_once_with(f"{GarminClient._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}/workouts")
        assert act


def test_download_activity(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, 'download') as mock_download:
        activity_id = 123
        mock_download.return_value = b'{"uuid": "123"}'

        act: bytes = authed_gclient.download_activity(activity_id)
        mock_download.assert_called_once_with(f"{GarminClient._DOWNLOAD_SERVICE}/activity/{activity_id}")
        assert act

        output_file: str = f"./activities/{str(activity_id)}.zip"
        os.remove(output_file)
        shutil.rmtree("./activities")
