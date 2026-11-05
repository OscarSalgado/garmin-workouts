# Proposal

## Why

The CI workflows do not protect `main` or the published Docker image:

- **`main` is never tested.** `ci.yml` triggers on `push` only for tags (`push: tags: ['*']`), plus PRs. Direct
  pushes to `main` (how this repo is developed) run no tests.
- **Lint is red.** `flake8 garminworkouts tests` (the CI lint step) reports 90 errors today, all in `tests/`
  (36 × F841 in `tests/models/test_workout.py`, W293, E702, F401). Because `build` `needs: [lint]`, a PR run would
  never reach the test matrix.
- **The tag job condition is malformed.** `if: ${{ needs.build.result }} == 'success' && github.ref == ...` mixes
  an expression with literal text; GitHub evaluates the whole string as truthy, so the `refs/heads/main` check is
  ignored.
- **Images are published regardless of CI.** `image.yml` runs on `workflow_run: completed` for CI and Dependabot
  auto-merge and never checks `github.event.workflow_run.conclusion`, so a failed CI still pushes
  `…/garminworkouts-bot` to Docker Hub. Docker Scout in the `merge` job scans `:main` with `PLATFORM_PAIR`, which is
  only defined in the other job.
- **Secrets in the test matrix.** All five matrix jobs receive Garmin credentials and `BOT_TOKEN`, though unit tests
  must not use them (see `isolate-live-garmin-tests`).
- Lint covers only `garminworkouts tests`; `bot.py`, `account.py` and `intervalsicu/` are never linted.

## What Changes

- Run CI on pushes to `main` and on PRs (keep path filters, add `bot.py`, `account.py`, `intervalsicu/**`).
- Fix the 90 flake8 findings and lint `bot.py account.py intervalsicu` too.
- Correct the `tag` job condition to `if: needs.build.result == 'success' && github.ref == 'refs/heads/main'`.
- Gate `image.yml` on `github.event.workflow_run.conclusion == 'success'` and on `main`; scan the pushed digest with
  Scout instead of `:main` + undefined `PLATFORM_PAIR`.
- Remove Garmin/Telegram secrets from the unit-test matrix.

## Capabilities

### New Capabilities
- `ci-pipeline`: what CI runs, when, and what must pass before tagging and publishing images.

### Modified Capabilities

## Impact

- Files: `.github/workflows/ci.yml`, `.github/workflows/image.yml`, test files with lint findings.
- Depends on `isolate-live-garmin-tests` to remove the secrets safely (otherwise the 2 live subtests fail
  instead of being skipped).
