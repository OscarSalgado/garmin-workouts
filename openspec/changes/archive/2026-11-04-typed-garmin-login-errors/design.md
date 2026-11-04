# Design

## Context

`GarminApi.login()` wraps `garminconnect.Garmin.login`, which already raises
`GarminConnectAuthenticationError`, `GarminConnectConnectionError` (including its `NotFound` subclass) and
`GarminConnectTooManyRequestsError`. The wrapper's blanket `except Exception` discards that information.
Callers inside the repository: the two calls in `_garmin_client()`, which have typed `except` branches that are
currently dead code. `account.py` calls `garminconnect.Garmin.login` directly and is not affected.

## Goals / Non-Goals

**Goals:**
- Callers can distinguish rate limit, bad credentials and connectivity failure.
- Unexpected failures remain non-fatal but visible in logs.

**Non-Goals:**
- Retry policy (change `bound-garmin-login-retries`).
- Changing the `Garmin` client or `account.py`.

## Decisions

- **Re-raise only the three typed exceptions**, placed before the generic `except Exception`. Alternative
  considered: remove the generic handler entirely; rejected because an unexpected error would then crash callers
  that today degrade to `False`.
- **Raise the library's own exception classes** rather than wrapping them in new ones, so the existing `except`
  clauses in `_garmin_client()` start working with no further changes.
- **Warning instead of debug** for the generic handler, so unexpected failures stop being invisible.

## Risks / Trade-offs

- [A caller outside this repository relied on `False` for auth errors] -> Documented as BREAKING; the only known
  callers already catch the typed exceptions.
- [`garminconnect` changes which exceptions it raises] -> Tests assert on the three classes, so a rename fails
  loudly.
