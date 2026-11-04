# Tasks

## 1. Bounded login in `_garmin_client`

- [x] 1.1 Replace the `while True` loop with a bounded loop (max 3 attempts) and add the backoff sleep.
  Verify: `pytest tests/test___main__.py` passes and no `while True` remains in `_garmin_client`.
- [x] 1.2 Exit with status 1 after a single failed attempt when `EMAIL` and `PASSWORD` come from the environment.
  Verify: new test asserts one `login` call and `SystemExit(1)`.
- [x] 1.3 Add tests for exhausted interactive attempts, success on retry, and `KeyboardInterrupt`, with
  `GarminClient`, `input`, `getpass` and `time.sleep` patched.
  Verify: `pytest tests/test___main__.py` passes in under 2 s and makes no network calls.

## 2. Regression check

- [x] 2.1 Run the full suite.
  Verify: `pytest -q` passes and `garminworkouts/models/strength.py` and `types.py` are unchanged.
