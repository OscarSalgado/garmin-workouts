"""Request construction and status handling of IntervalsAPI, with the HTTP verbs stubbed out."""
import logging
from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from intervalsicu.intervals.api import IntervalsAPI

BASE = f"{IntervalsAPI.BASE_URL}/ath"


def _resp(status=200, payload=None, text="body") -> MagicMock:
    response = MagicMock(status_code=status, text=text)
    response.json.return_value = payload if payload is not None else {}
    return response


@pytest.fixture
def api() -> IntervalsAPI:
    return IntervalsAPI("ath", "key")


@pytest.mark.parametrize("verb", ["get", "post", "put", "delete", "patch"])
def test_verbs_default_headers_and_allow_override(api, verb) -> None:
    with patch(f"intervalsicu.intervals.api.requests.{verb}") as call:
        getattr(api, verb)("http://x")
        getattr(api, verb)("http://x", headers={"h": "1"})
    assert call.call_args_list[0].kwargs["headers"] == api.headers
    assert call.call_args_list[1].kwargs["headers"] == {"h": "1"}


def test_context_manager(api) -> None:
    with api as entered:
        assert entered is api


@pytest.mark.parametrize("status, level", [(200, logging.INFO), (500, logging.ERROR)])
def test_upload_workouts(api, caplog, status, level) -> None:
    with patch.object(api, "post", return_value=_resp(status)) as post, caplog.at_level(logging.INFO):
        api.upload_workouts([{"a": 1}])
    post.assert_called_once_with(f"{BASE}/workouts/bulk", json=[{"a": 1}])
    assert caplog.records[-1].levelno == level


@pytest.mark.parametrize("status, expected", [(200, "Workouts uploaded"), (500, "Failed to upload workouts")])
def test_upload_events(api, caplog, status, expected) -> None:
    with patch.object(api, "post", return_value=_resp(status)), caplog.at_level(logging.INFO):
        api.upload_events([{"category": "WORKOUT"}])
    assert expected in caplog.text


def test_create_plan(api) -> None:
    with patch.object(api, "post", return_value=_resp(payload={"id": 3})) as post:
        assert api.create_plan("Plan", date(2026, 1, 5), ctl=10, atl=5) == {"id": 3}
    payload = post.call_args.kwargs["json"]
    assert post.call_args.args[0] == f"{BASE}/folders"
    assert payload["start_date_local"] == "2026-01-05T00:00:00"
    assert payload["starting_ctl"] == 10 and payload["starting_atl"] == 5


def test_delete_plan_and_update_workout(api) -> None:
    with patch.object(api, "delete") as delete, patch.object(api, "put") as put:
        api.delete_plan("p1")
        api.update_workout("w1", 3)
    delete.assert_called_once_with(f"{BASE}/folders/p1")
    put.assert_called_once_with(f"{BASE}/workouts/w1", json={"day": 3})


def test_list_workouts(api) -> None:
    with patch.object(api, "get", return_value=_resp(payload=[{"id": 1}])) as get:
        assert api.list_workouts() == [{"id": 1}]
    get.assert_called_once_with(f"{BASE}/workouts")


def test_list_folders(api, caplog) -> None:
    with patch.object(api, "get", return_value=_resp(payload=[{"id": 1}])):
        assert api.list_folders() == [{"id": 1}]
    with patch.object(api, "get", return_value=_resp(404)), caplog.at_level(logging.ERROR):
        assert api.list_folders() == []
    assert "Failed to fetch folders" in caplog.text


@pytest.mark.parametrize("start, end, status", [
    (None, None, 200),
    (date(2026, 1, 1), date(2026, 2, 1), 200),
    (date(2026, 1, 1), None, 500),
])
def test_delete_range_events(api, caplog, start, end, status) -> None:
    with patch.object(api, "delete", return_value=_resp(status)) as delete, caplog.at_level(logging.INFO):
        api.delete_range_events(start, end)
    params = delete.call_args.kwargs["params"]
    assert params["oldest"] == (start or date.today()).isoformat()
    assert ("newest" in params) == (end is not None)
    assert ("deleted successfully" in caplog.text) == (status == 200)


@pytest.mark.parametrize("settings, expected", [
    ([{"types": ["Run"], "id": 1}, {"types": ["Ride"], "id": 2}], 1),                   # exact match
    ([{"types": ["Ride"], "id": 2}, {"types": ["Other"], "id": 3}], 3),                 # 'Other' fallback
    ([{"types": ["Other"], "id": 3}, {"types": ["Other"], "id": 4}], 3),                # first 'Other' wins
    ([{"types": ["Ride"], "id": 2}, {"types": [], "id": 5}], 2),                        # first candidate
    ([{"id": 6}], 6),                                                                   # missing types
])
def test_get_sport_settings_selection(api, settings, expected) -> None:
    with patch.object(api, "get", return_value=_resp(payload=settings)):
        assert api.get_sport_settings("Run")["id"] == expected


def test_get_sport_settings_empty_and_error(api, caplog) -> None:
    with patch.object(api, "get", return_value=_resp(payload=[])):
        assert api.get_sport_settings("Run") == {}
    with patch.object(api, "get", return_value=_resp(500)), caplog.at_level(logging.ERROR):
        assert api.get_sport_settings("Run") == {}
    assert "Failed to fetch sport settings" in caplog.text


SPORT_SETTING_UPDATES = [
    ("update_threshold_pace", (4.5, "7"), {"threshold_pace": 4.5}, "threshold pace"),
    ("update_max_hr", (190, "7"), {"max_hr": 190}, "maximum heart rate"),
    ("update_lthr", (170, "7"), {"lthr": 170}, "lactate threshold heart rate"),
    ("update_hrrc_min_percent", (0.3, "7"), {"hrrc_min_percent": 0.3}, "minimum percentage"),
    ("update_ftp", (250, 240, "7"), {"ftp": 250, "indoor_ftp": 240}, "functional threshold power"),
    ("update_wprime", (20000, "7"), {"wprime": 20000}, "W prime"),
    ("update_pmax", (900, "7"), {"pmax": 900}, "Pmax"),
]


@pytest.mark.parametrize("method, args, payload, label", SPORT_SETTING_UPDATES)
@pytest.mark.parametrize("status", [200, 500])
def test_sport_setting_updates(api, caplog, method, args, payload, label, status) -> None:
    with patch.object(api, "put", return_value=_resp(status)) as put, caplog.at_level(logging.INFO):
        getattr(api, method)(*args)
    assert put.call_args.args[0] == f"{BASE}/sport-settings/7"
    assert put.call_args.kwargs["json"] == payload
    assert put.call_args.kwargs["params"] == {"recalcHrZones": "true"}
    if status == 200:
        assert "updated successfully" in caplog.text
    else:
        assert "Failed to update" in caplog.text and label in caplog.text


@pytest.mark.parametrize("status", [200, 500])
def test_update_resting_hr(api, caplog, status) -> None:
    with patch.object(api, "put", return_value=_resp(status)) as put, caplog.at_level(logging.INFO):
        api.update_resting_hr(48)
    assert put.call_args.kwargs["json"]["icu_resting_hr"] == 48
    assert ("updated successfully" in caplog.text) == (status == 200)


@pytest.mark.parametrize("status", [200, 500])
def test_set_target(api, caplog, status) -> None:
    with patch.object(api, "post", return_value=_resp(status)) as post, caplog.at_level(logging.INFO):
        api.set_target(date(2026, 1, 5), 40, 7200)
    assert post.call_args.kwargs["json"] == {
        "start_date_local": "2026-01-05T00:00:00", "mileage": 40, "duration": 7200}
    assert ("Target set successfully" in caplog.text) == (status == 200)


def test_get_wellness(api, caplog) -> None:
    with patch.object(api, "get", return_value=_resp(payload={"hrv": 60})) as get:
        assert api.get_wellness(date(2026, 1, 5)) == {"hrv": 60}
    get.assert_called_once_with(f"{BASE}/wellness/2026-01-05")
    with patch.object(api, "get", return_value=_resp(404)), caplog.at_level(logging.ERROR):
        assert api.get_wellness(date(2026, 1, 5)) == {}
    assert "Failed to retrieve wellness data" in caplog.text


@pytest.mark.parametrize("status", [200, 500])
def test_delete_workout(api, caplog, status) -> None:
    with patch.object(api, "delete", return_value=_resp(status)) as delete, caplog.at_level(logging.INFO):
        api.delete_workout("w1")
    delete.assert_called_once_with(f"{BASE}/workouts/w1")
    assert ("deleted successfully" in caplog.text) == (status == 200)


def test_get_activities(api, caplog) -> None:
    start, end = date(2026, 1, 1), date(2026, 1, 31)
    with patch.object(api, "get", return_value=_resp(payload=[1, 2, 3])) as get:
        assert api.get_activities(start, end) == [3, 2, 1]
    assert get.call_args.kwargs["params"] == {"oldest": "2026-01-01", "newest": "2026-01-31"}
    with patch.object(api, "get", return_value=_resp(payload={"k": "v"})):
        assert api.get_activities(start, end) == {"k": "v"}
    with patch.object(api, "get", return_value=_resp(500)), caplog.at_level(logging.ERROR):
        assert api.get_activities(start, end) == []
    assert "Failed to retrieve activities" in caplog.text


def test_get_activity_stream(api, caplog) -> None:
    with patch.object(api, "get", return_value=_resp(payload=[{"data": [1, 2]}])) as get:
        assert api.get_activity_stream("a1", "heartrate") == [1, 2]
    assert get.call_args.kwargs["params"] == {"types": "heartrate"}
    with patch.object(api, "get", return_value=_resp(payload=[])):
        assert api.get_activity_stream("a1", "heartrate") == []
    with patch.object(api, "get", return_value=_resp(500)), caplog.at_level(logging.ERROR):
        assert api.get_activity_stream("a1", "heartrate") == []
    assert "Failed to retrieve activity stream" in caplog.text
