# Proposal

## Why

`_garmin_client()` in `garminworkouts/__main__.py` retries a failed login in an unbounded `while True` loop.
`GarminApi.login()` swallows every exception and returns `False`, so with `EMAIL` and `PASSWORD` set in the
environment the loop repeats the same failing login against Garmin SSO forever, with no pause. This risks
rate limiting or account lockout and hung a unit test for 34 s.

## What Changes

- Bound the interactive credential login to 3 attempts, with a short growing pause between attempts.
- When credentials come from the environment, a failed login exits with a non-zero status after one attempt
  instead of retrying.
- Add tests for both behaviours that never touch the network or sleep for real.

## Capabilities

### New Capabilities
- `garmin-cli-login`: how the CLI restores a saved session or logs in with credentials, including retry limits
  and exit behaviour on failure.

### Modified Capabilities

## Impact

- Code: `garminworkouts/__main__.py` (`_garmin_client`), `tests/test___main__.py`.
- No API or dependency changes. The `GarminApi.login()` contract is handled by the separate change
  `typed-garmin-login-errors`.
