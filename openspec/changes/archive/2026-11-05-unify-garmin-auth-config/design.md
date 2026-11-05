# Design

## Context

Two auth paths grew in parallel: the `garmin-auth-refactor` change added a lazy centralized client in `account.py`,
and the later `bound-garmin-login-retries` / `typed-garmin-login-errors` changes hardened the CLI's own
`_garmin_client()`. Only the CLI path is actually used. The bot and the hourly workflow both run the CLI headless.

## Goals / Non-Goals

**Goals:**
- Every entry point (CLI interactive, CLI headless, Docker bot, GitHub workflow) reads the same variables.
- Headless runs never block on or crash in a prompt.
- Tokens persist across container restarts with the shipped `docker-compose.yml`.

**Non-Goals:**
- New auth methods, token encryption, or changes to `garminconnect` itself.
- Intervals.icu configuration.

## Decisions

- **`GARMIN_USERNAME`/`GARMIN_PASSWORD` are canonical.** They are already what the README, `.env.example`, compose
  file and CI secrets use; only the CLI and one workflow use `EMAIL`/`PASSWORD`. Fallback keeps old setups alive for
  one release, with a deprecation warning.
- **Read through `python-decouple` in `account.py`** so `.env` works for the CLI exactly as for the rest of the app
  (today `os.getenv` in `__main__` ignores `.env`).
- **`account.get_tokenstore()`** returns the expanded `GARMINTOKENS` path, default `~/.garminconnect`. The old
  `./.garminworkouts-cache/garmin` path is dropped; it was only used by the dead centralized client.
- **TTY check decides prompting.** If `sys.stdin.isatty()` is false and credentials are missing, exit 1. This
  replaces the existing `is_interactive` flag, which was only used by the dead client.
- **Delete the centralized client rather than wire it in.** Wiring it would add a second login per process and
  duplicate the bounded-retry logic. Removing it makes the spec match the code.

## Risks / Trade-offs

- [Someone imports `account.garmin_client` or `get_garmin_client`] -> `grep` shows only tests use them; tests are
  updated. Mention in the release notes.
- [Docker users lose the first login after upgrade] -> One fresh login, then tokens persist on the volume.
