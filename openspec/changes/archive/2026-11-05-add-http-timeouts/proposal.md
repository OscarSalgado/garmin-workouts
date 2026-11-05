# Proposal

## Why

`intervalsicu/intervals/api.py` (`IntervalsApi`, 34 methods) sends every request through bare
`requests.get/post/put/delete/patch`:

- **No timeout.** A stalled TCP connection blocks the process forever; under the bot or a scheduled job nothing
  recovers it. The ruff rule that would flag this (`S113`) is globally ignored in `pyproject.toml` ("CLI tool, user
  controls execution"), which is no longer true now that runs are unattended.
- **No connection reuse.** Each call opens a new TCP + TLS connection; bulk operations (uploading a plan's
  workouts/events, iterating activities) pay a handshake per request.
- **No retry/backoff** on `429` or transient `5xx`, and inconsistent error handling: some methods check
  `status_code == 200` and log with f-strings, others call `.json()` on whatever came back.

The Garmin side is already bounded (`garminconnect` uses 10–30 s timeouts), so Intervals.icu is the remaining
unbounded network path.

## What Changes

- `IntervalsApi` owns a `requests.Session` with the auth header, a default `(connect, read)` timeout of
  `(5, 30)` seconds (configurable), and an `HTTPAdapter` with `urllib3.Retry` (3 retries, exponential backoff,
  `status_forcelist={429, 500, 502, 503, 504}`, honouring `Retry-After`; urllib3's default idempotent-method set,
  so `POST` uploads are never replayed).
- Callers can still override `timeout`/`headers` per call.
- Add a `raise_for_status`-based helper and use it in methods that currently call `.json()` unchecked; switch
  log calls to lazy `%s` formatting.
- Re-enable ruff `S113` (remove it from the global ignore list) so new unbounded calls are caught.

## Capabilities

### New Capabilities
- `intervals-http-client`: timeouts, retries and connection reuse for Intervals.icu requests.

### Modified Capabilities

## Impact

- Code: `intervalsicu/intervals/api.py`, `pyproject.toml` (ruff ignores), `tests/test_intervals_api.py`.
- Behaviour: calls that used to hang now raise `requests.Timeout` after the configured time; transient 429/5xx are
  retried transparently.
- No new dependencies (`urllib3` ships with `requests`).
