# Proposal

## Why

The Docker image already builds on `python:3.15.0-slim-bookworm` (Dependabot bumped it), but CI only tests Python
3.10-3.14 and the packaging metadata and README stop at 3.14. The published bot therefore runs on an interpreter that
no test exercises. A spike on 3.15.0rc2 shows the code itself is fine (4776 tests pass) and the only blocker is
`pyyaml`, which has no `cp315` wheel on any platform, so installs need a compiler or fall back to pure Python.

## What Changes

- Add `"3.15"` to the CI test matrix as a blocking job.
- Install `pyyaml` without its C extension on 3.15 (`PYYAML_FORCE_LIBYAML=0`) in CI and in the `Dockerfile`, so the
  install does not depend on a compiler or libyaml headers.
- Add the 3.15 classifier to `pyproject.toml` and update the README requirement to "Python 3.10-3.15".
- Drop the unused `pytest-vcr` from the `test` extra (no test imports it; it only pulls in `vcrpy` and `pyyaml`).
- Keep `requires-python = ">=3.10"` and the pyright `pythonVersion` unchanged; dropping 3.10 is a separate change.

## Capabilities

### New Capabilities

### Modified Capabilities
- `ci-pipeline`: the unit test matrix must cover every Python version declared as supported, including the one the
  Docker image runs on.

## Impact

- Files: `.github/workflows/ci.yml`, `Dockerfile`, `pyproject.toml`, `README.md`.
- Depends on `fix-ci-pipeline-gating` (already committed) so that a failing 3.15 job blocks tagging and publishing.
- Revisit and remove the `PYYAML_FORCE_LIBYAML=0` workaround once `pyyaml` ships a `cp315` wheel.
