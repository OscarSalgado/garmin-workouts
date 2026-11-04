"""Sport-dependent and fallback branches of Workout that the YAML-driven tests do not reach."""
import os
from unittest.mock import patch

import pytest

from garminworkouts.config import configreader
from garminworkouts.models.pace import Pace
from garminworkouts.models.power import Power
from garminworkouts.models.workout import Workout


def _bare(sport_type: str) -> Workout:
    """A Workout with only the attributes the helpers under test read."""
    w = object.__new__(Workout)
    w.sport_type = sport_type
    w.rfmax, w.cfmax, w.sfmax = 190, 170, 160
    w.rflt, w.cflt, w.sflt = 175, 155, 145
    w.fmin = 50
    w.rFTP, w.cFTP = Power("300w"), Power("200w")
    w.vVO2 = Pace("5:00")
    return w


def _config() -> dict:
    return configreader.read_config(os.path.join(".", "workouts", "cardio_training", "ADVANCED", "BBtO4iZ.yaml"))


@pytest.mark.parametrize("account_patch", [
    {"side_effect": RuntimeError("no account")},
    {"return_value": {"fmin": "abc"}},
])
def test_fmin_falls_back_to_60(account_patch) -> None:
    with patch("account.get_athlete_config", **account_patch):
        w = Workout(config=_config(), target=[])
    assert w.fmin == 60


@pytest.mark.parametrize("step_type, index", [
    ("interval", 0), ("recovery", 1), ("rest", 2), ("warmup", 3), ("cooldown", 4), ("other", 5),
])
def test_update_durations_adds_to_matching_bucket(step_type, index) -> None:
    result = _bare("running").update_durations({"type": step_type}, 30, 1, 2, 3, 4, 5, 6)
    base = [1, 2, 3, 4, 5, 6]
    base[index] += 30
    assert result == tuple(base)


def test_update_durations_run_bucket_is_separate() -> None:
    assert _bare("running").update_durations({"type": "run"}, 30, 1, 2, 3, 4, 5, 6) == (1, 2, 3, 4, 5, 6)


def test_update_durations_defaults_to_other() -> None:
    assert _bare("running").update_durations({}, 10, 0, 0, 0, 0, 0, 0) == (0, 0, 0, 0, 0, 10)


def test_load_metrics_is_a_noop() -> None:
    assert Workout.load_metrics("any/path") is None


@pytest.mark.parametrize("sport, expected", [("running", 300.0 * 0.5), ("cycling", 200.0 * 0.5), ("swimming", 0.5)])
def test_power_zone_value_per_sport(sport, expected) -> None:
    assert _bare(sport)._get_power_zone_value("power.zone", "0.5") == pytest.approx(expected)


@pytest.mark.parametrize("sport, expected", [
    ("running", 190), ("cycling", 170), ("swimming", 160), ("cardio", 190),
])
def test_get_fmax_per_sport(sport, expected) -> None:
    assert _bare(sport).get_fmax() == expected


@pytest.mark.parametrize("sport, expected", [
    ("running", 175), ("cycling", 155), ("swimming", 145), ("cardio", 175),
])
def test_get_flt_per_sport(sport, expected) -> None:
    assert _bare(sport).get_flt() == expected


def test_convert_hr_to_target_hr_zero_denominator() -> None:
    w = _bare("running")
    w.fmin = w.rfmax
    assert w.convert_HR_to_targetHR(150) == 0.0


def test_convert_hr_to_target_hr_normal() -> None:
    w = _bare("running")
    assert w.convert_HR_to_targetHR(120) == pytest.approx((120 - 50) / (190 - 50))
