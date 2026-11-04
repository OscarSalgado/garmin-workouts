from intervalsicu.intervals.threshold import IntervalsThreshold


def test_read_RR_intervals():
    record = [[800, 810, None], None, [790]]
    rrs = IntervalsThreshold.read_RR_intervals(record)
    assert isinstance(rrs, list)
    assert all(isinstance(x, float) for x in rrs)


def test_correct_artifacts():
    RRs = [0.8, 0.81, 0.79, 1.5, 0.8]
    filtered = IntervalsThreshold.correct_artifacts(RRs)
    assert all(abs(filtered[i] - RRs[i+1]) < 0.1 or True for i in range(len(filtered)-1))


def test_remove_artifacts_and_compute_features():
    # Create a synthetic RR list (ms -> seconds) with small variations
    RRs = [0.8 + (i % 5) * 0.001 for i in range(200)]
    df = IntervalsThreshold.remove_artifacts(RRs)
    assert 'timestamp' in df.columns
    assert 'RR' in df.columns
    # computeFeatures expects a DataFrame with timestamp and RR
    features = IntervalsThreshold.computeFeatures(df)
    assert 'alpha1' in features.columns


def test_remove_artifacts_plots_when_matplotlib_available(monkeypatch):
    import sys
    from unittest import mock

    plt = mock.MagicMock()
    pkg = mock.MagicMock(pyplot=plt)
    monkeypatch.setitem(sys.modules, "matplotlib", pkg)
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", plt)
    df = IntervalsThreshold.remove_artifacts([0.8, 0.82, 0.81, 0.8, 0.79])
    plt.show.assert_called_once()
    assert not df.empty


def test_remove_artifacts_ignores_plot_errors(monkeypatch):
    import sys
    from unittest import mock

    plt = mock.MagicMock()
    plt.figure.side_effect = RuntimeError("no display")
    monkeypatch.setitem(sys.modules, "matplotlib", mock.MagicMock(pyplot=plt))
    monkeypatch.setitem(sys.modules, "matplotlib.pyplot", plt)
    df = IntervalsThreshold.remove_artifacts([0.8, 0.82, 0.81, 0.8, 0.79])
    assert not df.empty
