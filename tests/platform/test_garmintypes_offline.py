"""Offline tests for GarminTypes: every payload is faked and every file write lands in a tmp dir."""
import logging
import os
from unittest.mock import MagicMock, patch

import pytest

from garminworkouts.garmin.garminclient import GarminClient

TYPES_FILE = "".join(
    f"{name}: dict[str, int] = {{\n    'old{i}': {i},\n}}\n"
    for i, name in enumerate(["STEP_TYPES", "TARGET_TYPES", "SWIMINSTRUCTION_TYPES", "ACTIVITY_TYPES",
                              "GOLF_CLUB", "GOLF_FLEX"])
)


@pytest.fixture
def types_file(tmp_path):
    path = tmp_path / "types.py"
    path.write_text(TYPES_FILE)
    return str(path)


def test_process_workout_types_step(authed_gclient: GarminClient, types_file) -> None:
    resp = {"workoutStepTypes": [{"stepTypeKey": "warmup", "stepTypeId": 1}]}
    authed_gclient.process_workout_types(types_file, resp, "step")
    assert "'warmup': 1," in open(types_file).read()


def test_process_workout_types_target_and_swim_keys(authed_gclient: GarminClient, types_file) -> None:
    authed_gclient.process_workout_types(
        types_file, {"workoutTargetTypes": [{"workoutTargetTypeKey": "pace", "workoutTargetTypeId": 6}]}, "target")
    authed_gclient.process_workout_types(
        types_file, {"workoutSwimInstructionTypes": [{"instructionTypeKey": "kick", "instructionTypeId": 2}]},
        "swimInstruction")
    content = open(types_file).read()
    assert "'pace': 6," in content
    assert "'kick': 2," in content


def test_process_activity_types(authed_gclient: GarminClient, types_file) -> None:
    authed_gclient.process_activity_types(types_file, [{"typeKey": "running", "typeId": 1}], "activity")
    assert "'running': 1," in open(types_file).read()


def test_process_golf_types_club_and_flex(authed_gclient: GarminClient, types_file) -> None:
    authed_gclient.process_golf_types(types_file, [{"name": "Driver", "value": 7}], "club")
    authed_gclient.process_golf_types(types_file, [{"name": "Stiff", "id": 3}], "flex")
    content = open(types_file).read()
    assert "'Driver': 7," in content
    assert "'Stiff': 3," in content


def test_get_golf_types(authed_gclient: GarminClient, types_file) -> None:
    responses = [[{"name": "Iron", "value": 5}], [{"name": "Soft", "id": 1}]]
    fake = MagicMock()
    fake.json.side_effect = responses
    with patch.object(authed_gclient, "get", return_value=fake) as mock_get:
        authed_gclient.get_golf_types(types_file)
    assert mock_get.call_count == 2
    content = open(types_file).read()
    assert "'Iron': 5," in content and "'Soft': 1," in content


def test_get_activity_and_event_types(authed_gclient: GarminClient, types_file) -> None:
    fake = MagicMock()
    fake.json.return_value = [{"typeKey": "x", "typeId": 9}]
    with patch.object(authed_gclient, "get", return_value=fake), \
            patch.object(authed_gclient, "process_activity_types") as proc:
        authed_gclient.get_activity_types(types_file)
        authed_gclient.get_event_types(types_file)
    assert proc.call_count == 2


def test_get_strength_types_fetch_failure(authed_gclient: GarminClient, caplog) -> None:
    with patch.object(authed_gclient, "get", side_effect=RuntimeError("boom")), caplog.at_level(logging.WARNING):
        authed_gclient.get_strength_types()
    assert "Could not fetch strength types" in caplog.text


def test_get_strength_types_empty_payload(authed_gclient: GarminClient, caplog) -> None:
    fake = MagicMock()
    fake.json.return_value = {"categories": {}}
    with patch.object(authed_gclient, "get", return_value=fake), caplog.at_level(logging.WARNING):
        authed_gclient.get_strength_types()
    assert "Empty strength types payload" in caplog.text


def test_get_strength_types_writes_files_in_cwd(authed_gclient: GarminClient, tmp_path, monkeypatch) -> None:
    models = tmp_path / "garminworkouts" / "models"
    models.mkdir(parents=True)
    (models / "strength.py").write_text("")
    monkeypatch.chdir(tmp_path)

    long_muscles = [f"MUSCLE_NUMBER_{i}" for i in range(12)]
    payload = {"categories": {
        "BENCH_PRESS": {"exercises": {
            "SHORT": {"primaryMuscles": ["CHEST"], "secondaryMuscles": ["TRICEPS"]},
            "LONG": {"primaryMuscles": long_muscles, "secondaryMuscles": long_muscles},
        }},
        "CURL": {"exercises": {"BAR": {"primaryMuscles": ["BICEPS"], "secondaryMuscles": []}}},
        "EMPTY": {},
    }}
    fake = MagicMock()
    fake.json.return_value = payload
    with patch.object(authed_gclient, "get", return_value=fake):
        authed_gclient.get_strength_types()

    # Rewritten catalogue is valid Python containing every exercise
    namespace: dict = {}
    exec(compile((tmp_path / "strength.py").read_text(), "strength.py", "exec"), namespace)  # noqa: S102
    assert set(namespace["BENCH_PRESS"]) == {"SHORT", "LONG"}
    assert namespace["BENCH_PRESS"]["LONG"]["primaryMuscles"] == long_muscles
    assert namespace["EMPTY"] == {}
    # Generators and tests are regenerated under the (tmp) cwd only
    assert os.path.isdir(tmp_path / "garminworkouts" / "config" / "generators" / "strength")
    assert os.path.isdir(tmp_path / "tests" / "config" / "generators" / "strength")


def test_update_garmin_rewrites_version(authed_gclient: GarminClient, tmp_path, monkeypatch) -> None:
    api_dir = tmp_path / "garminworkouts" / "garmin"
    api_dir.mkdir(parents=True)
    (api_dir / "garminapi.py").write_text('_GARMIN_VERSION = "1.0.0.0"\n')
    monkeypatch.chdir(tmp_path)
    authed_gclient.version = "2.0.0.0"
    with patch.object(authed_gclient, "get_types") as get_types:
        authed_gclient.updateGarmin()
    get_types.assert_called_once()
