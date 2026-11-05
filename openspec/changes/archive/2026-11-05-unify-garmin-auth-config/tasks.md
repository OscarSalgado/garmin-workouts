# Tasks

## 1. Single configuration source

- [x] 1.1 Add `account.get_tokenstore()` (expanded `GARMINTOKENS`, default `~/.garminconnect`) and make
  `account.get_credentials()` read `GARMIN_USERNAME`/`GARMIN_PASSWORD`, falling back to `EMAIL`/`PASSWORD` with a
  deprecation warning, returning `None` for missing values instead of raising.
  Verify: unit tests cover canonical, fallback-with-warning and missing cases.
- [x] 1.2 Make `_garmin_client()` use `account.get_tokenstore()` and `account.get_credentials()`; remove its direct
  `os.getenv` calls. Verify: `grep -n 'os.getenv' garminworkouts/__main__.py` returns nothing.

## 2. Headless behaviour

- [x] 2.1 When stdin is not a TTY and no usable tokens or credentials exist, print which variables to set and exit
  with status 1 without calling `input` or `getpass`.
  Verify: test with `sys.stdin.isatty` patched to `False` asserts `SystemExit(1)` and that `input`/`getpass` are
  never called.

## 3. Remove the dead centralized client

- [x] 3.1 Delete `get_garmin_client`, `garmin_client`, `_garmin_client_property`, `__getattr__`, `is_interactive`
  and `tokenstore` from `account.py`, and the `default_garmin_client` import/branch in `garminapi.py`.
  Verify: `grep -rn "garmin_client\b\|get_garmin_client" --include=*.py .` matches only `_garmin_client` in
  `__main__.py` and its tests.
- [x] 3.2 Update `tests/test_garmin_auth.py` to the new API. Verify: `pytest tests/test_garmin_auth.py -q` passes.

## 4. Deployments and docs

- [x] 4.1 Add `GARMINTOKENS=/usr/src/app/garminconnect` to `docker-compose.yml`.
  Verify: `docker compose config` shows the variable and the volume target matches it.
- [x] 4.2 Rename `EMAIL`/`PASSWORD` to `GARMIN_USERNAME`/`GARMIN_PASSWORD` in `garminupdate.yml`.
- [x] 4.3 Update `.env.example`, the `__main__.py` module docstring and the README auth section.
  Verify: `grep -rn "\bEMAIL\b" README.md .env.example .github` only mentions the deprecated fallback.
- [x] 4.4 Full suite. Verify: `pytest -q` shows no new failures.
