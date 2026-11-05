# garmin-cli-login Specification

## Purpose

Defines how the command line tool obtains an authenticated Garmin client: restoring saved tokens first, then logging in with credentials, with bounded retries so a failing login can never loop indefinitely.

## Requirements

### Requirement: Restore a saved session first
The CLI SHALL try to restore a saved session from the token store before asking for or using credentials.

#### Scenario: Valid saved tokens
- **WHEN** the token store holds valid tokens
- **THEN** the CLI returns an authenticated client without using credentials

### Requirement: Environment credentials fail fast
When `GARMIN_USERNAME` and `GARMIN_PASSWORD` (or the deprecated `EMAIL` and `PASSWORD`) are provided through the
environment or `.env`, a failed login SHALL make the CLI exit with a non-zero status after a single attempt and
SHALL NOT retry.

#### Scenario: Environment credentials rejected
- **WHEN** no valid tokens exist, `GARMIN_USERNAME` and `GARMIN_PASSWORD` are set, and the login fails
- **THEN** exactly one login attempt is made
- **AND** the CLI exits with status 1 and a message explaining the failure

### Requirement: Interactive login is bounded
When credentials are typed by the user, the CLI SHALL allow at most 3 login attempts, pausing briefly and increasingly between attempts, and SHALL then give up.

#### Scenario: Interactive attempts exhausted
- **WHEN** no valid tokens exist, credentials are entered interactively, and every login fails
- **THEN** at most 3 login attempts are made
- **AND** the CLI returns no client

#### Scenario: Interactive login succeeds on a retry
- **WHEN** an interactive login fails once and then succeeds
- **THEN** the CLI returns the authenticated client after the second attempt

### Requirement: User interruption stops login
The CLI SHALL stop the login flow immediately when the user interrupts it.

#### Scenario: Interrupt during credential entry
- **WHEN** the user interrupts while the CLI is asking for credentials
- **THEN** the CLI returns no client without further attempts
