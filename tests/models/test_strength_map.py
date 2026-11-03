import pytest
import os
import tempfile
from garminworkouts.models.strength_map import generate_functions, write_functions_to_file, write_test_functions_to_file, MAP


class TestGenerateFunctions:
    """Test generate_functions utility."""

    def test_generate_functions_creates_correct_count(self):
        """Test that generate_functions creates 1 code block per exercise (each containing rep+hold)."""
        exercises = {"EXERCISE_1": {}, "EXERCISE_2": {}}
        functions = generate_functions("TEST", exercises)
        # Each exercise generates 1 code block containing both rep and hold generators
        assert len(functions) == 2  # 2 exercises = 2 code blocks

    def test_generate_functions_rep_generator(self):
        """Test rep generator function generation."""
        exercises = {"BENCH_PRESS": {}}
        functions = generate_functions("STRENGTH", exercises)
        # Each code block contains both rep and hold generators
        assert "bench_press_rep_generator" in functions[0]
        assert "execution='reps'" in functions[0]

    def test_generate_functions_hold_generator(self):
        """Test hold generator function generation."""
        exercises = {"SQUAT": {}}
        functions = generate_functions("STRENGTH", exercises)
        # Same code block contains both generators
        assert "squat_hold_generator" in functions[0]
        assert "execution='hold'" in functions[0]

    def test_generate_functions_category_included(self):
        """Test that category is included in generated functions."""
        exercises = {"PLANK": {}}
        functions = generate_functions("CORE", exercises)
        assert "category='CORE'" in functions[0]


class TestWriteFunctionsToFile:
    """Test write_functions_to_file utility."""

    def test_write_functions_creates_directory(self):
        """Test that write_functions_to_file creates directory if needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "subdir", "test_output.py")
            functions = ["def test(): pass\n"]
            write_functions_to_file(functions, output_path)
            assert os.path.exists(output_path)

    def test_write_functions_writes_content(self):
        """Test that write_functions_to_file writes correct content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_output.py")
            functions = ["def test_func(): pass\n"]
            write_functions_to_file(functions, output_path)
            
            with open(output_path, 'r') as f:
                content = f.read()
            
            assert "def test_func(): pass" in content

    def test_write_functions_writes_import(self):
        """Test that write_functions_to_file includes import statement."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_output.py")
            functions = ["def test(): pass\n"]
            write_functions_to_file(functions, output_path)
            
            with open(output_path, 'r') as f:
                content = f.read()
            
            assert "from garminworkouts.config.generators.strength.simple_step import exercise_generator" in content


class TestWriteTestFunctionsToFile:
    """Test write_test_functions_to_file utility."""

    def test_write_test_functions_creates_directory(self):
        """Test that write_test_functions_to_file creates directory if needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exercises = {"EXERCISE_1": {}}
            output_path = os.path.join(tmpdir, "subdir", "test_output.py")
            write_test_functions_to_file("STRENGTH", exercises, output_path)
            assert os.path.exists(output_path)

    def test_write_test_functions_writes_imports(self):
        """Test that write_test_functions_to_file includes correct imports."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exercises = {"BENCH_PRESS": {}}
            output_path = os.path.join(tmpdir, "test_output.py")
            write_test_functions_to_file("STRENGTH", exercises, output_path)
            
            with open(output_path, 'r') as f:
                content = f.read()
            
            assert "import pytest" in content
            assert "from garminworkouts.config.generators.strength.strength import" in content

    def test_write_test_functions_writes_parametrize(self):
        """Test that write_test_functions_to_file includes parametrize decorator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exercises = {"SQUAT": {}}
            output_path = os.path.join(tmpdir, "test_output.py")
            write_test_functions_to_file("STRENGTH", exercises, output_path)
            
            with open(output_path, 'r') as f:
                content = f.read()
            
            assert "@pytest.mark.parametrize" in content
            assert "squat_rep_generator" in content
            assert "squat_hold_generator" in content


class TestMAP:
    """Test MAP dictionary contains all expected keys."""

    def test_map_contains_all_categories(self):
        """Test that MAP contains all strength categories."""
        expected_keys = [
            'BANDED_EXERCISES', 'BATTLE_ROPE', 'BENCH_PRESS', 'BIKE_OUTDOOR',
            'CALF_RAISE', 'CARDIO', 'CARRY', 'CHOP', 'CORE', 'CRUNCH',
            'CURL', 'DEADLIFT', 'ELLIPTICAL', 'FLOOR_CLIMB', 'FLYE',
            'HIP_RAISE', 'HIP_STABILITY', 'HIP_SWING', 'HYPEREXTENSION',
            'INDOOR_BIKE', 'LADDER', 'LATERAL_RAISE', 'LEG_CURL', 'LEG_RAISE',
            'LUNGE', 'OLYMPIC_LIFT', 'PLANK', 'PLYO', 'PULL_UP', 'PUSH_UP',
            'ROW', 'RUN', 'RUN_INDOOR', 'SANDBAG', 'SHOULDER_PRESS',
            'SHOULDER_STABILITY', 'SHRUG', 'SIT_UP', 'SLED', 'SLEDGE_HAMMER',
            'SQUAT', 'STAIR_STEPPER', 'SUSPENSION', 'TIRE', 'TOTAL_BODY',
            'TRICEPS_EXTENSION', 'WARM_UP'
        ]
        for key in expected_keys:
            assert key in MAP, f"Missing key: {key}"

    def test_map_values_are_dicts(self):
        """Test that all MAP values are dictionaries."""
        for key, value in MAP.items():
            assert isinstance(value, dict), f"Value for {key} is not a dict"
