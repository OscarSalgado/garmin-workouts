# Spec Delta

## Purpose
Defines what `login` on the Garmin API wrapper returns or raises, so callers can tell authentication failures, connectivity failures and rate limiting apart from a simple missing-credentials case.

## ADDED Requirements

### Requirement: Successful login returns true
The Garmin API wrapper SHALL return `True` when a login succeeds, whether it restored cached tokens or used credentials.

#### Scenario: Login with a token store
- **WHEN** login is requested with a token store path and the underlying login succeeds
- **THEN** the result is `True`

### Requirement: Missing credentials return false
The wrapper SHALL return `False` without contacting Garmin when no token store is given and no email and password are configured.

#### Scenario: Nothing to log in with
- **WHEN** login is requested with no token store and no credentials
- **THEN** the result is `False`
- **AND** no network request is made

### Requirement: Typed failures are surfaced
The wrapper SHALL let authentication errors, connection errors and rate-limit errors reach the caller instead of converting them to `False`.

#### Scenario: Rate limited
- **WHEN** Garmin answers the login with a rate-limit error
- **THEN** the rate-limit error is raised to the caller

#### Scenario: Wrong credentials
- **WHEN** Garmin rejects the credentials
- **THEN** the authentication error is raised to the caller

#### Scenario: Connectivity failure
- **WHEN** Garmin cannot be reached during login
- **THEN** the connection error is raised to the caller

### Requirement: Unexpected failures are reported and tolerated
The wrapper SHALL return `False` for any other exception and SHALL report it at warning level, not debug level.

#### Scenario: Unexpected error during login
- **WHEN** the underlying login raises an exception that is not one of the typed failures
- **THEN** the result is `False`
- **AND** a warning is logged with the error
