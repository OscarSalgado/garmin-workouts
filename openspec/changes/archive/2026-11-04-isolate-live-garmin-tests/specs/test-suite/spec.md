# Spec Delta

## ADDED Requirements

### Requirement: Default test run is offline
The default `pytest` invocation SHALL NOT open network connections to external hosts and SHALL NOT require Garmin
credentials or athlete secrets.

#### Scenario: Run without credentials
- **WHEN** `pytest` runs with no `.env` and no `GARMIN_*` variables
- **THEN** every collected test runs and passes without network access

#### Scenario: Accidental network call
- **WHEN** a default-run test tries to reach an external host
- **THEN** the test fails with an explicit socket-blocked error

### Requirement: Live account tests are opt-in
Tests that read from or write to the real Garmin account SHALL be marked `live` and SHALL only run when explicitly
selected.

#### Scenario: Default run
- **WHEN** `pytest` runs without a marker expression
- **THEN** no `live` test is executed and the athlete's Garmin account is not modified

#### Scenario: Explicit live run
- **WHEN** `pytest -m live` runs with valid credentials
- **THEN** the live tests run against the real account

### Requirement: Coverage reflects application code
Coverage measurement SHALL include all hand-written application modules and SHALL exclude only generated code.

#### Scenario: Coverage report
- **WHEN** `pytest --cov` runs
- **THEN** `garminworkouts/garmin/` and `garminworkouts/__main__.py` appear in the report
