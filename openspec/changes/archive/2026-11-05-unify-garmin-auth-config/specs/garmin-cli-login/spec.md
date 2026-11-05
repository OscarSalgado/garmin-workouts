# Spec Delta

## MODIFIED Requirements

### Requirement: Environment credentials fail fast
When `GARMIN_USERNAME` and `GARMIN_PASSWORD` (or the deprecated `EMAIL` and `PASSWORD`) are provided through the
environment or `.env`, a failed login SHALL make the CLI exit with a non-zero status after a single attempt and
SHALL NOT retry.

#### Scenario: Environment credentials rejected
- **WHEN** no valid tokens exist, `GARMIN_USERNAME` and `GARMIN_PASSWORD` are set, and the login fails
- **THEN** exactly one login attempt is made
- **AND** the CLI exits with status 1 and a message explaining the failure
