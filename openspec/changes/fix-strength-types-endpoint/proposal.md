# Proposal

## Why

`garmin-update` can no longer refresh the strength exercise catalogue: `GET /web-data/exercises/Exercises.json` resolved against the `connectapi` host now returns 404 (Garmin release 26.21.3.0), so `strength.py` and the generated strength generators/tests silently stay stale.

## What Changes

- `get_strength_types` fetches the catalogue from `https://connect.garmin.com/web-data/exercises/Exercises.json`, which answers 200 with the same `{categories: {<CATEGORY>: {exercises: {...}}}}` shape (47 categories, identical to the current `strength.py`).
- The platform tests `test_get_strength_types` and `test_get_yoga_types` use the same host (`Yoga.json` also returns 404 on `connectapi` and 200 on `connect.garmin.com`, 11 categories).
- The existing guard (keep `strength.py` on fetch error or empty payload) is unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `garminworkouts`: adds a requirement stating where the strength catalogue is fetched from and that a failed fetch keeps the existing file.

## Impact

- Code: `garminworkouts/garmin/garmintypes.py` (`get_strength_types`), `tests/platform/test_platform_types.py` (strength and yoga tests).
- No new dependencies. The garminconnect client already accepts absolute URLs on the Garmin domain.
- Out of scope: `exerciseToEquipments.json` (equipment data, different shape), the `/web-api/` and `/gc-api/` prefixes (403 with the library token), and the `ERROR` log level of the version-bump message.
