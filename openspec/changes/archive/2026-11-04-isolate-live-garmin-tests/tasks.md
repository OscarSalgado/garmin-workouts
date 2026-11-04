# Tasks

## 1. Live tests are opt-in

- [x] 1.1 Add `[tool.pytest.ini_options]` with `markers = ["live: talks to the real Garmin account"]` and
  `addopts = "-m 'not live'"`. Verify: `pytest --markers` lists `live`.
- [x] 1.2 Mark `WorkoutTestCase.test_workout` (and any test using `platform_workout_files`) as `live`.
  Verify: `pytest -q` reports 0 failures; `pytest -m live --collect-only -q` lists the moved tests.
- [x] 1.3 Add an offline test that runs `settings()` and `create_workout()` for the same plan files and validates
  the payload shape. Verify: it passes with networking blocked.

## 2. No secrets, no sockets

- [x] 2.1 Replace `account.get_credentials()` in fixtures with constants and set dummy athlete values in
  `conftest.py` (`monkeypatch.setenv`). Verify: `env -u GARMIN_USERNAME -u GARMIN_PASSWORD pytest -q` passes with
  no `.env` present.
- [x] 2.2 Block outbound sockets in the default run (autouse fixture or `pytest-socket --disable-socket`, allowing
  localhost for `pytest-httpserver`). Verify: a deliberately added `requests.get("https://example.com")` test fails
  with a socket-blocked error.
- [x] 2.3 Remove `account.get_garmin_client()` calls from decorators in `tests/test_garmin_auth.py`.
  Verify: `pytest --collect-only -q tests/test_garmin_auth.py` makes no network call.

## 3. Honest coverage

- [x] 3.1 Limit `[tool.coverage.report] omit` to generated modules (`models/strength.py`, generated strength
  generators) and set `fail_under` to the measured total. Verify: `pytest --cov` passes and prints the new total.
