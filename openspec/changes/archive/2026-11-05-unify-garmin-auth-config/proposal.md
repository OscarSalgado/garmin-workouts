# Proposal

## Why

Garmin credentials and the token store are configured in two incompatible ways, and the headless deployments
(Docker bot, CI) fall between them:

| Where | Credentials | Token store |
|---|---|---|
| CLI `_garmin_client()` (`garminworkouts/__main__.py`) | `EMAIL` / `PASSWORD` | `GARMINTOKENS`, default `~/.garminconnect` |
| `account.py`, `.env.example`, `README.md`, `docker-compose.yml`, `ci.yml` | `GARMIN_USERNAME` / `GARMIN_PASSWORD` | `./.garminworkouts-cache/garmin` |
| `garminupdate.yml` | `EMAIL` / `PASSWORD` (mapped from `GARMIN_*` secrets) | `~/.garminconnect` (cached) |

Consequences:

- In the Docker bot, `docker-compose.yml` sets only `GARMIN_USERNAME`/`GARMIN_PASSWORD`, so once tokens expire the
  CLI subprocess falls through to `input("Email: ")` with no TTY and dies with an uncaught `EOFError`.
- The compose volume is mounted at `/usr/src/app/garminconnect`, but the CLI saves tokens to `/root/.garminconnect`,
  so tokens are lost on every container rebuild, forcing fresh SSO logins (the 429 risk the project already fought).
- `account.garmin_client` is dead: `account.py` defines `garmin_client = None` at module level, so the module
  `__getattr__` never fires and `GarminApi` always gets `None` from `from account import garmin_client`. The
  `garmin-client-initialization` spec describes behaviour that does not exist.

## What Changes

- One credential source: `GARMIN_USERNAME` / `GARMIN_PASSWORD`, with `EMAIL` / `PASSWORD` accepted as a deprecated
  fallback that logs a warning.
- One token store: `GARMINTOKENS`, default `~/.garminconnect`, resolved in one helper in `account.py` and used by
  the CLI.
- Non-interactive runs (no TTY) never call `input()`/`getpass()`: without valid tokens or credentials they exit
  with status 1 and a message naming the variables to set.
- Remove the unused centralized client (`get_garmin_client`, `garmin_client`, `__getattr__`, the
  `default_garmin_client` import in `garminapi.py`) and update the spec to match.
- `docker-compose.yml` sets `GARMINTOKENS=/usr/src/app/garminconnect` so tokens persist on the existing volume;
  `garminupdate.yml` switches to `GARMIN_*` names.

## Capabilities

### New Capabilities
- `garmin-credentials`: where Garmin credentials and tokens come from, for every entry point.

### Modified Capabilities
- `garmin-cli-login`: environment credential names and non-interactive behaviour.
- `garmin-client-initialization`: the module-level client requirements are removed.

## Impact

- Code: `account.py`, `garminworkouts/__main__.py`, `garminworkouts/garmin/garminapi.py`, `docker-compose.yml`,
  `.github/workflows/garminupdate.yml`, `.env.example`, `README.md`, tests in `tests/test_garmin_auth.py` and
  `tests/test___main__.py`.
- Deployments using `EMAIL`/`PASSWORD` keep working (deprecated fallback).
- Existing tokens in `~/.garminconnect` keep working; Docker users get persistence after the next run.
