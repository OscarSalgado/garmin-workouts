# Tasks

## 1. Surface typed login failures

- [x] 1.1 Add `except` clauses in `GarminApi.login()` that re-raise the three typed exceptions, and log the generic
  fallback at warning level.
  Verify: `pytest tests/platform/test_garminapi.py` passes.
- [x] 1.2 Add one test per typed exception asserting it propagates, and one asserting a generic `Exception`
  still returns `False` and logs a warning.
  Verify: the four new tests pass and `test_expired_token_login_failure_is_handled` still passes unchanged.

## 2. Callers

- [x] 2.1 Add a test that the rate-limit exception reaches `_garmin_client()` and produces `SystemExit(1)`.
  Verify: the test passes without network access.
- [x] 2.2 Run `tests/platform/test_garminclient.py` and the full suite.
  Verify: `pytest -q` passes and `strength.py` and `types.py` are unchanged.
