# garmin-api-login Specification

## Purpose

Defines what `login` on the Garmin API wrapper returns or raises, so callers can tell authentication failures, connectivity failures and rate limiting apart from a simple missing-credentials case.

## Requirements

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

### Requirement: Profile is available after login
After a successful login the wrapper SHALL expose the account's `full_name`, `display_name` and `unit_system` as currently held by the underlying client, and SHALL NOT keep copies taken before the login.

#### Scenario: Profile populated by login
- **WHEN** the wrapper is constructed with an unauthenticated client and a login then succeeds and populates the client profile
- **THEN** `full_name`, `display_name` and `unit_system` return the populated values

### Requirement: Successful login is reported with the account identity
The wrapper SHALL log "Logged in as <full name> (<display name>)" once, when a login succeeds, and SHALL NOT log an identity message at construction.

#### Scenario: Identity logged after login
- **WHEN** a login succeeds
- **THEN** one info message names the full name and display name from the client

#### Scenario: No identity at construction
- **WHEN** the wrapper is constructed with an unauthenticated client
- **THEN** no "Logged in as" message is logged

### Requirement: Release version is checked after login
After a successful login the wrapper SHALL query the Garmin release version and fall back to the built-in default version if the query fails.

#### Scenario: Version queried after login
- **WHEN** a login succeeds and the release endpoint reports a version
- **THEN** `version` equals the reported version

#### Scenario: Version query fails
- **WHEN** a login succeeds and the release endpoint fails
- **THEN** `version` equals the built-in default
