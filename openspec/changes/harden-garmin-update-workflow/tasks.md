# Tasks

## 1. Token persistence

- [ ] 1.1 Replace `actions/cache` with `actions/cache/restore` (`restore-keys: garmin-tokens-`) before the run and
  `actions/cache/save` (`key: garmin-tokens-${{ github.run_id }}`, `if: always()` and token file present) after it.
  Verify: actionlint clean; after two manual dispatches the second log shows `Cache restored from key:
  garmin-tokens-<previous run id>` and no SSO login.

## 2. Schedule and concurrency

- [ ] 2.1 Change the cron to once a day and add `concurrency: { group: garmin-update, cancel-in-progress: false }`.
  Verify: actionlint clean; `gh workflow view garminupdate.yml` shows the daily schedule.

## 3. Validate before publishing

- [ ] 3.1 After `python -m garminworkouts garmin-update`, run `flake8 garminworkouts tests` and `pytest -q`.
  Verify: a dispatch with a deliberately broken regenerated file fails at the test step and opens no PR.
- [ ] 3.2 Replace `git-auto-commit-action` with `peter-evans/create-pull-request` (branch `bot/garmin-update`,
  delete-branch on merge). Verify: a dispatch with changes opens or updates one PR; with no changes, none.

## 4. Rate-limit handling

- [x] 4.1 Make the CLI exit with a dedicated status (e.g. 75) on `GarminConnectTooManyRequestsError` and have the
  workflow report it as a warning annotation. Verify: unit test asserts the exit status; workflow shows the
  annotation.

## 5. Deploy

- [ ] 5.1 Push `main` (currently 282 commits ahead of `origin/main`) so the scheduled job runs this version.
  Verify: `git rev-list --count origin/main..main` is 0 and the next scheduled run uses the new workflow.
