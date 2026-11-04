# Design

## Context

`_garmin_client()` first tries `GarminClient(email="", password="").login(tokenstore)`, then loops asking for
credentials. `GarminApi.login()` currently turns every exception into `False`, so the loop cannot tell a wrong
password from a network failure or a rate limit; the typed `except` branches in the loop never run. Fixing that
contract is out of scope here (see change `typed-garmin-login-errors`). This change must therefore bound the loop
using only the `True`/`False` result.

## Goals / Non-Goals

**Goals:**
- No code path in `_garmin_client()` can retry forever.
- Credentials from the environment are never retried.
- Tests exercise the loop without network access or real sleeping.

**Non-Goals:**
- Changing `GarminApi.login()` or exception propagation.
- Changing token restoration or `account.py`.

## Decisions

- **Counted loop instead of `while True`.** `for attempt in range(MAX_LOGIN_ATTEMPTS)` with a module constant of 3.
  Alternative considered: keep `while True` and break on a counter; rejected as easier to regress.
- **Credential source decides the policy.** If `EMAIL` and `PASSWORD` are both set, make one attempt and
  `sys.exit(1)` on failure, because repeating the same values cannot succeed. Interactive entry gets the retries.
- **Backoff via `time.sleep(attempt)`** (1 s, 2 s) between interactive attempts, imported at module level so
  tests patch `garminworkouts.__main__.time.sleep`.
- **Return `None` after exhausting interactive attempts**, matching the existing connection-error behaviour.

## Risks / Trade-offs

- [Callers expect a client and get `None`] -> Callers already handle `None` today (connection error path).
- [Environment with only one of `EMAIL`/`PASSWORD`] -> Treated as interactive for the missing value, so retries
  stay bounded.
