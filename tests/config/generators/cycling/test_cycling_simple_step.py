import pytest
from garminworkouts.config.generators.cycling.simple_step import (
    P0_step_generator, P1_step_generator, P1p_step_generator, P2_step_generator,
    P3_step_generator, P3p_step_generator, P4_step_generator, P5_step_generator,
    P6_step_generator, P7_step_generator, Hcyclingoutdoor_step_generator, H0c_step_generator
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
    (P0_step_generator, 10, expected_result("interval", 10, "P0", "P0 power zone", secondary="H0")),
    (P1_step_generator, 20, expected_result("interval", 20, "P1", "P1 power zone", secondary="H1")),
    (P1p_step_generator, 30, expected_result("interval", 30, "P1p", "P1+ power zone", secondary="H1p")),
    (P2_step_generator, 40, expected_result("interval", 40, "P2", "P2 power zone", secondary="H2")),
    (P3_step_generator, 50, expected_result("interval", 50, "P3", "P3 power zone", secondary="H3")),
    (P3p_step_generator, 60, expected_result("interval", 60, "P3p", "P3+ power zone")),
    (P4_step_generator, 70, expected_result("interval", 70, "P4", "P4 power zone")),
    (P5_step_generator, 80, expected_result("interval", 80, "P5", "P5 power zone")),
    (P6_step_generator, 90, expected_result("interval", 90, "P6", "P6 power zone")),
    (P7_step_generator, 100, expected_result("interval", 100, "P7", "P7 power zone")),
    (Hcyclingoutdoor_step_generator, 110, expected_result("interval", 110, "Hcyclingoutdoor", "Cycling outdoor heart rate zone", secondary="BikeCadence")),
    (H0c_step_generator, 120, expected_result("interval", 120, "H0c", "R0 heart rate zone")),
])
def test_cycling_step_generators(generator, duration, expected):
    """Test cycling step generators with various durations."""
    result = generator(duration)
    assert result == expected, f"Failed for generator: {generator.__name__}"


def test_p0_step_generator_structure():
    """Test P0 step generator returns correct structure."""
    result = P0_step_generator("100w")
    assert result["type"] == "interval"
    assert result["duration"] == "100w"
    assert result["target"] == "P0"
    assert result["secondary"] == "H0"
    assert result["description"] == "P0 power zone"


def test_p1p_step_generator_structure():
    """Test P1+ step generator returns correct structure."""
    result = P1p_step_generator("200w")
    assert result["type"] == "interval"
    assert result["duration"] == "200w"
    assert result["target"] == "P1p"
    assert result["secondary"] == "H1p"
    assert result["description"] == "P1+ power zone"


def test_p4_step_generator_no_secondary():
    """Test P4 step generator has no secondary target."""
    result = P4_step_generator("300w")
    assert result["type"] == "interval"
    assert result["duration"] == "300w"
    assert result["target"] == "P4"
    assert "secondary" not in result
    assert result["description"] == "P4 power zone"


def test_p7_step_generator_structure():
    """Test P7 step generator returns correct structure."""
    result = P7_step_generator("400w")
    assert result["type"] == "interval"
    assert result["duration"] == "400w"
    assert result["target"] == "P7"
    assert "secondary" not in result
    assert result["description"] == "P7 power zone"


def test_hcyclingoutdoor_step_generator_structure():
    """Test Hcyclingoutdoor step generator returns correct structure."""
    result = Hcyclingoutdoor_step_generator("5min")
    assert result["type"] == "interval"
    assert result["duration"] == "5min"
    assert result["target"] == "Hcyclingoutdoor"
    assert result["secondary"] == "BikeCadence"
    assert result["description"] == "Cycling outdoor heart rate zone"


def test_h0c_step_generator_structure():
    """Test H0c step generator returns correct structure."""
    result = H0c_step_generator("6min")
    assert result["type"] == "interval"
    assert result["duration"] == "6min"
    assert result["target"] == "H0c"
    assert "secondary" not in result
    assert result["description"] == "R0 heart rate zone"
