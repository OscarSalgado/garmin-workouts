"""Intervals.icu workout export to YAML."""
import pytest
import yaml
from unittest import mock

from intervalsicu.intervals import extraction as extraction_module
from intervalsicu.intervals.extraction import Extraction

ATHLETE = {"fmin": 45, "rfmax": 185, "cfmax": 166}


@pytest.mark.parametrize("text, expected", [
    (None, ""),
    ("One. Two", "One.\nTwo"),
    ("Dr. Who. Next", "Dr. Who. Next"),
    ("Go. Complete it", "Go. Complete it"),
    ("rest20s", "rest\n 20s"),
    ("Importado con EstraperTools:\nestraperlista.com/estrapertools\n\nHola", "Hola"),
])
def test_description_formatting(text, expected) -> None:
    assert Extraction.description_formatting(text) == expected


@pytest.mark.parametrize("sport, expected", [
    ("Run", "running"), ("Ride", "cycling"), ("Swim", "swimming"), ("Walk", "walking"),
    ("Strength Training", "strength_training"), ("Other", ""),
])
def test_format_sport(sport, expected) -> None:
    assert Extraction.format_sport(sport) == expected


def test_power_steps() -> None:
    fmt = Extraction.format_step
    value = fmt({"duration": 60, "power": {"value": 80}}, "Ride")
    assert value["target"] == {"type": "power.zone", "min": 0.75, "max": 0.85}
    zero = fmt({"duration": 60, "power": {"value": 0}}, "Ride")
    assert zero["target"]["max"] == 0.05
    ramp = fmt({"duration": 60, "power": {"start": 90, "end": 50}}, "Ride")
    assert ramp["target"]["min"] == 0.5 and ramp["target"]["max"] == 0.9
    ordered = fmt({"duration": 60, "power": {"start": 50, "end": 90}}, "Ride")
    assert ordered["target"]["min"] == 0.5
    unknown = fmt({"duration": 60, "power": {}}, "Ride")
    assert unknown["description"] == "Unknown Power Zone"


@pytest.mark.parametrize("sport", ["Run", "Ride", "Swim"])
def test_hr_steps(sport) -> None:
    with mock.patch.object(extraction_module.account, "get_athlete_config", return_value=ATHLETE):
        value = Extraction.format_step({"duration": 60, "hr": {"value": 70}}, sport)
        ramp = Extraction.format_step({"duration": 60, "hr": {"start": 80, "end": 60}}, sport)
        ordered = Extraction.format_step({"duration": 60, "hr": {"start": 60, "end": 80}}, sport)
        unknown = Extraction.format_step({"duration": 60, "hr": {}}, sport)
    assert value["description"] == "70%HR" and value["target"]["type"] == "heart.rate.zone"
    assert ramp["target"]["min"] == 0.6 and ramp["target"]["max"] == 0.8
    assert ordered["description"] == "60 - 80%HR"
    assert unknown["target"]["max"] == 1


def test_reps_maxeffort_and_default_steps() -> None:
    reps = Extraction.format_step(
        {"reps": 2, "steps": [{"duration": 30}, {"duration": 60, "maxeffort": True}]}, "Ride")
    assert len(reps) == 4
    assert reps[0]["target"] is None and reps[0]["duration"] == "0:00:30"
    assert reps[1]["description"] == "Maximum effort"


def test_workout_export_yaml(tmp_path) -> None:
    workout = {
        "name": "W", "type": "Ride", "sub_type": "RACE", "icu_training_load": 50,
        "workout_doc": {"description": "Easy. Go", "steps": [
            {"duration": 60, "power": {"value": 60}},
            {"reps": 2, "steps": [{"duration": 30, "power": {"value": 100}}]},
        ]},
    }
    out = tmp_path / "w.json"
    Extraction.workout_export_yaml(workout, str(out))
    data = yaml.safe_load((tmp_path / "w.yaml").read_text())
    assert data["name"] == "W" and data["sport"] == "cycling" and data["subsport"] == "RACE"
    assert data["description"] == "Easy.\nGo" and data["load"] == 50
    assert len(data["steps"]) == 3 and isinstance(data["steps"][1], list)


def test_workout_export_yaml_without_doc_writes_nothing(tmp_path) -> None:
    out = tmp_path / "w.yaml"
    Extraction.workout_export_yaml({"name": "W", "type": "Run"}, str(out))
    assert not out.exists()
