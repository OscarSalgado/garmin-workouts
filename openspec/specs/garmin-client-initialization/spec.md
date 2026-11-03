# garmin-client-initialization Specification

## Purpose

TBD - Defines module-level initialization and exposure of the authenticated Garmin client in account.py.

## Requirements

### Requirement: Initialize and expose Garmin client at module level
The system SHALL initialize a `garmin_client` variable in `account.py` that provides authenticated access to Garmin's API, using credentials loaded from environment variables and python-garminconnect's token storage for persistence.

#### Scenario: Client initialization on module import
- **WHEN** `account.py` is imported
- **THEN** a `Garmin` client instance is created using `GARMIN_USERNAME` and `GARMIN_PASSWORD` from environment config

#### Scenario: Token storage and persistence
- **WHEN** a user authenticates successfully with MFA
- **THEN** the token is cached in `./.garminworkouts-cache/garmin` directory for future authentications

#### Scenario: Non-interactive environment handling
- **WHEN** `account.py` is imported in a non-interactive environment (no tokenstore found)
- **THEN** authentication is skipped and a warning is logged, allowing tests and CLI tools to proceed

#### Scenario: MFA prompt during authentication
- **WHEN** Garmin requires multi-factor authentication
- **THEN** the client calls the `get_mfa()` function to prompt the user for their MFA code

### Requirement: Provide authenticated Garmin client as public API
The module-level `garmin_client` SHALL be accessible to other parts of the application without requiring them to manage their own authentication or client instances.

#### Scenario: Import garmin_client
- **WHEN** other modules import `account.garmin_client`
- **THEN** they receive the initialized `Garmin` client instance ready for API calls

#### Scenario: Client authentication status
- **WHEN** code queries `garmin_client.client.is_authenticated`
- **THEN** it receives the current authentication status

### Requirement: Maintain backward compatibility with GarminApi
The `GarminApi` class SHALL continue to work but use the centralized `garmin_client` instead of creating its own instance.

#### Scenario: GarminApi initialization
- **WHEN** `GarminApi` is instantiated
- **THEN** it uses the `garmin_client` from `account.py` rather than creating a new Garmin client

#### Scenario: Existing code using GarminApi
- **WHEN** existing code imports and uses `GarminApi`
- **THEN** it continues to function without modification
