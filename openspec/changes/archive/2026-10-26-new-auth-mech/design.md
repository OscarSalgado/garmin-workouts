## Context

`GarminApi` (`garminworkouts/garmin/garminapi.py`) currently authenticates through `garth.Client`, wrapped by an embedded `_CompatClient` shim that also contains a secondary, best-effort attempt to delegate to `garminconnect.Garmin` inside `_CompatClient.login`, plus a `_MinimalClient` no-op fallback used when neither path is available. In practice the primary `garth` path is broken, so real usage silently falls through to either the untested `garminconnect` branch or the no-op client, which never actually authenticates. The project already lists `garminconnect==0.3.20` as a dependency, and `python-garminconnect` (cyberjunky) is the actively maintained reference implementation for talking to Garmin Connect, including its login/MFA/token-persistence conventions.

## Goals / Non-Goals

**Goals:**
- Make `garminconnect.Garmin` (per the cyberjunky/python-garminconnect strategy) the sole authentication mechanism for `GarminApi`.
- Preserve existing external behavior: `GarminApi(email, password)` construction, `.get/.put/.post/.delete/.download`, `.display_name`, `.full_name`, `.unit_system`, `.version`, and MFA-via-prompt support.
- Preserve token caching so repeated runs (e.g. scheduled jobs) don't require interactive login/MFA every time.

**Non-Goals:**
- Not migrating away from `garminconnect` to some other library.
- Not changing the Intervals.icu auth mechanism (`encode_auth` in `intervalsicu/intervals/api.py`) — out of scope.
- Not adding new auth methods (OAuth apps, SSO) beyond what `garminconnect` itself supports.

## Decisions

- **Use `garminconnect.Garmin` directly instead of the `garth`/`_CompatClient` abstraction.** `garminconnect` already implements the full login flow (initial credential login, MFA, session/token reuse) matching Garmin Connect's current API; re-wrapping it behind a `garth`-shaped compatibility layer added complexity and hid the fact the primary path was dead code. `GarminApi` will hold a `garminconnect.Garmin` instance directly (e.g. `self._client`) rather than an intermediary `garth`-like object.
- **Token persistence via `garminconnect`'s own store, not `garth.dump/load`.** `garminconnect.Garmin.garth.dump(tokenstore)` / `.garth.login(tokenstore)` (the library's built-in token save/resume, keyed off a directory) replaces the custom JSON load/dump in `_CompatClient`. Default tokenstore path stays `./garminconnect` to minimize disruption to existing deployments/CI that may mount that path, but old token files written by the previous `garth`-based flow are not binary-compatible and will trigger a fresh interactive/credential login.
- **MFA stays prompt-based.** Keep `GarminApi.get_mfa()` returning `input("MFA one-time code: ")`, but pass it as `garminconnect.Garmin(..., prompt_mfa=self.get_mfa)` or via whatever hook `garminconnect`'s `Garmin.login()` exposes for MFA, instead of `garth`'s `prompt_mfa`/`resume_login` two-step.
- **Delete `_CompatClient`, `_MinimalClient`, and the `garth` import-fallback module-level shim entirely** rather than keeping them behind a flag. There is no need for a `garth` code path since it is being fully replaced; keeping dead fallback code was the source of the original silent-failure bug.
- **Drop `garth` from dependencies** (`pyproject.toml`, `requirements.txt`) since nothing will import it anymore.

## Risks / Trade-offs

- [Existing persisted `./garminconnect` token caches from the old flow become invalid] → Mitigation: on load failure, fall back to a normal credential + MFA login and re-dump tokens, same as today's `login()` already does when `load()` fails.
- [`garminconnect` library's login/MFA API may differ slightly from the previous `garth`-passthrough signature used inside `_CompatClient.login`] → Mitigation: pin to `garminconnect==0.3.20` (pinned; 0.3.20 includes the mobile-login fix) and validate the real constructor/login signature against the installed package during implementation rather than assuming the code in the old shim was correct (it was unverified/fallback-only code).
- [Removing `garth` may be a breaking change for any external scripts importing `garminworkouts.garmin.garminapi.garth`] → Mitigation: this is an internal implementation detail, not documented as public API; call out as **BREAKING** in the proposal.

## Migration Plan

1. Rewrite `GarminApi.login` to construct and use `garminconnect.Garmin` only.
2. Remove `_CompatClient`, `_MinimalClient`, and the `garth` fallback shim from `garminapi.py`.
3. Update `tests/platform/test_garminclient.py` to mock/exercise the `garminconnect.Garmin` client instead of `garth`.
4. Remove `garth` from `pyproject.toml` / `requirements.txt`; run `pip install -r requirements.txt` (or equivalent) to confirm resolution.
5. Manually verify login against a real Garmin Connect account (or recorded fixture) including the MFA prompt path.
6. No rollback beyond reverting the commit is needed — there is no data migration, only code and dependency changes.

## Open Questions

- Does `garminconnect==0.3.20`'s `Garmin` constructor/`login()` support `prompt_mfa` the same way the old fallback code assumed, or does it require a two-step `login()` / resume with the MFA code entered separately? Needs confirming against the installed package during implementation.
