## Context

`intervalsicu/__main__.py` imports `account`, which calls `logging.warning/info` at module level. Module-level `logging.*` calls with no handlers invoke `basicConfig()` implicitly, so the root logger already has a stderr handler at WARNING when `main()` runs. A second `basicConfig` call without `force` is ignored.

## Goals / Non-Goals

**Goals:**
- CLI logging honors `--debug`, writes to `./debug.log` and stdout.

**Non-Goals:**
- Changing `account.py` logging behavior or the `garminworkouts` CLI (its own `basicConfig` is out of scope).

## Decisions

- Use `logging.basicConfig(..., force=True)`: minimal, removes the pre-installed handler and applies ours. Alternative: configure logging before `import account` — rejected, it requires reordering imports and is fragile.

## Risks / Trade-offs

- `force=True` discards any handlers installed earlier by imported modules; none are relied upon here.
