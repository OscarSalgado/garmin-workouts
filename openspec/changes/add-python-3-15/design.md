# Design

## Context

See proposal.md - Why. Spike on CPython 3.15.0rc2 (Windows): all dependencies resolve to prebuilt wheels for
`cp315` on Linux x86_64/aarch64 and Windows except `pyyaml` 6.0.3, which would be built from source. On Windows
that fails without Visual Studio. `PYYAML_FORCE_LIBYAML=0` makes it install as pure Python
(`yaml.__with_libyaml__ == False`) and the full suite passes (4776 passed, 374 subtests). `pytest-vcr` is not
imported by any test.

## Goals / Non-Goals

- Goal: the 3.15 job is as strict as the other matrix entries.
- Non-Goal: dropping Python 3.10 or changing `requires-python` / pyright `pythonVersion`.
- Non-Goal: pinning dependencies (the repo deliberately keeps them unpinned).

## Decisions

- **Set `PYYAML_FORCE_LIBYAML=0` only for the 3.15 matrix entry in CI.** 3.10-3.14 have pyyaml wheels with libyaml,
  so the pure-Python fallback would only slow them down. Alternative: set it for all jobs (simpler, slightly slower
  YAML parsing in tests).
- **Set it unconditionally in the `Dockerfile`** (`ENV`), since 3.15 is the only interpreter there. Pure-Python
  pyyaml is slower for large YAML, which is acceptable for this bot's workload. Alternative: keep `gcc` and let pip
  compile with libyaml; rejected because it needs libyaml headers (`libyaml-dev`) and lengthens the arm64 QEMU build.
- **Make the 3.15 job blocking.** Alternative `continue-on-error: true` rejected: it would reopen the publishing gap
  that `fix-ci-pipeline-gating` closed, on exactly the version the image uses.
- **Remove `pytest-vcr` from the `test` extra.** It is unused and only adds `vcrpy` -> `pyyaml`.

## Risks / Trade-offs

- [Pure-Python pyyaml is slower] -> Only affects 3.15; remove the workaround when a `cp315` wheel is released.
- [Spike ran on rc2 / Windows, not on the final Docker image] -> Verify with a real `docker build` on both
  platforms as part of the tasks.
- [`gcc` may still be needed by another dependency] -> Check the Docker build before removing it.

## Migration Plan

Land the CI matrix, metadata and Dockerfile in one PR. Rollback is reverting that PR; the Docker image tag then
keeps using the last published build.
