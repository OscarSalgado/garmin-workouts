## Why

`python -m intervalsicu <command>` runs silently: no console output and an empty `debug.log`. `account.py` logs at import time, which implicitly configures the root logger (WARNING, stderr) before `main()` calls `logging.basicConfig(...)`, turning the latter into a no-op.

## What Changes

- Pass `force=True` to `logging.basicConfig` in `intervalsicu/__main__.py` so the CLI's handlers (file + stdout) and level (`--debug`) replace any pre-existing root configuration.

## Capabilities

### New Capabilities
<!-- None: tooling fix, no spec-level behavior change. -->

### Modified Capabilities
<!-- None. -->

## Impact

- `intervalsicu/__main__.py` only.
- Behavior: INFO/DEBUG messages now reach stdout and `./debug.log` as the CLI help text already implies.
