## MODIFIED Requirements

### Requirement: APIAuthentication

The API SHALL require authentication via: Garmin Connect credentials (email + password) submitted through the `garminconnect.Garmin` client, Continuation of an in-progress Garmin login session via that client's MFA flow, Cached Garmin session tokens persisted by the `garminconnect.Garmin` client (used to skip credential/MFA login on subsequent runs), Garmin session token (`is_authenticated` must be True), Basic Auth (Base64 encoded API_KEY:{api_key}) for Intervals.icu requests.

#### Scenario: AuthenticatedRequest
- **GIVEN** a request with valid authentication credentials
- **WHEN** the request is processed
- **THEN** the request is authenticated successfully

#### Scenario: UnauthenticatedRequest
- **GIVEN** a request without authentication
- **WHEN** accessing a protected endpoint
- **THEN** the response status is 401 Unauthorized

#### Scenario: CredentialLogin
- **GIVEN** valid Garmin Connect email and password and no cached session token
- **WHEN** `GarminApi` logs in
- **THEN** the `garminconnect.Garmin` client authenticates via credential login and, if Garmin requires it, prompts for an MFA one-time code

#### Scenario: CachedTokenLogin
- **GIVEN** a previously persisted Garmin Connect session token on disk
- **WHEN** `GarminApi` logs in
- **THEN** the `garminconnect.Garmin` client resumes the session from the cached token without requiring credentials or MFA

#### Scenario: LoginFailureFallsBackToCredentials
- **GIVEN** a cached session token that fails to authenticate (expired or invalid)
- **WHEN** `GarminApi` logs in
- **THEN** it falls back to credential login (with MFA if required) and persists a new session token on success

