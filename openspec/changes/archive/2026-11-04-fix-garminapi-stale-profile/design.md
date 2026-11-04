## Context

The garminconnect library fills `display_name`, `full_name` and `unit_system` inside `Garmin.login()` (`_load_profile_and_settings`). `GarminApi.__init__` snapshots them immediately, usually before login, and logs the identity there. `version` is also resolved only if the client is authenticated at construction.

## Goals / Non-Goals

**Goals:** correct identity after login; no stale copies; version check that actually runs on fresh logins.
**Non-Goals:** changing login error handling, retries or token storage (covered by `garmin-api-login` / `garmin-cli-login`).

## Decisions

1. **Read-through properties** for `full_name`, `display_name`, `unit_system` returning `self._client.<attr> or ""` (`None` for `unit_system`). Removes duplicated state; chosen over refreshing copies because it cannot go stale.
2. **Post-login hook in `login()`**: after a successful `_client.login(...)`, log the identity and resolve `version` via a helper `_refresh_version()` shared with `__init__` (which still calls it when already authenticated).
3. **Log moves out of `__init__`**; `logging.info` uses the module `logger`.

Alternative rejected: only moving the log, which leaves `unit_system`/`version` stale.

## Risks / Trade-offs

- Tests that set attributes on a fake client and assert them on the wrapper keep working via properties; tests asserting `unit_system is None` for an unauthenticated client must be checked.
- `version` mismatch still only logs an error (existing behavior).
