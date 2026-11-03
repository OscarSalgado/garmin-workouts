## Why

Authentication logic is currently scattered across account.py (credentials loading) and garminapi.py (client initialization). This makes token management inconsistent and harder to maintain. Centralizing authentication in account.py with python-garminconnect's token storage simplifies credential handling and improves security by keeping tokens managed in one place.

## What Changes

- Move `Garmin` client initialization from `GarminApi.__init__` to `account.py` as a module-level `garmin_client`
- Consolidate token storage configuration to use python-garminconnect's built-in token caching
- Update `GarminApi` to use the centralized `garmin_client` instead of creating its own
- Maintain backward compatibility with existing MFA flow
- Update `.env.example` to document token storage expectations

## Capabilities

### New Capabilities

- `garmin-client-initialization`: Centralized Garmin client creation and authentication in account.py, handling token persistence and MFA prompts

### Modified Capabilities

- `garmin-api`: Updated to use the centralized garmin_client from account.py instead of initializing its own client instance

## Impact

- **Code changes**: account.py, garminworkouts/garmin/garminapi.py, garminworkouts/garmin/garminclient.py (if exists)
- **Tests**: test_garmin_auth.py and related Garmin integration tests
- **Configuration**: .env.example updated to document token storage paths
- **Dependencies**: No new dependencies (python-garminconnect already in use)
- **Breaking changes**: GarminApi initialization signature may change; verify debug_client.py usage
