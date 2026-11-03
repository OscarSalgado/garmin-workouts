import pytest
from garminworkouts.config.generators.swimming.simple_step import (
    S0_step_generator, S1_step_generator, S1p_step_generator, S2_step_generator,
    S3_step_generator, S3p_step_generator, S4_step_generator, S5_step_generator,
    S6_step_generator, S7_step_generator
)


# Helper function to generate expected results
def expected_result(step_type, duration, target, description, secondary=None):
    result = {
        "type": step_type,
        "duration": duration,
        "target": target,
        "description": description,
        "category": None,
        "exerciseName": None
    }
    if secondary is not None:
        result["secondary"] = secondary
    return result


@pytest.mark.parametrize("generator, duration, expected", [
    (S0_step_generator, 10, expected_result("interval", 10, "S0", "S0 pace zone", secondary="H0")),
    (S1_step_generator, 20, expected_result("interval", 20, "S1", "S1 pace zone", secondary="H1")),
    (S1p_step_generator, 30, expected_result("interval", 30, "S1p", "S1+ pace zone", secondary="H1p")),
    (S2_step_generator, 40, expected_result("interval", 40, "S2", "S2 pace zone", secondary="H2")),
    (S3_step_generator, 50, expected_result("interval", 50, "S3", "S3 pace zone", secondary="H3")),
    (S3p_step_generator, 60, expected_result("interval", 60, "S3p", "S3+ pace zone")),
    (S4_step_generator, 70, expected_result("interval", 70, "S4", "S4 pace zone")),
    (S5_step_generator, 80, expected_result("interval", 80, "S5", "S5 pace zone")),
    (S6_step_generator, 90, expected_result("interval", 90, "S6", "S6 pace zone")),
    (S7_step_generator, 100, expected_result("interval", 100, "S7", "S7 pace zone")),
])
def test_swimming_step_generators(generator, duration, expected):
    """Test swimming step generators with various durations."""
    result = generator(duration)
    assert result == expected, f"Failed for generator: {generator.__name__}"


def test_s0_step_generator_structure():
    """Test S0 step generator returns correct structure."""
    result = S0_step_generator("100m")
    assert result["type"] == "interval"
    assert result["duration"] == "100m"
    assert result["target"] == "S0"
    assert result["secondary"] == "H0"
    assert result["description"] == "S0 pace zone"


def test_s1p_step_generator_structure():
    """Test S1+ step generator returns correct structure."""
    result = S1p_step_generator("200m")
    assert result["type"] == "interval"
    assert result["duration"] == "200m"
    assert result["target"] == "S1p"
    assert result["secondary"] == "H1p"
    assert result["description"] == "S1+ pace zone"


def test_s4_step_generator_no_secondary():
    """Test S4 step generator has no secondary target."""
    result = S4_step_generator("300m")
    assert result["type"] == "interval"
    assert result["duration"] == "300m"
    assert result["target"] == "S4"
    assert "secondary" not in result
    assert result["description"] == "S4 pace zone"


def test_s7_step_generator_structure():
    """Test S7 step generator returns correct structure."""
    result = S7_step_generator("400m")
    assert result["type"] == "interval"
    assert result["duration"] == "400m"
    assert result["target"] == "S7"
    assert "secondary" not in result
    assert result["description"] == "S7 pace zone"
