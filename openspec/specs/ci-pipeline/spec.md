# ci-pipeline Specification

## Purpose

Defines what CI runs, when it runs, and what must pass before a CalVer tag or a Docker image is published.

## Requirements

### Requirement: Main branch is verified
Every push to `main` and every pull request that touches code, tests or packaging SHALL run lint and the unit test
matrix.

#### Scenario: Direct push to main
- **WHEN** a commit changing `garminworkouts/` is pushed to `main`
- **THEN** the CI workflow runs lint and the test matrix

### Requirement: Lint covers all application code
The lint step SHALL check `garminworkouts`, `intervalsicu`, `tests`, `bot.py` and `account.py`, and SHALL pass on
`main`.

#### Scenario: Lint on a clean tree
- **WHEN** CI runs on `main`
- **THEN** the lint step exits successfully

### Requirement: Publishing requires green CI
A CalVer tag and a Docker image SHALL only be produced from `main` after the test matrix succeeded.

#### Scenario: CI fails
- **WHEN** the CI run for a commit fails
- **THEN** no tag is created and no Docker image is pushed for that commit

#### Scenario: Pull request run
- **WHEN** CI runs for a pull request
- **THEN** the tag job is skipped

### Requirement: Unit tests run without account secrets
The unit test matrix SHALL NOT receive Garmin credentials or the Telegram bot token.

#### Scenario: Test job environment
- **WHEN** the test matrix runs
- **THEN** `GARMIN_USERNAME`, `GARMIN_PASSWORD` and `BOT_TOKEN` are not set from repository secrets
