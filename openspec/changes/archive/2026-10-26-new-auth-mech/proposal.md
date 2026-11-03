## Why

The Garmin Connect authentication mechanism built on `garth` (embedded via the `_CompatClient` shim in `garminworkouts/garmin/garminapi.py`) is broken: `garth`-based token load/login no longer reliably authenticates against Garmin Connect, and the current code already falls back to a no-op `_MinimalClient` that silently skips real login. We need to replace this mechanism with the authentication strategy used by [cyberjunky/python-garminconnect](https://github.com/cyberjunky/python-garminconnect), which the project already depends on (`garminconnect==0.3.20`) but only uses as a secondary, best-effort fallback inside `_CompatClient.login`.

## What Changes

- **BREAKING**: Remove the `garth`-based `_CompatClient`/`_MinimalClient` login path in `garminworkouts/garmin/garminapi.py` and make the `garminconnect.Garmin` client (cyberjunky/python-garminconnect) the primary and only authentication implementation.
- Authenticate using `garminconnect.Garmin(email, password)` with `.login()`, following that library's token caching convention (`~/.garminconnect` or a configurable tokenstore directory) instead of the current `garth.Client.load/dump` token file handling.
- Preserve MFA support (`get_mfa` prompt) using `garminconnect`'s native MFA flow instead of `garth`'s `prompt_mfa`/`resume_login` mechanism.
- Update `GarminApi.__init__`/`GarminApi.login` to drop `garth`-specific concepts (`domain`, `pool_connections`, CN-domain handling) and delegate `get`/`put`/`post`/`delete`/`download` to the `garminconnect.Garmin` client's request methods.
- Remove the `garth` dependency from `pyproject.toml`/`requirements.txt` once no code references it.
- Update/replace tests in `tests/platform/test_garminclient.py` that assert on the `garth`-based compatibility shim.

## Capabilities

### Modified Capabilities
- `api`: The `APIAuthentication` requirement changes from a `garth`-token-or-fallback model to authentication exclusively via the `garminconnect.Garmin` client (email/password login, its own token persistence, and its native MFA handling).

## Impact

- Affected code: `garminworkouts/garmin/garminapi.py` (removal of `_CompatClient`, `_MinimalClient`, `garth` shim/import, rewrite of `GarminApi`), any callers relying on `GarminApi.garth`/`self.garth` attribute.
- Affected tests: `tests/platform/test_garminclient.py`, `tests/platform/test_platform_types.py` if they reference the compat client.
- Dependencies: drop `garth==0.7.10` from `pyproject.toml` and `requirements.txt`; `garminconnect==0.3.20` becomes a required (not optional) dependency.
- Token storage: token cache location/format changes from `garth`'s dump/load JSON to `garminconnect`'s token store — any persisted `./garminconnect` token files from the old flow are no longer compatible and must be regenerated via re-login.
