# Design

## Context

`get_strength_types` calls `self.get("/web-data/exercises/Exercises.json")`, which `GarminApi.get` resolves against `connectapi`. Probing with the saved library token showed:

| URL | Status |
|---|---|
| `connectapi/web-data/exercises/Exercises.json` | 404 |
| `connect.garmin.com/web-data/exercises/Exercises.json` | 200 |
| `connect.garmin.com/web-api/...` and `.../gc-api/...` | 403 |

## Goals / Non-Goals

**Goals:** restore strength catalogue refresh with the smallest change.

**Non-Goals:** adopt `exerciseToEquipments.json`; change the `strength.py` format; touch other type fetchers.

## Decisions

- **Absolute URL on `connect.garmin.com/web-data/`.** The only variant that works with the library's DI token, and the response shape is unchanged so the parser needs no edits. Alternatives: `/web-api/` and `/gc-api/` require the browser session (403); `exerciseToEquipments.json` adds equipment but has a different shape and 49 categories, a separate change.
- **Keep the failure guard.** A non-200 or empty payload still leaves `strength.py` untouched.

## Risks / Trade-offs

- [Garmin moves the file again] -> the guard keeps the old file and logs a warning; the platform test flags it.
