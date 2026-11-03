# Defer credential and client initialization

## Purpose

Enable test mocking and prevent premature authentication by deferring credential loading until first access

## Requirements

### Requirement: Lazy credential loading
Credentials (EMAIL, PASSWORD) must be loaded lazily via functions or properties, not at module import time

#### Scenario: Credentials loaded on first access

- **GIVEN** Module is imported without triggering credential loading
- **WHEN** get_credentials() is called for the first time
- **THEN** Credentials are loaded from environment and cached for subsequent calls

#### Scenario: Tests can mock credentials

- **GIVEN** Test mocks the credential loading function before importing dependent modules
- **WHEN** Module is imported
- **THEN** Mocked credentials are used instead of reading from environment

### Requirement: Lazy client initialization
garmin_client must be initialized lazily via a factory function, not at module level

#### Scenario: Client created on first access

- **GIVEN** Module is imported without creating Garmin client
- **WHEN** get_garmin_client() is called for the first time
- **THEN** Client is initialized with credentials and cached for subsequent calls
