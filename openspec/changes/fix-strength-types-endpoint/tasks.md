# Tasks

## 1. Endpoint

- [x] 1.1 In `garminworkouts/garmin/garmintypes.py` point `get_strength_types` at `https://connect.garmin.com/web-data/exercises/Exercises.json`. Verify: `grep` shows the new URL and no `/web-data/exercises/Exercises.json` relative path remains.
- [x] 1.2 Update `test_get_strength_types` in `tests/platform/test_platform_types.py` to the same URL. Verify: `pytest tests/platform/test_platform_types.py -k strength` passes.

- [x] 1.3 Update `test_get_yoga_types` in `tests/platform/test_platform_types.py` to `https://connect.garmin.com/web-data/exercises/Yoga.json`. Verify: `pytest tests/platform/test_platform_types.py -k yoga` passes.

## 2. Verification

- [x] 2.1 Run the unit tests for the garmin types module. Verify: `pytest tests -q` shows no new failures.
- [x] 2.2 Confirm the endpoint live with a read-only GET (no write to `strength.py`). Verify: HTTP 200 and 47 categories.
