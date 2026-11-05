import argparse
import os
import sys
from unittest import mock

import pytest
from garminconnect import (GarminConnectAuthenticationError, GarminConnectConnectionError,
                           GarminConnectTooManyRequestsError)
from garminworkouts.garmin.garminclient import GarminClient
from garminworkouts.__main__ import (_garmin_client, safe_api_call, command_event_get, command_event_import,
                                     command_trainingplan_import, command_trainingplan_metrics,
                                     command_workout_get,
                                     )
from garminworkouts.models.event import Event
from garminworkouts.models.workout import Workout


@mock.patch('garminworkouts.__main__.GarminClient')
def test__garmin_client_success(mock_garmin, monkeypatch, tmp_path) -> None:
    monkeypatch.setattr('account.config', _environ_only_config)
    monkeypatch.setenv('GARMINTOKENS', str(tmp_path / 'tokens'))

    # Mock the GarminClient class (never touch the real Garmin SSO)
    mock_instance = mock.MagicMock()
    mock_instance.login.return_value = True
    mock_garmin.return_value = mock_instance

    result = _garmin_client()

    mock_garmin.assert_called_once()
    mock_instance.login.assert_called_once_with(str(tmp_path / 'tokens'))
    assert result is mock_instance


@mock.patch('garminworkouts.__main__._garmin_client')
def test_trainingplan_import(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

    with mock.patch.object(authed_gclient, 'update_workouts') as mock_update_workouts, \
         mock.patch.object(authed_gclient, 'get_calendar') as mock_get_calendar, \
         mock.patch.object(authed_gclient, 'update_notes') as mock_update_notes:
        mock_update_workouts.return_value = None
        mock_get_calendar.return_value = None, None, None
        mock_update_notes.return_value = None

        command_trainingplan_import(args)
        assert mock_update_workouts.call_count == 1
        assert mock_get_calendar.call_count == 1
        assert mock_update_notes.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_event_import(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='Races/*.yaml')

    with mock.patch.object(authed_gclient, 'update_workouts') as mock_update_workouts, \
            mock.patch.object(authed_gclient, 'get_calendar') as mock_get_calendar, \
            mock.patch.object(authed_gclient, 'update_events') as mock_update_events:
        mock_update_workouts.return_value = None
        mock_get_calendar.return_value = None, None, None
        mock_update_events.return_value = None

        command_event_import(args)
        assert mock_update_workouts.call_count == 1
        assert mock_get_calendar.call_count == 1
        assert mock_update_events.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_trainingplan_metrics(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(trainingplan='trainingplans/*/Garmin/5k/Beginner/HeartRate/*.yaml')

    with mock.patch.object(Workout, 'load_metrics') as mock_trainingplan_metrics:
        mock_trainingplan_metrics.return_value = None

        command_trainingplan_metrics(args)
        assert mock_trainingplan_metrics.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_workout_get(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(id='1')

    with mock.patch.object(Workout, 'print_workout_json') as mock_workout_print, \
         mock.patch.object(authed_gclient, 'get_workout') as mock_workout_get:
        mock_workout_print.return_value = None
        mock_workout_get.return_value = None

        command_workout_get(args)
        assert mock_workout_get.call_count == 1
        assert mock_workout_print.call_count == 1


@mock.patch('garminworkouts.__main__._garmin_client')
def test_event_get(mock_garmin_client, authed_gclient: GarminClient) -> None:
    mock_garmin_client.return_value = authed_gclient
    args = argparse.Namespace(id='1')

    with mock.patch.object(Event, 'print_event_json') as mock_event_print, \
            mock.patch.object(authed_gclient, 'get_event') as mock_event_get:
        mock_event_print.return_value = None
        mock_event_get.return_value = None

        command_event_get(args)
        assert mock_event_get.call_count == 1
        assert mock_event_print.call_count == 1


# --- _garmin_client: bounded login (never touches the network or sleeps for real) ---

def _environ_only_config(key, default=None, **_):
    """Stand-in for decouple.config that ignores any developer .env file."""
    return os.environ.get(key, default)


@pytest.fixture
def login_env(monkeypatch, tmp_path):
    """Isolated environment: fake token store, no credentials, patched GarminClient and sleep."""
    monkeypatch.setenv('GARMINTOKENS', str(tmp_path / 'tokens'))
    for name in ('GARMIN_USERNAME', 'GARMIN_PASSWORD', 'EMAIL', 'PASSWORD'):
        monkeypatch.delenv(name, raising=False)
    # A developer terminal by default; headless tests switch it off.
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: True, raising=False)
    monkeypatch.setattr('account.config', _environ_only_config)
    with mock.patch('garminworkouts.__main__.GarminClient') as client_cls, mock.patch('garminworkouts.__main__.time.sleep') as sleep, mock.patch('garminworkouts.__main__.input', return_value='user@example.com', create=True), mock.patch('garminworkouts.__main__.getpass', return_value='secret'):
        instance = client_cls.return_value
        instance.login.return_value = False
        yield mock.Mock(instance=instance, sleep=sleep)


def test_garmin_client_env_credentials_fail_fast(login_env, monkeypatch) -> None:
    monkeypatch.setenv('GARMIN_USERNAME', 'user@example.com')
    monkeypatch.setenv('GARMIN_PASSWORD', 'secret')

    with pytest.raises(SystemExit) as exc:
        _garmin_client()

    assert exc.value.code == 1
    # 1 call restoring saved tokens + exactly 1 credential attempt, no retry and no pause
    assert login_env.instance.login.call_count == 2
    login_env.sleep.assert_not_called()


def test_garmin_client_interactive_attempts_are_bounded(login_env) -> None:
    assert _garmin_client() is None

    # 1 call restoring saved tokens + 3 interactive attempts
    assert login_env.instance.login.call_count == 4
    assert [c.args[0] for c in login_env.sleep.call_args_list] == [1, 2]


def test_garmin_client_interactive_succeeds_on_retry(login_env) -> None:
    login_env.instance.login.side_effect = [False, False, True]

    assert _garmin_client() is login_env.instance
    assert login_env.instance.login.call_count == 3
    login_env.sleep.assert_called_once_with(1)


def test_garmin_client_legacy_env_credentials_fail_fast(login_env, monkeypatch) -> None:
    monkeypatch.setenv('EMAIL', 'user@example.com')
    monkeypatch.setenv('PASSWORD', 'secret')

    with pytest.raises(SystemExit) as exc:
        _garmin_client()

    assert exc.value.code == 1
    assert login_env.instance.login.call_count == 2


def test_garmin_client_headless_without_tokens_or_credentials_exits(login_env, monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: False, raising=False)
    with mock.patch('garminworkouts.__main__.input', create=True) as fake_input, \
            mock.patch('garminworkouts.__main__.getpass') as fake_getpass:
        with pytest.raises(SystemExit) as exc:
            _garmin_client()

    assert exc.value.code == 1
    fake_input.assert_not_called()
    fake_getpass.assert_not_called()
    out = capsys.readouterr().out
    assert 'GARMIN_USERNAME' in out and 'GARMIN_PASSWORD' in out and 'GARMINTOKENS' in out
    # Only the attempt to restore saved tokens happened
    assert login_env.instance.login.call_count == 1


def test_garmin_client_headless_with_partial_credentials_exits(login_env, monkeypatch) -> None:
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: False, raising=False)
    monkeypatch.setenv('GARMIN_USERNAME', 'user@example.com')

    with pytest.raises(SystemExit) as exc:
        _garmin_client()

    assert exc.value.code == 1


def test_garmin_client_headless_restores_saved_tokens(login_env, monkeypatch) -> None:
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: False, raising=False)
    login_env.instance.login.return_value = True

    assert _garmin_client() is login_env.instance


def test_garmin_client_partial_env_credentials_stay_bounded(login_env, monkeypatch) -> None:
    monkeypatch.setenv('GARMIN_USERNAME', 'user@example.com')

    assert _garmin_client() is None
    assert login_env.instance.login.call_count == 4


def test_garmin_client_keyboard_interrupt_stops_login(login_env) -> None:
    with mock.patch('garminworkouts.__main__.input', side_effect=KeyboardInterrupt, create=True):
        assert _garmin_client() is None

    assert login_env.instance.login.call_count == 1
    login_env.sleep.assert_not_called()


def test_garmin_client_rate_limit_from_login_exits(login_env) -> None:
    # Saved tokens fail quietly, then the credential login is rate limited: the typed error must
    # reach _garmin_client() (it used to be swallowed into False) and stop the flow at once.
    login_env.instance.login.side_effect = [False, GarminConnectTooManyRequestsError('429')]

    with pytest.raises(SystemExit) as exc:
        _garmin_client()

    assert exc.value.code == 75
    assert login_env.instance.login.call_count == 2
    login_env.sleep.assert_not_called()


def test_garmin_client_wrong_credentials_error_counts_as_an_attempt(login_env) -> None:
    login_env.instance.login.side_effect = [False] + [GarminConnectAuthenticationError('bad')] * 3

    assert _garmin_client() is None
    assert login_env.instance.login.call_count == 4


def test_garmin_client_restores_saved_tokens(login_env) -> None:
    login_env.instance.login.return_value = True

    assert _garmin_client() is login_env.instance
    assert login_env.instance.login.call_count == 1


def test_garmin_client_saved_tokens_rate_limited_exits(login_env) -> None:
    login_env.instance.login.side_effect = GarminConnectTooManyRequestsError('429')

    with pytest.raises(SystemExit) as exc:
        _garmin_client()

    assert exc.value.code == 75


def test_garmin_client_connection_error_during_login_returns_none(login_env) -> None:
    login_env.instance.login.side_effect = [False, GarminConnectConnectionError('down')]

    assert _garmin_client() is None
    assert login_env.instance.login.call_count == 2


# --- safe_api_call ---

def test_safe_api_call_success() -> None:
    assert safe_api_call(lambda a, b=0: a + b, 1, b=2) == (True, 3, None)


@pytest.mark.parametrize("error, expected", [
    (GarminConnectAuthenticationError('x'), 'Authentication error: x'),
    (GarminConnectTooManyRequestsError('x'), 'Rate limit exceeded: x'),
    (GarminConnectConnectionError('HTTP 400'), 'Not available (400)'),
    (GarminConnectConnectionError('HTTP 401'), 'Authentication required (401)'),
    (GarminConnectConnectionError('HTTP 403'), 'Access denied (403)'),
    (GarminConnectConnectionError('HTTP 404'), 'Not found (404)'),
    (GarminConnectConnectionError('HTTP 429'), 'Rate limit (429)'),
    (GarminConnectConnectionError('HTTP 500'), 'Server error (500)'),
    (GarminConnectConnectionError('boom'), 'Connection error: boom'),
    (ValueError('weird'), 'Unexpected error: weird'),
])
def test_safe_api_call_errors(error, expected) -> None:
    def fail():
        raise error

    ok, result, message = safe_api_call(fail)
    assert ok is False
    assert result is None
    assert message.startswith(expected)


def test_garmin_client_saved_tokens_rejected_falls_through_to_credentials(login_env) -> None:
    login_env.instance.login.side_effect = [GarminConnectAuthenticationError('stale'), True]

    assert _garmin_client() is login_env.instance
    assert login_env.instance.login.call_count == 2
