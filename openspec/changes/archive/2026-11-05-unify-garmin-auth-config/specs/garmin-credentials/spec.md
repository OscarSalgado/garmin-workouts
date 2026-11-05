# Spec Delta

## ADDED Requirements

### Requirement: Single source of Garmin credentials
Every entry point SHALL read Garmin credentials from `GARMIN_USERNAME` and `GARMIN_PASSWORD` (environment or
`.env`). `EMAIL` and `PASSWORD` SHALL be accepted only as a deprecated fallback that logs a warning.

#### Scenario: Canonical variables set
- **WHEN** `GARMIN_USERNAME` and `GARMIN_PASSWORD` are set
- **THEN** those values are used for login

#### Scenario: Only legacy variables set
- **WHEN** only `EMAIL` and `PASSWORD` are set
- **THEN** those values are used for login
- **AND** a deprecation warning naming `GARMIN_USERNAME`/`GARMIN_PASSWORD` is logged

### Requirement: Single token store location
The token store SHALL be the path in `GARMINTOKENS`, defaulting to `~/.garminconnect`, for every entry point.

#### Scenario: Container deployment
- **WHEN** the bot runs with the shipped `docker-compose.yml`
- **THEN** tokens are written under the mounted volume and survive a container rebuild

### Requirement: Headless runs never prompt
When stdin is not a terminal, the CLI SHALL NOT prompt for credentials or MFA input it cannot receive; if no valid
tokens and no credentials are available it SHALL exit with a non-zero status and name the variables to set.

#### Scenario: Bot subprocess without tokens or credentials
- **WHEN** the CLI runs without a TTY, the token store is empty and no credentials are configured
- **THEN** it exits with status 1
- **AND** the message names `GARMIN_USERNAME`, `GARMIN_PASSWORD` and `GARMINTOKENS`
