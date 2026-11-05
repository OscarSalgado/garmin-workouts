# intervals-http-client Specification

## Purpose

Defines timeouts, retries and connection reuse for requests to Intervals.icu.

## Requirements

### Requirement: Intervals.icu requests are time-bounded
Every request to Intervals.icu SHALL use a connect and read timeout, defaulting to 5 s and 30 s, overridable per
call.

#### Scenario: Server stops responding
- **WHEN** Intervals.icu accepts the connection but does not answer within the read timeout
- **THEN** the call raises a timeout error instead of blocking indefinitely

### Requirement: Transient failures are retried with backoff
Requests SHALL be retried up to 3 times with exponential backoff on HTTP 429, 500, 502, 503 and 504, honouring
`Retry-After` when present.

#### Scenario: Rate limited once
- **WHEN** Intervals.icu answers 429 with `Retry-After: 1` and then 200
- **THEN** the call returns the 200 response

#### Scenario: Persistent server error
- **WHEN** every attempt returns 503
- **THEN** the call fails after the last retry with an HTTP error

### Requirement: Connections are reused
All requests made through one `IntervalsApi` instance SHALL share a single HTTP session.

#### Scenario: Bulk upload
- **WHEN** several requests are made through the same `IntervalsApi` instance
- **THEN** they are sent through the same session with the same authentication headers
