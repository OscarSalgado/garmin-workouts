## 1. Investigate `garminconnect` API surface
- [x] 1.1 Confirm the installed `garminconnect==0.3.3` `Garmin` class constructor signature (email, password, is_cn, prompt_mfa) and `.login()`/MFA resume behavior against actual package source
- [x] 1.2 Confirm token persistence API (e.g. `garth`-backed `dump`/`load` exposed via `Garmin.garth`, or a dedicated tokenstore method) and default token directory

## 2. Rewrite `GarminApi` authentication
- [x] 2.1 Remove `_CompatClient`, `_MinimalClient`, and the `garth` import/fallback shim from `garminworkouts/garmin/garminapi.py`
- [x] 2.2 Update `GarminApi.__init__`/`GarminApi.login` to construct and use `garminconnect.Garmin` directly, dropping `domain`/`pool_connections`/`pool_maxsize`/CN-domain concepts
- [x] 2.3 Wire up token load/dump using `garminconnect`'s persistence mechanism, preserving the `./garminconnect` tokenstore path convention and the load-then-fallback-to-credential-login behavior
- [x] 2.4 Preserve `get_mfa()` prompt-based MFA and wire it into the `garminconnect.Garmin` login flow
- [x] 2.5 Update `get`/`put`/`post`/`delete`/`download` methods to delegate to the `garminconnect.Garmin` client's request methods instead of the `garth`-shaped interface
- [x] 2.6 Preserve `display_name`, `full_name`, `unit_system`, `version` population logic using data from the `garminconnect.Garmin` client

## 3. Update dependencies
- [x] 3.1 Remove `garth==0.7.10` from `pyproject.toml` (replaced with `garminconnect==0.3.3`, matching `requirements.txt`)
- [x] 3.2 Remove `garth` entry from `requirements.txt` (already absent; `garminconnect==0.3.3` was already listed)
- [x] 3.3 Re-resolve/install dependencies and confirm no remaining imports of `garth` anywhere in the codebase (only stale `.pyc` cache files reference it; no source references remain)

## 4. Update tests
- [x] 4.1 `tests/platform/test_garminclient.py` — reincorporated (restored from git); no `garth`/compat-client references remain, and it relies on the constructor's non-network no-tokenstore path
- [x] 4.2 `tests/platform/test_platform_types.py` — reincorporated; `test_get_strength_types`/`test_get_yoga_types` updated to call `authed_gclient.get(url)` instead of the removed `authed_gclient.garth.get("connect", url)`
- [x] 4.3 Added `tests/platform/test_garminapi.py` with 13 tests covering: no-tokenstore skip, tokenstore-dir auto-detection, credential login, cached-token reuse, expired/failed-token login fallback, MFA prompt wiring, version-match/mismatch/fetch-error branches, `is_authenticated` (including its exception branch), all of `get`/`put`/`post`/`delete`/`download`, and `__enter__`/`__exit__` — **100% line coverage of `garminworkouts/garmin/garminapi.py`** (61/61 statements, verified via `pytest --cov=garminworkouts.garmin.garminapi --cov-report=term-missing`)

## 5. Verify
- [x] 5.1 Run the full test suite and fix any failures caused by the removed `garth` shim — `tests/platform/` reincorporated; 68/89 tests in that directory pass without any real network access. The remaining 21 failures + 2 subfailures are pre-existing integration tests (`test_platform_calendar.py`, `test_platform_event.py`, `test_platform_types.py`, `test_platform_workout.py`, `test_garminclient.py::test_update_garmin`, `base_test.py::WorkoutTestCase`) that call real Garmin Connect endpoints through `authed_gclient` and fail with `GarminConnectAuthenticationError: Not authenticated` because no live/valid session exists — see 5.2 for why a live session couldn't be established in this session. Not a regression: these tests require a real authenticated session regardless of the auth mechanism used. `tests/models`, `tests/config/test_includeloader.py`, etc. pass except 3 pre-existing unrelated failures in `tests/models/test_workout.py` (ZeroDivisionError in HR-to-pace conversion, unrelated to auth). The auth mechanism itself (`garminapi.py`) has 100% unit-test coverage (see 4.3).
- [x] 5.2 Manually exercise login against a real Garmin Connect account to confirm the new mechanism authenticates — VERIFIED 2026-10-26 with `garminconnect==0.3.20` from a non-blocked network (phone hotspot): credential login succeeded (`is_authenticated=True`), `socialProfile` and `workout-service/workouts` returned 200, `garmin_tokens.json` was written and a fresh `Garmin()` reused it. Earlier failures (429/403/`ACCOUNT_DEACTIVATED`) came from the pre-0.3.20 mobile-login bug plus a Cloudflare IP rate limit. NOTE: the account did not request MFA, so the MFA prompt path was not exercised live (covered only by unit tests).
- [x] 5.3 Confirm `openspec validate --change new-auth-mech --strict` passes
