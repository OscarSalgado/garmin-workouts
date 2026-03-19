from intervalsicu.intervals.extraction import Extraction


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


def test_format_hr_step(tmp_path, monkeypatch):
    # monkeypatch account fmin/rfmax values used by _format_hr_step
    import account
    monkeypatch.setattr(account, 'fmin', 40)
    monkeypatch.setattr(account, 'rfmax', 200)

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
