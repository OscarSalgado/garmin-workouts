from intervalsicu.intervals.extraction import Extraction
import pytest


@pytest.fixture
def mock_athlete_config(monkeypatch):
    """Fixture to mock account.get_athlete_config with default values."""
    import account
    monkeypatch.setattr(account, 'get_athlete_config', lambda: {
        'fmin': 40,
        'rfmax': 200,
        'cfmax': 175,
        'sfmax': 180,
        'vV02': 50,
        'rFTP': 250,
        'cFTP': 200,
        'rflt': 1.0,
        'cflt': 1.0,
        'sflt': 1.0,
        'bot_token': 'test_bot_token'
    })
    return account


def test_description_formatting_none():
    assert Extraction.description_formatting(None) == ""


def test_description_formatting_replacements():
    s = "Do this. Try that. Workout. push-ups.Benchmark"
    out = Extraction.description_formatting(s)
    assert "\nTry" in out
    assert "Workout" in out


def test_format_sport_mapping():
    assert Extraction.format_sport('Run') == 'running'
    assert Extraction.format_sport('Ride') == 'cycling'
    assert Extraction.format_sport('Swim') == 'swimming'
    assert Extraction.format_sport('Walk') == 'walking'
    assert Extraction.format_sport('Strength Training') == 'strength_training'
    assert Extraction.format_sport('Unknown') == ''


def test_format_power_step():
    step = {'duration': 60, 'power': {'value': 250}}
    out = Extraction._format_power_step(step)
    assert out['type'] == 'interval'
    assert 'target' in out and out['target']['type'] == 'power.zone'


def test_format_hr_step(mock_athlete_config):
    step = {'duration': 30, 'hr': {'value': 150}}
    out = Extraction._format_hr_step(step, 'Run')
    assert out['target']['type'] == 'heart.rate.zone'


def test_format_reps_step():
    step = {'reps': 2, 'steps': [{'duration': 10}, {'duration': 20}]}
    out = Extraction._format_reps_step(step, 'Run')
    assert isinstance(out, list)
    assert len(out) == 4


def test_format_maxeffort_step():
    step = {'duration': 45}
    out = Extraction._format_maxeffort_step(step)
    assert out['description'] == 'Maximum effort'


def test_format_default_step():
    step = {'duration': 15}
    out = Extraction._format_default_step(step)
    assert out['target'] is None


def test_format_power_step_zero_value():
    """Test power step with value == 0 (lines 101-103)."""
    step = {'duration': 60, 'power': {'value': 0}}
    out = Extraction._format_power_step(step)
    assert out['target']['min'] == 0
    assert out['target']['max'] == 0.05


def test_format_power_step_start_end():
    """Test power step with start/end values (lines 108-121)."""
    step = {'duration': 60, 'power': {'start': 200, 'end': 250}}
    out = Extraction._format_power_step(step)
    assert out['target']['min'] == 2.0
    assert out['target']['max'] == 2.5
    assert out['description'] == '200%FTP'


def test_format_power_step_start_end_swapped():
    """Test power step with start > end (swapping logic)."""
    step = {'duration': 60, 'power': {'start': 300, 'end': 200}}
    out = Extraction._format_power_step(step)
    assert out['target']['min'] == 2.0
    assert out['target']['max'] == 3.0


def test_format_power_step_unknown():
    """Test power step with no value or start/end (lines 118-121)."""
    step = {'duration': 60, 'power': {}}
    out = Extraction._format_power_step(step)
    assert out['target']['min'] == 0
    assert out['target']['max'] == 1
    assert out['description'] == 'Unknown Power Zone'


def test_format_hr_step_ride_sport(mock_athlete_config):
    """Test HR step with 'Ride' sport (line 136)."""
    step = {'duration': 30, 'hr': {'value': 140}}
    out = Extraction._format_hr_step(step, 'Ride')
    assert out['target']['type'] == 'heart.rate.zone'


def test_format_hr_step_other_sport(mock_athlete_config):
    """Test HR step with other sport (line 138)."""
    step = {'duration': 30, 'hr': {'value': 140}}
    out = Extraction._format_hr_step(step, 'Swim')
    assert out['target']['type'] == 'heart.rate.zone'


def test_format_hr_step_start_end(mock_athlete_config):
    """Test HR step with start/end values (lines 147-160)."""
    step = {'duration': 30, 'hr': {'start': 140, 'end': 160}}
    out = Extraction._format_hr_step(step, 'Run')
    assert out['description'] == '140 - 160%HR'


def test_format_hr_step_start_end_swapped(mock_athlete_config):
    """Test HR step with start > end (swapping logic)."""
    step = {'duration': 30, 'hr': {'start': 160, 'end': 140}}
    out = Extraction._format_hr_step(step, 'Run')
    assert '140 - 160%HR' in out['description'] or '160 - 140%HR' in out['description']


def test_format_hr_step_unknown(mock_athlete_config):
    """Test HR step with no value or start/end (lines 157-160)."""
    step = {'duration': 30, 'hr': {}}
    out = Extraction._format_hr_step(step, 'Run')
    assert out['target']['min'] == 0
    assert out['target']['max'] == 1
    assert out['description'] == 'Unknown Power Zone'


def test_workout_export_yaml(tmp_path, mock_athlete_config):
    """Test workout_export_yaml function (lines 34-62)."""
    workout = {
        'name': 'Test Workout',
        'type': 'Run',
        'workout_doc': {
            'description': 'Test description',
            'steps': [
                {'duration': 60, 'power': {'value': 250}},
                {'duration': 30, 'hr': {'value': 150}},
            ]
        },
        'icu_training_load': 50
    }
    
    filename = tmp_path / 'test_workout.json'
    Extraction.workout_export_yaml(workout, str(filename))
    
    output_file = tmp_path / 'test_workout.yaml'
    assert output_file.exists()
    
    import yaml
    with open(output_file) as f:
        data = yaml.safe_load(f)
    
    assert data['name'] == 'Test Workout'
    assert data['sport'] == 'running'
    assert len(data['steps']) == 2


def test_format_step_dispatch(mock_athlete_config):
    """Test format_step dispatches to correct helper (lines 81-90)."""
    # Power step
    step = {'duration': 60, 'power': {'value': 250}}
    out = Extraction.format_step(step, 'Run')
    assert out['target']['type'] == 'power.zone'
    
    # HR step
    step = {'duration': 30, 'hr': {'value': 150}}
    out = Extraction.format_step(step, 'Run')
    assert out['target']['type'] == 'heart.rate.zone'
    
    # Max effort step
    step = {'duration': 45, 'maxeffort': True}
    out = Extraction.format_step(step, 'Run')
    assert out['description'] == 'Maximum effort'
    
    # Default step
    step = {'duration': 15}
    out = Extraction.format_step(step, 'Run')
    assert out['target'] is None
    
    # Reps step (line 86)
    step = {'reps': 2, 'steps': [{'duration': 10}]}
    out = Extraction.format_step(step, 'Run')
    assert isinstance(out, list)
    assert len(out) == 2


def test_workout_export_yaml_with_reps(tmp_path, mock_athlete_config):
    """Test workout_export_yaml with reps steps (lines 56-59)."""
    workout = {
        'name': 'Test Workout with Reps',
        'type': 'Run',
        'workout_doc': {
            'description': 'Test description',
            'steps': [
                {'reps': 3, 'steps': [{'duration': 30, 'power': {'value': 250}}]},
            ]
        },
        'icu_training_load': 50
    }
    
    filename = tmp_path / 'test_reps_workout.json'
    Extraction.workout_export_yaml(workout, str(filename))
    
    output_file = tmp_path / 'test_reps_workout.yaml'
    assert output_file.exists()
    
    import yaml
    with open(output_file) as f:
        data = yaml.safe_load(f)
    
    assert data['name'] == 'Test Workout with Reps'
    # Should have 3 reps * 1 step = 3 steps expanded
    assert len(data['steps']) == 3
