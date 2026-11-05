"""Offline tests for the thin REST wrappers in GarminWorkout and GarminNote."""
from unittest.mock import MagicMock, patch

import pytest

from garminworkouts.garmin.garminclient import GarminClient

WORKOUT = "/workout-service"
NOTE = "/calendar-service"
PLAN = GarminClient._TRAINING_PLAN_SERVICE_ENDPOINT


def _resp(payload=None) -> MagicMock:
    response = MagicMock()
    response.json.return_value = payload if payload is not None else {}
    return response


# ---- workouts ----------------------------------------------------------------------------------------------

def test_get_workout(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "get", return_value=_resp()) as get:
        authed_gclient.get_workout(5)
    get.assert_called_once_with(f"{WORKOUT}/workout/5")


def test_save_workout(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "post", return_value=_resp({"workoutId": 1})) as post:
        assert authed_gclient.save_workout({"a": 1}) == {"workoutId": 1}
    post.assert_called_once_with(f"{WORKOUT}/workout", json={"a": 1})


def test_update_and_delete_workout(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "put") as put, patch.object(authed_gclient, "delete") as delete:
        authed_gclient.update_workout(5, {"a": 1})
        authed_gclient.delete_workout(5)
    put.assert_called_once_with(f"{WORKOUT}/workout/5", json={"a": 1})
    delete.assert_called_once_with(f"{WORKOUT}/workout/5")


def test_schedule_and_remove_workout(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "post", return_value=_resp({"ok": 1})) as post, \
            patch.object(authed_gclient, "delete") as delete:
        assert authed_gclient.schedule_workout(5, "2026-01-01") == {"ok": 1}
        authed_gclient.remove_workout(5, "2026-01-01")
    post.assert_called_once_with(f"{WORKOUT}/schedule/5", json={"date": "2026-01-01"})
    delete.assert_called_once_with(f"{WORKOUT}/schedule/5", json={"date": "2026-01-01"})


def test_download_workout_yaml(authed_gclient: GarminClient) -> None:
    data = {"workoutId": 5}
    with patch.object(authed_gclient, "get_workout", return_value=_resp(data)), \
            patch("garminworkouts.garmin.garminworkout.Extraction.workout_export_yaml") as export:
        assert authed_gclient.download_workout_yaml(5, "f.yaml") == data
    export.assert_called_once_with(data, "f.yaml")


def test_download_workout_writes_file(authed_gclient: GarminClient, tmp_path) -> None:
    target = tmp_path / "w.fit"
    with patch.object(authed_gclient, "download", return_value=b"FIT") as download:
        assert authed_gclient.download_workout(5, str(target)) == b"FIT"
    download.assert_called_once_with(f"{WORKOUT}/workout/FIT/5")
    assert target.read_bytes() == b"FIT"


def test_workout_export(authed_gclient: GarminClient, tmp_path) -> None:
    args = MagicMock(directory=str(tmp_path))
    workouts = [{"workoutId": 1, "workoutName": "A"}, {"workoutId": 2, "workoutName": "B"}]
    with patch.object(authed_gclient, "list_workouts", return_value=iter(workouts)), \
            patch.object(authed_gclient, "download_workout") as download:
        authed_gclient.workout_export(args)
    assert download.call_count == 2
    assert download.call_args_list[0].args[1].endswith("1.fit")


def test_fetch_workouts(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "get", return_value=_resp([])) as get:
        authed_gclient._fetch_workouts("/u", {"start": 0})
    get.assert_called_once_with("/u", params={"start": 0})


def test_list_workouts_paginates(authed_gclient: GarminClient) -> None:
    pages = iter([[{"workoutId": 1}, {"workoutId": 2}], [{"workoutId": 3}], []])
    with patch.object(authed_gclient, "_fetch_workouts", side_effect=lambda u, p: _resp(next(pages))) as fetch:
        result = list(authed_gclient.list_workouts(batch_size=2))
    assert [w["workoutId"] for w in result] == [1, 2, 3]
    assert [c.args[1]["start"] for c in fetch.call_args_list] == [0, 2, 4]


def test_workout_list_prints_summary(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "list_workouts", return_value=iter([{"a": 1}, {"a": 2}])), \
            patch("garminworkouts.garmin.garminworkout.Workout.print_workout_summary") as summary:
        authed_gclient.workout_list()
    assert summary.call_count == 2


def test_external_workout_endpoints(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "get", side_effect=[_resp({"workouts": [{"x": 1}]}), _resp({"w": 1})]) as get:
        assert authed_gclient.external_workouts("en-US") == [{"x": 1}]
        assert authed_gclient.get_external_workout("C1", "en-US") == {"w": 1}
    assert get.call_args_list[0].args[0] == "web-data/workouts/en-US/index.json"
    assert get.call_args_list[1].args[0] == "web-data/workouts/en-US/C1.json"


def test_workout_export_yaml_creates_directories(authed_gclient: GarminClient, tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    listing = [{"workoutSourceId": "C1", "sportTypeKey": "running", "difficulty": "Beginner"}]
    detail = {"workoutName": "Easy"}
    with patch.object(authed_gclient, "external_workouts", return_value=listing), \
            patch.object(authed_gclient, "get_external_workout", return_value=detail), \
            patch("garminworkouts.garmin.garminworkout.Extraction.workout_export_yaml") as export:
        authed_gclient.workout_export_yaml()
        # second pass: directory now exists
        authed_gclient.workout_export_yaml()
    assert (tmp_path / "workouts" / "running" / "Beginner").is_dir()
    assert export.call_count == 2


@pytest.mark.parametrize("ww, expected", [
    ("plain", "R1_1.yaml"),
    ("a- warm", "R1_1a.yaml"),
    ("a - warm", "R1_1a.yaml"),
    ("b- cool", "R1_1b.yaml"),
    ("b - cool", "R1_1b.yaml"),
    ("a- b-", "R1_1ab.yaml"),
])
def test_generate_filename(authed_gclient: GarminClient, ww, expected) -> None:
    assert authed_gclient.generate_filename("dir", "R1_1", ww).endswith(expected)


def test_external_workout_export_yaml_runs_both(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "workout_export_yaml") as a, \
            patch.object(authed_gclient, "export_trainingplans") as b:
        authed_gclient.external_workout_export_yaml()
    a.assert_called_once()
    b.assert_called_once()


def _plan(subtype: str, name: str) -> dict:
    return {
        "trainingPlanId": "123", "trainingType": {"typeKey": "running"},
        "trainingSubType": {"subTypeKey": subtype}, "trainingLevel": {"levelKey": "beginner"},
        "trainingVersion": {"versionName": "Time"}, "name": name,
        "description": "d", "durationInWeeks": 12, "avgWeeklyWorkouts": 3,
    }


@pytest.mark.parametrize("subtype, name, expected_dir", [
    # sub-type equals the plan name -> no extra folder
    ("Marathon", "Marathon", "Marathon"),
    # RunningOther takes the name as sub-type
    ("RunningOther", "My Plan", "MyPlan"),
    # otherwise the plan name is a trailing folder
    ("Marathon", "Fast Plan", "FastPlan"),
])
def test_export_trainingplans_paths(authed_gclient: GarminClient, tmp_path, monkeypatch, subtype, name,
                                    expected_dir) -> None:
    monkeypatch.chdir(tmp_path)
    plan = _plan(subtype, name)
    tasks = [
        {"weekId": "1", "dayOfWeekId": "1", "taskWorkout": {"workoutId": "9"}},
        {"weekId": "1", "dayOfWeekId": "2", "taskNote": {"note": "a- n", "noteDescription": "txt"}},
        {"weekId": "1", "dayOfWeekId": "3"},
    ]
    with patch.object(authed_gclient, "list_trainingplans", return_value=[plan]), \
            patch.object(authed_gclient, "schedule_training_plan", return_value=plan), \
            patch.object(authed_gclient, "get_training_plan", return_value=tasks), \
            patch.object(authed_gclient, "get_workout", return_value=_resp({"workoutName": "w"})), \
            patch.object(authed_gclient, "delete_training_plan") as delete, \
            patch("garminworkouts.garmin.garminworkout.Extraction.workout_export_yaml") as wexp, \
            patch("garminworkouts.garmin.garminworkout.Extraction.note_export_yaml") as nexp:
        authed_gclient.export_trainingplans()
    wexp.assert_called_once()
    nexp.assert_called_once()
    delete.assert_called_once_with("123")
    assert expected_dir in wexp.call_args.kwargs["filename"].replace("\\", "/")


# ---- notes -------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("plan, base", [(True, f"{PLAN}/scheduled/notes/7"), (False, f"{NOTE}/note/7")])
def test_get_and_update_note(authed_gclient: GarminClient, plan, base) -> None:
    with patch.object(authed_gclient, "get") as get, patch.object(authed_gclient, "put") as put:
        authed_gclient.get_note(plan, 7)
        authed_gclient.update_note(plan, 7, {"n": 1})
    get.assert_called_once_with(base)
    put.assert_called_once_with(base, json={"n": 1})


def test_save_and_delete_note(authed_gclient: GarminClient) -> None:
    with patch.object(authed_gclient, "post", return_value=_resp({"id": 1})) as post, \
            patch.object(authed_gclient, "delete") as delete:
        assert authed_gclient.save_note({"n": 1}) == {"id": 1}
        authed_gclient.delete_note(7)
    post.assert_called_once_with(f"{NOTE}/note", json={"n": 1})
    delete.assert_called_once_with(f"{NOTE}/note/7")


def test_download_note_yaml(authed_gclient: GarminClient) -> None:
    data = {"noteId": 7}
    with patch.object(authed_gclient, "get_note", return_value=_resp(data)) as get_note, \
            patch("garminworkouts.garmin.garminnote.Extraction.note_export_yaml") as export:
        assert authed_gclient.download_note_yaml(False, 7, "n.yaml") == data
    get_note.assert_called_once_with(False, 7)
    export.assert_called_once_with(data, "n.yaml")
