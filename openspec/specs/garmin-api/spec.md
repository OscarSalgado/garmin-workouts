# garmin-api Specification

## Purpose

TBD - Defines how the GarminApi class delegates to the centralized Garmin client and keeps its public interface stable.

## Requirements

### Requirement: GarminApi uses centralized client
GarminApi SHALL use the `garmin_client` from `account.py` instead of creating its own Garmin client instance. This eliminates duplicate authentication logic and ensures token caching is centralized.

#### Scenario: GarminApi instantiation
- **WHEN** `GarminApi` is created with email and password parameters
- **THEN** it stores these for reference but delegates actual client operations to `account.garmin_client`

#### Scenario: API requests through GarminApi
- **WHEN** code calls methods like `api.get()` or `api.put()` on a GarminApi instance
- **THEN** these methods delegate to `account.garmin_client.client` for the actual HTTP request

#### Scenario: Authentication status check
- **WHEN** code checks `api.is_authenticated`
- **THEN** it reflects the authentication status of `account.garmin_client`

### Requirement: Maintain GarminApi interface for backward compatibility
The GarminApi class interface SHALL remain unchanged to ensure existing code continues to work without modification.

#### Scenario: GarminApi method availability
- **WHEN** existing code calls `get()`, `put()`, `post()`, `delete()` on GarminApi
- **THEN** these methods are available and function as before

#### Scenario: GarminApi properties
- **WHEN** code accesses properties like `display_name`, `full_name`, `is_authenticated`, `unit_system`
- **THEN** these properties are available and return the expected values from the centralized client
