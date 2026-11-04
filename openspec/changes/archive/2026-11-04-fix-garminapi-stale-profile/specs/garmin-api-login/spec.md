## ADDED Requirements

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
