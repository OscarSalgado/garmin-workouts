"""Fallback branches of generator_struct when the (generated) strength module is missing or misbehaves."""
import logging
import sys
from unittest.mock import MagicMock

import pytest

import garminworkouts.config.generators as generators_pkg
from garminworkouts.config.includeloader import generator_struct


@pytest.fixture
def fake_strength(monkeypatch):
    fake = MagicMock()
    monkeypatch.setattr(generators_pkg, "strength", fake, raising=False)
    monkeypatch.setitem(sys.modules, "garminworkouts.config.generators.strength", fake)
    return fake


def test_import_failure_falls_back(monkeypatch) -> None:
    monkeypatch.delattr(generators_pkg, "strength", raising=False)
    monkeypatch.setitem(sys.modules, "garminworkouts.config.generators.strength", None)
    # Without the strength module the strength-backed table cannot be built, but the import failure is handled
    with pytest.raises(AttributeError):
        generator_struct("n", "10min", 0, "R0")


def test_unknown_strength_exercise_returns_empty(fake_strength, caplog) -> None:
    class MultiStep:
        def __getattr__(self, name):
            if name == "something_new_generator":
                raise AttributeError(name)
            return MagicMock()

    fake_strength.multi_step = MultiStep()
    with caplog.at_level(logging.WARNING):
        assert generator_struct("n", "10", 0, "SomethingNew") == {}
    assert "Unknown strength exercise" in caplog.text


def test_strength_attribute_error(fake_strength, caplog) -> None:
    fake_strength.multi_step.something_new_generator.side_effect = AttributeError("bad attr")
    with caplog.at_level(logging.WARNING):
        assert generator_struct("n", "10", 0, "SomethingNew") == {}
    assert "AttributeError for strength exercise" in caplog.text


def test_strength_unexpected_error(fake_strength, caplog) -> None:
    fake_strength.multi_step.something_new_generator.side_effect = ValueError("bad value")
    with caplog.at_level(logging.WARNING):
        assert generator_struct("n", "10", 0, "SomethingNew") == {}
    assert "Unexpected error for strength exercise" in caplog.text


def test_strength_found_dynamically(fake_strength) -> None:
    fake_strength.multi_step.something_new_generator.return_value = {"ok": 1}
    assert generator_struct("n", "10", 0, "SomethingNew") == {"ok": 1}


def test_falsy_strength_returns_empty(fake_strength) -> None:
    fake_strength.__bool__.return_value = False
    assert generator_struct("n", "10", 0, "SomethingNew") == {}
