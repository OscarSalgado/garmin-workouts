import pytest
from garminworkouts.config.generators.strength.simple_step import exercise_generator, rest_generator
from garminworkouts.config.generators.running.simple_step import (
    H0_step_generator, H1_step_generator, H1p_step_generator, H2_step_generator,
    R0_step_generator, R1_step_generator, R1p_step_generator, R2_step_generator,
    R3_step_generator, R3p_step_generator,
    H3_step_generator, H3p_step_generator,
    R4_step_generator, R5_step_generator,
    R6_step_generator, recovery_step_generator, aerobic_step_generator,
    lt_step_generator, lr_step_generator, marathon_step_generator,
    hm_step_generator, tuneup_step_generator, warmup_step_generator,
    cooldown_step_generator, walk_step_generator
)

# Constants for expected values to avoid repetition
NO_TARGET = {"category": None, "exerciseName": None}


# Helper function to generate expected results
def expected_result(step_type, duration, target, description, **kwargs):
    return {
        "type": step_type,
        "duration": duration,
        "target": target,
        "description": description,
        **NO_TARGET,
        **kwargs
    }


@pytest.mark.parametrize("generator, duration, expected", [
    (R0_step_generator, 10, expected_result("interval", 10, "R0", "R0 pace zone", secondary="H0")),
    (R1_step_generator, 20, expected_result("interval", 20, "R1", "R1 pace zone", secondary="H1")),
    (R1p_step_generator, 30, expected_result("interval", 30, "R1p", "R1+ pace zone", secondary="H1p")),
    (H0_step_generator, 10, expected_result("interval", 10, "H0", "R0 heart rate zone")),
    (H1_step_generator, 20, expected_result("interval", 20, "H1", "R1 heart rate zone")),
    (H1p_step_generator, 30, expected_result("interval", 30, "H1p", "R1+ heart rate zone")),
    (H2_step_generator, 20, expected_result("interval", 20, "H2", "R2 heart rate zone")),
    (H3_step_generator, 20, expected_result("interval", 20, "H3", "R3 heart rate zone")),
    (R3p_step_generator, 60, expected_result("interval", 60, "R3p", "R3+ pace zone")),
    (H3p_step_generator, 20, expected_result("interval", 20, "H3p", "R3+ heart rate zone")),
    (R4_step_generator, 70, expected_result("interval", 70, "R4", "R4 pace zone")),
    (R5_step_generator, 80, expected_result("interval", 80, "R5", "R5 pace zone")),
    (R6_step_generator, 90, expected_result("interval", 90, "R6", "R6 pace zone")),
    (walk_step_generator, 190, expected_result("rest", 190, "WALK", "Walk")),
    (tuneup_step_generator, 160, expected_result("interval", 160, "10KM_PACE", "10K pace run")),
    (warmup_step_generator, 170, expected_result("warmup", 170, "AEROBIC_HEART_RATE", "Warm up")),
])
def test_single_use_generators(generator, duration, expected):
    """Test single-use step generators with fixed durations."""
    result = generator(duration)
    assert result == expected, f"Failed for generator: {generator.__name__}"


@pytest.mark.parametrize("generator, duration, pace, expected", [
    (recovery_step_generator, 100, False, expected_result("recovery", 100, "RECOVERY_HEART_RATE", "Recovery pace")),
    (aerobic_step_generator, 110, False, expected_result("interval", 110, "AEROBIC_HEART_RATE", "Aerobic pace")),
    (cooldown_step_generator, 180, False, expected_result("cooldown", 180, "AEROBIC_HEART_RATE", "Cool down")),
    (recovery_step_generator, 100, True, expected_result("recovery", 100, "RECOVERY_PACE", "Recovery pace")),
    (aerobic_step_generator, 110, True, expected_result("interval", 110, "AEROBIC_PACE", "Aerobic pace")),
    (cooldown_step_generator, 180, True, expected_result("cooldown", 180, "AEROBIC_PACE", "Cool down")),
    (lr_step_generator, 240, False, expected_result("interval", 240, "LONG_RUN_HEART_RATE", "Long run pace")),
    (lr_step_generator, 250, True, expected_result("interval", 250, "LONG_RUN_PACE", "Long run pace")),
])
def test_pace_generators(generator, duration, pace, expected):
    """Test pace-based step generators with optional pace flag."""
    result = generator(duration, pace)
    assert result == expected, f"Failed for generator: {generator.__name__} with pace={pace}"


@pytest.mark.parametrize("generator, duration, target, expected", [
    (marathon_step_generator, 200, "", expected_result("interval", 200, "MARATHON_PACE", "Marathon pace")),
    (hm_step_generator, 210, "", expected_result("interval", 210, "HALF_MARATHON_PACE", "Half Marathon pace")),
    (R2_step_generator, 40, "", expected_result("interval", 40, "R2", "R2 pace zone")),
    (R3_step_generator, 50, "", expected_result("interval", 50, "R3", "R3 pace zone")),
])
def test_target_duration_generators(generator, duration, target, expected):
    """Test generators that accept target and duration."""
    result = generator(duration, target)
    assert result == expected, f"Failed for generator: {generator.__name__} with target={target}"


@pytest.mark.parametrize("generator, duration, target, pace, expected", [
    (lt_step_generator, 220, "", False, expected_result("interval", 220, "THRESHOLD_HEART_RATE", "Threshold pace")),
    (lt_step_generator, 230, "", True, expected_result("interval", 230, "THRESHOLD_PACE", "Threshold pace")),
])
def test_lt_generators(generator, duration, target, pace, expected):
    """Test LT step generators with optional pace flag."""
    result = generator(duration, target, pace)
    assert result == expected, f"Failed for generator: {generator.__name__} with pace={pace}"


@pytest.mark.parametrize("category, exercise_name, duration, execution, expected", [
    ("PUSH_UP", "PUSH_UP", "10", "reps",
     expected_result("interval", "10reps", "NO_TARGET", "Push Up", category="PUSH_UP", exerciseName="PUSH_UP")),
    ("SQUAT", "SQUAT", "20", "hold",
     expected_result("interval", "lap.button", "NO_TARGET", "20-count hold", category="SQUAT", exerciseName="SQUAT")),
    ("PLANK", "PLANK", "30", "",
     expected_result("interval", "lap.button", "NO_TARGET", "Max Planks", category="PLANK", exerciseName="PLANK")),
])
def test_exercise_generator(category, exercise_name, duration, execution, expected):
    """Test exercise generator with various categories and executions."""
    result = exercise_generator(category, exercise_name, duration, execution)
    assert result == expected, f"Failed for category: {category}, exercise_name: {exercise_name}"


def test_exercise_generator_invalid_category():
    """Test exercise generator with an invalid category."""
    with pytest.raises(KeyError):
        exercise_generator("invalid_category", "push_up", "10", "reps")


def test_exercise_generator_invalid_exercise():
    """Test exercise generator with an invalid exercise name."""
    with pytest.raises(ValueError):
        exercise_generator("CORE", "invalid_exercise", "10", "reps")


@pytest.mark.parametrize("duration, expected", [
    ("10s", expected_result("rest", "10s", "NO_TARGET", "")),
    ("20s", expected_result("rest", "20s", "NO_TARGET", "")),
])
def test_rest_generator(duration, expected):
    """Test rest generator with various durations."""
    result = rest_generator(duration)
    assert result == expected, f"Failed for duration: {duration}"
