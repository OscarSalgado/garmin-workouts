# Proposal

## Why

`.github/workflows/garminupdate.yml` (scheduled `garmin-update`) is in a failure loop: **38 of the last 40 runs
failed** (latest 2026-11-04 03:12 UTC) with `429 Too Many Requests` from `sso.garmin.com/mobile/api/login`.

Root cause, from the run log (`Cache not found for input keys: garmin-connect-tokens`):

1. `actions/cache` only **saves** in its post step when the job succeeds. Once a run fails, no tokens are ever
   saved, so every following run starts with no tokens, performs a full SSO login, and gets rate limited again.
2. The key is a constant. Even on success, a cache entry is immutable: refreshed tokens are never written back
   under an existing key, so the cached tokens age until they expire and the spiral starts.
3. The schedule is **hourly** (24 SSO-capable runs/day) for a job whose purpose is to notice a Garmin release
   version bump.

Beyond the 429 loop, on success the job rewrites source files (`garminapi.py`, `models/types.py`,
`models/strength.py`, 50+ generated strength modules and their tests) and pushes them straight to `main` with a
PAT, **without running lint or tests**. The history shows the consequence (`53ece662 Fix: restore strength.py
wiped by regeneration`).

Note: local `main` is 282 commits ahead of `origin/main`; the scheduled job still runs the older workflow and code
on GitHub. This change must be pushed to take effect.

## What Changes

- Run daily (once, off-peak) instead of hourly; keep `workflow_dispatch`.
- Persist tokens with `actions/cache/restore` + `actions/cache/save` using a unique key per run
  (`garmin-tokens-${{ github.run_id }}`) and `restore-keys: garmin-tokens-`, saving with `if: always()` whenever the
  token file exists, so a refreshed token is written even when a later step fails.
- On `429`, exit with a distinct message and do not retry inside the job; add a `concurrency` group so runs never
  overlap.
- Run `flake8` and `pytest -q` on the regenerated tree; open a pull request with the changes
  (`peter-evans/create-pull-request`) instead of pushing to `main`.
- Skip the commit/PR when nothing changed.

## Capabilities

### New Capabilities
- `garmin-catalogue-sync`: how the scheduled Garmin catalogue/version sync authenticates, validates and publishes
  regenerated files.

### Modified Capabilities

## Impact

- Files: `.github/workflows/garminupdate.yml`; optionally `garminworkouts/__main__.py` to return a distinct exit
  code on rate limit.
- Requires the `PAT` (or default token with `pull-requests: write`) to open PRs.
- Related: `unify-garmin-auth-config` renames the `EMAIL`/`PASSWORD` env vars used here.
