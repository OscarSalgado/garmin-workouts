# Fix command injection in bot.py subprocess calls

## Purpose

Eliminate command injection vulnerability by using shell=False and validating user input in subprocess calls

## Requirements

### Requirement: Safe subprocess usage
All subprocess.run calls must use shell=False with list arguments instead of shell=True with string commands

#### Scenario: Training plan import with valid input

- **GIVEN** User selects a valid training plan via Telegram callback
- **WHEN** Bot executes subprocess with shell=False and validated arguments
- **THEN** Command executes successfully without shell interpretation

#### Scenario: Malicious input is rejected

- **GIVEN** User provides callback_data containing shell metacharacters like '; rm -rf /'
- **WHEN** Input is validated against allowlist before subprocess execution
- **THEN** Invalid input is rejected and logged, no command executes

### Requirement: Input validation
User-provided input (callback_data) must be validated against an allowlist of known safe values

#### Scenario: Valid workout name passes validation

- **GIVEN** Allowlist contains 'Races', 'Zones', 'Challenges' and known training plan names
- **WHEN** callback_data matches an entry in the allowlist
- **THEN** Command proceeds with validated input
