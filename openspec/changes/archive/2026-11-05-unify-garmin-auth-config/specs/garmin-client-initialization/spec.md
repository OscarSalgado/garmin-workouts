# Spec Delta

## REMOVED Requirements

### Requirement: Initialize and expose Garmin client at module level
**Reason**: The module-level client was never used: `account.garmin_client` is defined as `None`, so `GarminApi`
always built its own client. Authentication lives in the CLI's `_garmin_client()` (see `garmin-cli-login`).
**Migration**: Use `account.get_credentials()` and `account.get_tokenstore()` for configuration and obtain a client
through the CLI login flow.

### Requirement: Provide authenticated Garmin client as public API
**Reason**: Same as above; there is no shared authenticated client.
**Migration**: Pass a `Garmin` instance explicitly to `GarminApi(client=...)` when one is needed.

### Requirement: Maintain backward compatibility with GarminApi
**Reason**: `GarminApi` no longer looks up a centralized client; it uses the client passed in or creates its own.
**Migration**: No caller change needed; `GarminApi(email, password, client=None)` keeps its signature.
