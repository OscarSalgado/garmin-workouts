import pytest
from garminworkouts.config.generators.cycling.multi_step import Pseries_generator


def test_pseries_generator_increasing_zones():
    """Test Pseries generator with increasing power zones."""
    duration = ["5min", "10min"]
    objective = [("P1", "1"), ("P2", "2")]
    result = Pseries_generator(duration, objective)
    
    assert len(result) == 2
    assert result[0]["type"] == "recovery"
    assert result[0]["duration"] == "5min"
    assert result[0]["target"] == ("P1", "1")
    assert result[0]["description"] == "('P1', '1') power zone"
    assert result[1]["type"] == "interval"
    assert result[1]["duration"] == "10min"
    assert result[1]["target"] == ("P2", "2")
    assert result[1]["description"] == "('P2', '2') power zone"


def test_pseries_generator_decreasing_zones():
    """Test Pseries generator with decreasing power zones."""
    duration = ["5min", "10min"]
    objective = [("P3", "3"), ("P1", "1")]
    result = Pseries_generator(duration, objective)
    
    assert len(result) == 2
    assert result[0]["type"] == "interval"
    assert result[0]["duration"] == "5min"
    assert result[1]["type"] == "recovery"
    assert result[1]["duration"] == "10min"


def test_pseries_generator_same_zones():
    """Test Pseries generator with same power zones."""
    duration = ["5min", "10min"]
    objective = [("P2", "2"), ("P2", "2")]
    result = Pseries_generator(duration, objective)
    
    assert len(result) == 2
    # When zones are equal (not <), first is 'interval', second is 'recovery'
    assert result[0]["type"] == "interval"
    assert result[1]["type"] == "recovery"


def test_pseries_generator_string_duration():
    """Test Pseries generator with string durations."""
    duration = ["100w", "200w"]
    objective = [("P1", "1"), ("P3", "3")]
    result = Pseries_generator(duration, objective)
    
    assert len(result) == 2
    assert result[0]["duration"] == "100w"
    assert result[1]["duration"] == "200w"
