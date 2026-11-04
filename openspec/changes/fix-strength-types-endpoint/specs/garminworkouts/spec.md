# Spec Delta

## ADDED Requirements

### Requirement: StrengthTypesSource

The system SHALL fetch the strength exercise catalogue from the Garmin Connect web-data host (`https://connect.garmin.com/web-data/exercises/Exercises.json`), not from the `connectapi` host, and SHALL keep the existing strength definitions when the catalogue cannot be fetched.

#### Scenario: FetchStrengthCatalogueFromWebData
- **GIVEN** A valid Garmin API session
- **WHEN** get_strength_types() is called
- **THEN** The catalogue is requested from `https://connect.garmin.com/web-data/exercises/Exercises.json` and its categories are written to the strength definitions

#### Scenario: KeepStrengthDefinitionsOnFetchFailure
- **GIVEN** The catalogue request fails or returns no categories
- **WHEN** get_strength_types() is called
- **THEN** A warning is logged and the existing strength definitions are left unchanged
