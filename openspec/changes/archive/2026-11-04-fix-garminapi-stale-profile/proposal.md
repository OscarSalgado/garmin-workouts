## Why

`GarminApi.__init__` copies `full_name`, `display_name` and `unit_system` from the Garmin client and logs "Logged in as ..." before any login has happened. The underlying library only fills those fields inside `login()`, so the wrapper reports an empty identity (`Logged in as  ()`) and keeps stale values afterwards. The release-version check also runs only when the client was already authenticated at construction time, so on a fresh login it never queries Garmin.

## What Changes

- `full_name`, `display_name` and `unit_system` become read-through properties of the wrapped client instead of copies taken in the constructor.
- The "Logged in as ..." message is logged at the end of a successful `login()`, not in the constructor.
- The release-version query runs after a successful `login()` (and in the constructor only if the client is already authenticated).
- Unauthenticated construction logs no identity message.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `garmin-api-login`: a successful login SHALL expose the account profile and report it.

## Impact

- Code: `garminworkouts/garmin/garminapi.py`.
- Tests: `tests/platform/test_garminapi.py` (assertions on `unit_system`, `version`, `full_name` set at construction), `tests/conftest.py` fake client.
- No dependency or CLI interface changes.
