# Tasks

## 1. Lint green

- [x] 1.1 Fix the flake8 findings in `tests/` (unused `a = get_athlete_values()` assignments, whitespace-only blank
  lines, `;`-joined statements, unused imports). Verify: `flake8 garminworkouts tests` exits 0.
- [x] 1.2 Extend the lint step to `flake8 garminworkouts tests intervalsicu bot.py account.py` and fix what it
  reports. Verify: the command exits 0 locally.

## 2. Triggers and gating in `ci.yml`

- [x] 2.1 Add `push: branches: [main]` (with the same path filters plus `bot.py`, `account.py`, `intervalsicu/**`)
  next to the tag trigger. Verify: `actionlint .github/workflows/ci.yml` is clean and a push to `main` starts CI.
- [x] 2.2 Rewrite the tag condition as
  `if: needs.build.result == 'success' && github.ref == 'refs/heads/main'`. Verify: actionlint clean; a PR run
  shows the `tag` job as skipped.
- [x] 2.3 Remove `GARMIN_*`, athlete and `BOT_TOKEN` secrets from the `build` job env, providing dummy athlete
  values for tests that need them. Verify: CI passes with no secrets referenced in `build`.

## 3. Image publishing

- [x] 3.1 In `image.yml` add
  `if: github.event_name != 'workflow_run' || (github.event.workflow_run.conclusion == 'success' && github.event.workflow_run.head_branch == 'main')`
  to the `build` job. Verify: actionlint clean; a failed CI run produces a skipped image run.
- [x] 3.2 Point Docker Scout at the merged manifest (`${{ env.REGISTRY_IMAGE }}:${{ steps.meta.outputs.version }}`)
  and drop the undefined `PLATFORM_PAIR`. Verify: Scout step runs on the next published image.
