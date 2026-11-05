# Spec Delta

## ADDED Requirements

### Requirement: Image contains only runtime files
The bot image SHALL contain only the application code, packaging metadata and workout/plan data needed at
runtime, and SHALL NOT contain version control data, local tooling state, environment files or Garmin tokens.

#### Scenario: Build from a developer working copy
- **WHEN** the image is built from a working copy that has `.git`, `.env` and a token directory
- **THEN** none of them are present in the image

### Requirement: Image runs unprivileged
The bot process SHALL run as a non-root user without a compiler toolchain in the runtime image.

#### Scenario: Inspect the running container
- **WHEN** the container starts
- **THEN** the bot runs with a non-zero uid
- **AND** `gcc` is not available

### Requirement: Resolved dependencies are recorded
Each image SHALL include the exact list of installed Python package versions.

#### Scenario: Reproduce a deployed image
- **WHEN** an operator needs to know what a published image contains
- **THEN** `requirements.lock` inside the image lists every installed package with its version
