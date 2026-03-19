import base64
import requests

from intervalsicu.intervals.api import IntervalsAPI


def test_format_sport_strings():
    class W:
        def __init__(self, sport):
            self.config = {"sport": sport}

    assert IntervalsAPI.format_sport(W("cycling")) == "Ride"
    assert IntervalsAPI.format_sport(W("run")) == "Run"
    assert IntervalsAPI.format_sport(W("swim")) == "Swim"
    assert IntervalsAPI.format_sport(W("walk")) == "Walk"
    assert IntervalsAPI.format_sport(W("strength")) == "WeightTraining"
    assert IntervalsAPI.format_sport(W("something else")) == "Other"


def test_format_duration_string():
    assert IntervalsAPI.format_duration_string(1, 2, 3) == "1h2m3s"
    assert IntervalsAPI.format_duration_string(0, 5, 0) == "5m"
    assert IntervalsAPI.format_duration_string(0, 0, 30) == "30s"
    assert IntervalsAPI.format_duration_string(2, 0, 0) == "2h"


def test_convert_duration():
    assert IntervalsAPI.convert_duration("5km") == 5000.0
    assert IntervalsAPI.convert_duration("10m") == 600
    assert IntervalsAPI.convert_duration("30s") == 30
    assert IntervalsAPI.convert_duration("42") == 42
    assert IntervalsAPI.convert_duration("invalid") == 0


def test_encode_auth_and_headers():
    api = IntervalsAPI("ath1", "secret")
    token = api.encode_auth("secret")
    assert isinstance(token, str)
    decoded = base64.b64decode(token.encode()).decode()
    assert decoded == "API_KEY:secret"
    assert "Authorization" in api.headers


def test_http_wrappers_monkeypatch(monkeypatch):
    api = IntervalsAPI("ath1", "key")

    class Resp:
        def __init__(self, code=200, data=None):
            self.status_code = code
            self._data = data or {}

        def json(self):
            return self._data

    called = {}

    def fake_get(*args, **kwargs):
        called['get'] = (args, kwargs)
        return Resp(200, {"ok": True})

    monkeypatch.setattr(requests, 'get', fake_get)
    r = api.get('http://example.com')
    assert r.json() == {"ok": True}
    assert 'headers' in called['get'][1]
