from unittest import mock
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.__main__ import (_garmin_client, update_garmin, command_update_types,
                                     command_activity_list, command_trainingplan_list, command_challenge_list,
                                     command_workout_list, command_event_list)


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_workout_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_workout_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_event_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_event_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_challenge_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_challenge_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_trainingplan_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_trainingplan_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_activity_list(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_activity_list(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_command_update_types(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert command_update_types(None) is None


@mock.patch('garminworkouts.__main__._garmin_client')
def test_update_garmin(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient

    assert update_garmin(None) is None


@mock.patch('garminworkouts.garmin.garminclient.GarminClient')
def test__garmin_client(mock_garmin_client) -> None:
    # Mock the GarminClient class
    mock_garmin_client.return_value.__enter__.return_value = mock_garmin_client

    # Call the _garmin_client function
    result: GarminClient = _garmin_client()

    # Assert that the result is an instance of GarminClient
    assert isinstance(result, GarminClient)
