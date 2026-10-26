# Garmin Auth Refactor - Implementation Tasks

## 1. Preparation

- [x] 1.1 Update `.env.example` to document token storage path (`.garminworkouts-cache/garmin`)
- [x] 1.2 Create `.garminworkouts-cache/` directory structure in gitignore handling

## 2. Core Implementation

- [x] 2.1 Add `get_mfa()` function to `account.py` for MFA prompts
- [x] 2.2 Create module-level `garmin_client` initialization in `account.py` using Garmin() from garminconnect
- [x] 2.3 Configure token storage path to `./.garminworkouts-cache/garmin` in garmin_client initialization
- [x] 2.4 Handle non-interactive environments gracefully (skip login, log warning)
- [x] 2.5 Export `garmin_client` from `account.py` for use by other modules

## 3. Update GarminApi Class

- [x] 3.1 Modify `GarminApi.__init__()` to accept optional client parameter, use `account.garmin_client` by default
- [x] 3.2 Update `GarminApi.login()` to use the centralized client instead of creating a new one
- [x] 3.3 Ensure `GarminApi.is_authenticated` property delegates to `account.garmin_client.client.is_authenticated`
- [x] 3.4 Verify all GarminApi methods (`get()`, `put()`, `post()`, etc.) use the centralized client

## 4. Testing

- [x] 4.1 Create `tests/test_garmin_auth.py` with tests for:
  - [x] 4.1a Garmin client initialization with valid credentials
  - [x] 4.1b Garmin client authentication status
  - [x] 4.1c Token persistence and retrieval from cache
  - [x] 4.1d MFA flow with mocked input
  - [x] 4.1e Non-interactive environment handling
- [x] 4.2 Update existing `GarminApi` tests to ensure backward compatibility
- [x] 4.3 Run full test suite to verify no regressions
- [x] 4.4 Verify `debug_client.py` still works with new auth structure

## 5. Integration & Documentation

- [x] 5.1 Update docstrings in `account.py` explaining the `garmin_client` usage
- [x] 5.2 Update docstrings in `GarminApi` class explaining the delegation to `account.garmin_client`
- [x] 5.3 Update README.md if it documents authentication flow
- [x] 5.4 Add migration notes to CHANGELOG or commit message about centralized auth
