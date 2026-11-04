"""IntervalsClient orchestration with a stubbed Intervals.icu API and fake workouts."""
import logging
import sys
from datetime import date, timedelta
from unittest import mock

import numpy as np
import pandas as pd
import pytest

for _name in ("sklearn", "sklearn.linear_model"):
    try:
        __import__(_name)
    except ImportError:
        sys.modules[_name] = mock.MagicMock()

from intervalsicu.intervals import client as client_module  # noqa: E402
from intervalsicu.intervals.client import IntervalsClient  # noqa: E402


class FakeWorkout:
    def __init__(self, day, name="w"):
        self.day = day
        self.name = name

    def get_workout_date(self):
        return self.day, 0, 0

    def get_workout_name(self):
        return self.name


@pytest.fixture
def api() -> IntervalsClient:
    return IntervalsClient("ath", "key")


def test_update_workouts_delegates(api) -> None:
    with mock.patch.object(api, "list_plans", return_value={"p": 1}), \
            mock.patch.object(api, "get_plan_folder", return_value={"id": 1}) as folder, \
            mock.patch.object(api, "update_events_") as events:
        api.update_workouts([FakeWorkout(date(2026, 3, 10))], "p")
    folder.assert_called_once()
    events.assert_called_once_with(mock.ANY, {"id": 1})


def test_get_plan_folder_new_plan(api) -> None:
    workouts = [FakeWorkout(date(2026, 3, 11)), FakeWorkout(date(2026, 3, 9))]
    with mock.patch.object(api, "get_wellness", return_value={"ctl": 5, "atl": 6}), \
            mock.patch.object(api, "create_plan", return_value={"id": 9}) as create:
        assert api.get_plan_folder(workouts, "new", {}) == {"id": 9}
    assert create.call_args.kwargs == {"plan_name": "new", "d": date(2026, 3, 9), "ctl": 5, "atl": 6}


def test_get_plan_folder_existing_with_children_is_reused(api) -> None:
    existing = {"p": {"id": 1, "children": [{"id": 2}]}}
    assert api.get_plan_folder([FakeWorkout(date(2026, 3, 9))], "p", existing) == existing["p"]


def test_get_plan_folder_empty_plan_is_recreated_from_monday(api) -> None:
    existing = {"p": {"id": 1}}
    with mock.patch.object(api, "delete_plan") as delete, \
            mock.patch.object(api, "get_wellness", return_value={}), \
            mock.patch.object(api, "create_plan", return_value={"id": 2}) as create:
        assert api.get_plan_folder([FakeWorkout(date(2026, 3, 12))], "p", existing) == {"id": 2}
    delete.assert_called_once_with(1)
    assert create.call_args.kwargs["d"] == date(2026, 3, 9)
    assert create.call_args.kwargs["ctl"] == -1


@pytest.mark.parametrize("payload", [[{"name": "x"}], []])
def test_update_events(api, caplog, payload) -> None:
    future = date.today() + timedelta(days=3)
    workouts = [FakeWorkout(future), FakeWorkout(future + timedelta(days=30))]
    with mock.patch.object(api, "delete_range_events") as delete, \
            mock.patch.object(api, "set_targets") as targets, \
            mock.patch.object(api, "format_training_data", return_value=payload), \
            mock.patch.object(api, "upload_events") as upload, caplog.at_level(logging.WARNING):
        api.update_events_(workouts, {"name": "Plan"})
    delete.assert_called_once()
    targets.assert_called_once()
    if payload:
        upload.assert_called_once_with(payload)
    else:
        upload.assert_not_called()
        assert "No events to upload for plan 'Plan'" in caplog.text


def test_update_training_plan_delegates(api) -> None:
    with mock.patch.object(api, "list_plans", return_value={}), \
            mock.patch.object(api, "get_plan_folder", return_value={"id": 1}), \
            mock.patch.object(api, "sync_plan_folder") as sync:
        api.update_training_plan([], "p")
    sync.assert_called_once_with([], {"id": 1})


def test_sync_plan_folder_uploads_new_and_deletes_stale(api) -> None:
    folder = {"start_date_local": "2026-03-01T00:00:00",
              "children": [{"name": "keep", "id": 1}, {"name": "stale", "id": 2}]}
    workouts = [FakeWorkout(date(2026, 3, 5), "keep"), FakeWorkout(date(2026, 3, 8), "new")]
    with mock.patch.object(api, "format_training_data", return_value=[{"n": 1}]) as fmt, \
            mock.patch.object(api, "upload_workouts") as upload, \
            mock.patch.object(api, "delete_workout") as delete:
        api.sync_plan_folder(workouts, folder)
    assert fmt.call_args.kwargs["day_a"] == date(2026, 3, 1)
    assert fmt.call_args.kwargs["day_b"] == date(2026, 3, 8)
    upload.assert_called_once_with([{"n": 1}])
    delete.assert_called_once_with(2)


def test_sync_plan_folder_nothing_to_change(api) -> None:
    with mock.patch.object(api, "upload_workouts") as upload, mock.patch.object(api, "delete_workout") as delete:
        api.sync_plan_folder([], {})
    upload.assert_not_called()
    delete.assert_not_called()


def test_export_workouts(api, tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    folders = [
        {"type": "FOLDER", "name": "F", "children": [{"name": 'a.b:c'}, {"name": "d"}]},
        {"type": "PLAN", "name": "P", "children": [{"name": "ignored"}]},
    ]
    with mock.patch.object(api, "list_folders", return_value=folders), \
            mock.patch.object(api, "export_workout") as export:
        api.export_workouts()
    assert [c.args[1] for c in export.call_args_list] == ["./workouts/F/a_b_c.yaml", "./workouts/F/d.yaml"]


def test_export_workout_uses_extraction(api) -> None:
    with mock.patch.object(client_module.Extraction, "workout_export_yaml") as export:
        api.export_workout({"w": 1}, "f.yaml")
    export.assert_called_once_with({"w": 1}, "f.yaml")


class _Reg:
    """Stands in for LinearRegression: predict returns fixed [LT1, LT2] values."""

    def __init__(self, lt1, lt2) -> None:
        self.values = iter([lt1, lt2])

    def fit(self, x, y):
        return self

    def predict(self, x):
        return np.array([[next(self.values)]])


def _features(alpha=(0.9, 0.5), hr=(120, 160)) -> pd.DataFrame:
    return pd.DataFrame({"alpha1": list(alpha), "heartrate": list(hr)})


@pytest.mark.parametrize("lt1, lt2, features, rr_len, expected", [
    (140, 150, _features(), 1001, ["LT1", "LT2"]),     # both thresholds below max HR
    (140, 170, _features(), 1001, ["LT1"]),            # LT2 above the max HR
    (170, 180, _features(), 1001, []),                 # LT1 above the max HR
    (140, 150, _features(hr=(60, 80)), 1001, []),      # max HR too low
    (140, 150, _features(alpha=(), hr=()), 1001, []),  # no features
    (140, 150, _features(), 10, []),                   # too few RR intervals
])
def test_compute_aerobic_threshold(api, capsys, lt1, lt2, features, rr_len, expected) -> None:
    activities = [{"type": "Ride", "id": "a1", "start_date_local": "2026-01-01"},
                  {"type": "Run", "id": "a2"},
                  {"type": "Swim", "id": "a3"}]
    with mock.patch.object(api, "get_activities", return_value=activities), \
            mock.patch.object(api, "get_activity_stream", return_value=[]), \
            mock.patch.object(client_module.IntervalsThreshold, "read_RR_intervals", return_value=[1] * rr_len), \
            mock.patch.object(client_module.IntervalsThreshold, "remove_artifacts", return_value=pd.DataFrame()), \
            mock.patch.object(client_module.IntervalsThreshold, "computeFeatures", return_value=features), \
            mock.patch.object(client_module, "LinearRegression", side_effect=lambda: _Reg(lt1, lt2)):
        api.compute_aerobic_threshold()
    out = capsys.readouterr().out
    assert out.count("LT1 (alpha1=0.75)") == (2 if "LT1" in expected else 0)
    assert out.count("LT2 (alpha1=0.5)") == (2 if "LT2" in expected else 0)


def test_compute_aerobic_threshold_warns_for_other_sports(api, caplog) -> None:
    with mock.patch.object(api, "get_activities", return_value=[{"type": "Swim"}]), \
            caplog.at_level(logging.WARNING):
        api.compute_aerobic_threshold()
    assert "No valid HRV data found for type : Swim" in caplog.text
