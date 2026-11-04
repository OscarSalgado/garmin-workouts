# Proposal

## Why

The default `pytest` run (`4785 passed, 2 failed` in 144 s locally) is not fully offline:

- `tests/trainingplans/base_test.py::platform_workout_files` (used by
  `tests/platform/test_platform_workout.py::WorkoutTestCase::test_workout`) builds a real `GarminClient` and
  **creates, updates, schedules, downloads and deletes workouts on the real Garmin account**. Without a live session
  it fails with `GarminConnectAuthenticationError: Not authenticated` (the 2 current failures); with one, every test
  run mutates the athlete's account.
- Test fixtures call `account.get_credentials()`, so the suite fails at fixture setup when `GARMIN_USERNAME` /
  `GARMIN_PASSWORD` are not in the environment, which is why CI injects real secrets into all five matrix jobs.
- `tests/test_garmin_auth.py` calls `account.get_garmin_client()` inside `@patch.object(...)` decorators, i.e. at
  collection time; in an interactive terminal that triggers a real login attempt.
- Coverage hides the riskiest code: `[tool.coverage.report] omit` excludes `garminworkouts/garmin/*`,
  `__main__.py`, `models/workout.py`, `config/includeloader.py`, `intervalsicu/intervals/api.py`, among others.
  The reported coverage is not representative.

## What Changes

- Register a `live` pytest marker; move `platform_workout_files` and any other real-account test behind it, skipped
  by default and run only with `pytest -m live` plus credentials.
- Add an offline variant of `test_workout` that builds payloads for the same plan files and validates them without
  network calls.
- Fixtures use fixed dummy credentials instead of `account.get_credentials()`; a `conftest.py` guard blocks real
  sockets (`pytest-socket` or a `socket.socket` monkeypatch) in the default run.
- Remove collection-time client creation from `tests/test_garmin_auth.py`.
- Shrink the coverage `omit` list to generated files only and set a `fail_under` at the current measured value.

## Capabilities

### New Capabilities
- `test-suite`: what the default test run may touch and how live tests are opted into.

### Modified Capabilities

## Impact

- Files: `tests/trainingplans/base_test.py`, `tests/platform/test_platform_workout.py`, `tests/conftest.py`,
  `tests/test_garmin_auth.py`, `pyproject.toml` (`[tool.pytest.ini_options]` markers, coverage config).
- Unblocks `fix-ci-pipeline-gating` removing secrets from CI.
- Overlaps `unify-garmin-auth-config` on `tests/test_garmin_auth.py`; land that change first or rebase.
