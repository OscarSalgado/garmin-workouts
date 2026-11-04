# Proposal

## Why

`GarminApi.login()` catches every exception and returns `False`, logging only at debug level. A wrong password,
a network failure and a Garmin rate limit (HTTP 429) are therefore indistinguishable to callers, and the typed
`except` branches in `_garmin_client()` (rate-limit exit, wrong credentials, connection error) can never run.

## What Changes

- `GarminApi.login()` re-raises `GarminConnectAuthenticationError`, `GarminConnectConnectionError` and
  `GarminConnectTooManyRequestsError` instead of converting them to `False`.
- Any other exception still returns `False`, but is logged at warning level instead of debug.
- Success and the "no tokenstore and no credentials" case keep returning `True` and `False` respectively.
- **BREAKING** for callers that relied on `login()` never raising these three exceptions. In this repository the
  only callers are in `_garmin_client()`, which already catches them.

## Capabilities

### New Capabilities
- `garmin-api-login`: the contract of `GarminApi.login()`: return values and which failures are surfaced as
  exceptions.

### Modified Capabilities

## Impact

- Code: `garminworkouts/garmin/garminapi.py`, `tests/platform/test_garminapi.py`, and a check of
  `tests/platform/test_garminclient.py`.
- `account.py` is unaffected: it calls `garminconnect.Garmin.login` directly, not `GarminApi.login`.
- Depends on, but does not require, change `bound-garmin-login-retries`.
