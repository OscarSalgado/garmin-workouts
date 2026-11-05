# Design

## Context

Garmin SSO allows roughly one credential login per hour per account from shared runner IPs; token refresh does not
hit that endpoint. Keeping a valid token file between runs is therefore the only thing that keeps the job healthy.

## Goals / Non-Goals

**Goals:**
- A single failed run cannot prevent the next run from having tokens.
- Regenerated code never reaches `main` without passing lint and tests.
- Far fewer SSO-capable runs.

**Non-Goals:**
- Changing what `garmin-update` regenerates or how (`GarminTypes`).
- Storing tokens anywhere other than the Actions cache (e.g. encrypted secrets via API).

## Decisions

- **Split restore/save actions with run-unique keys.** `actions/cache/restore@v6` with `restore-keys:
  garmin-tokens-` picks the newest entry; `actions/cache/save@v6` with `key: garmin-tokens-${{ github.run_id }}`
  runs under `if: always() && hashFiles('~/.garminconnect/garmin_tokens.json') != ''`. Old entries are evicted by
  GitHub's LRU policy. Alternative: one constant key with delete-then-save via `gh cache delete`; rejected as more
  moving parts.
- **Daily schedule** (`17 4 * * *`). Garmin release bumps are not time-critical.
- **PR instead of push.** `peter-evans/create-pull-request` with branch `bot/garmin-update`, so reruns update the
  same PR; tests run in the job before the PR step and CI runs again on the PR.
- **`concurrency: garmin-update`, `cancel-in-progress: false`.**

## Risks / Trade-offs

- [Cache entries evicted after 7 days without access] -> Daily runs access the cache well within that window.
- [Already in a 429 spiral when this lands] -> First run after merge may still 429; it saves nothing, and the next
  daily run (24 h later) is outside the rate-limit window. Optionally seed tokens once with a manual dispatch.
