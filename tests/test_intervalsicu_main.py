"""intervalsicu CLI entry points, with the client and settings stubbed."""
import argparse
from unittest import mock

import pytest

import importlib
import sys

# scikit-learn is an optional debug extra imported by the Intervals client; stub it when absent.
for _name in ("sklearn", "sklearn.linear_model"):
    try:
        importlib.import_module(_name)
    except ImportError:
        sys.modules[_name] = mock.MagicMock()

from intervalsicu import __main__ as cli  # noqa: E402


@pytest.fixture
def client():
    with mock.patch.object(cli, "_intervals_client") as factory:
        yield factory.return_value.__enter__.return_value


def test_trainingplan_import(client) -> None:
    with mock.patch.object(cli, "settings", return_value=(["w"], [], None, "plan")):
        cli.command_trainingplan_import(argparse.Namespace())
    client.update_workouts.assert_called_once_with(workouts=["w"], plan="plan")


def test_trainingplan_update(client) -> None:
    with mock.patch.object(cli, "settings", return_value=(["w"], [], None, "plan")):
        cli.command_trainingplan_update(argparse.Namespace())
    client.update_training_plan.assert_called_once_with(workouts=["w"], plan="plan")


def test_thresholds_detect(client) -> None:
    cli.command_thresholds_detect(argparse.Namespace())
    client.compute_aerobic_threshold.assert_called_once()


def test_workout_creator() -> None:
    with mock.patch.object(cli.WorkoutCreator, "MesoCreator") as creator:
        cli.command_workout_creator(argparse.Namespace(mesocycle_index="2"))
    creator.assert_called_once_with("2")


def test_intervals_client_built_from_config() -> None:
    cfg = {"api_key": "k", "athlete_id": "i1"}
    with mock.patch.object(cli.account, "get_intervals_config", return_value=cfg), \
            mock.patch.object(cli, "IntervalsClient") as cls:
        assert cli._intervals_client() is cls.return_value
    cls.assert_called_once_with(api_key="k", athlete_id="i1")


@pytest.mark.parametrize("cfg, message", [
    ({"athlete_id": "i1"}, "API key"),
    ({"api_key": "k"}, "athlete ID"),
])
def test_intervals_client_missing_config(cfg, message) -> None:
    with mock.patch.object(cli.account, "get_intervals_config", return_value=cfg), \
            pytest.raises(ValueError, match=message):
        cli._intervals_client()

