# Fix ZeroDivisionError in convert_HR_to_targetHR

## Purpose

Prevent ZeroDivisionError when fmax equals fmin in heart rate conversion calculations

## Requirements

### Requirement: ZeroDivisionError prevention
The convert_HR_to_targetHR method must handle the edge case where fmax equals fmin without raising ZeroDivisionError

#### Scenario: Normal case - fmax greater than fmin

- **GIVEN** fmax is 185 and fmin is 45
- **WHEN** convert_HR_to_targetHR is called with HR=150
- **THEN** Method returns (150-45)/(185-45) = 0.75 without error

#### Scenario: Edge case - fmax equals fmin

- **GIVEN** fmax is 100 and fmin is 100
- **WHEN** convert_HR_to_targetHR is called with HR=100
- **THEN** Method returns a safe default value (0.0 or 1.0) without raising ZeroDivisionError
