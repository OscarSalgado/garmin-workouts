# Spec Delta

## ADDED Requirements

### Requirement: Supported Python versions are tested
The unit test matrix SHALL include every Python version declared as supported in the package metadata, and the Python
version used by the published Docker image. A failure on any of them SHALL block tagging and image publishing.

#### Scenario: Newest supported Python fails
- **WHEN** the unit tests fail on the newest supported Python version
- **THEN** the CI run fails and no tag is created and no Docker image is pushed

#### Scenario: Docker image Python is covered
- **WHEN** the Docker image is built on a given Python minor version
- **THEN** the unit test matrix has a job for that same minor version

### Requirement: Installs do not require a compiler
Installing the project in CI and in the Docker image SHALL NOT depend on a C compiler or libyaml headers being present
for any dependency that has no prebuilt wheel for the Python version in use.

#### Scenario: Dependency without a wheel
- **WHEN** a dependency has no prebuilt wheel for the Python version under test
- **THEN** the install still succeeds using the dependency's pure-Python fallback
