# Garmin Connect Workouts Tools

[![CI](https://github.com/OscarSalgado/garmin-workouts/actions/workflows/ci.yml/badge.svg)](https://github.com/OscarSalgado/garmin-workouts/actions/workflows/ci.yml)
[![CodeQL](https://github.com/OscarSalgado/garmin-workouts/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/OscarSalgado/garmin-workouts/actions/workflows/github-code-scanning/codeql)
[![Dependency Review](https://github.com/OscarSalgado/garmin-workouts/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/OscarSalgado/garmin-workouts/actions/workflows/dependency-review.yml)
[![codecov](https://codecov.io/gh/OscarSalgado/garmin-workouts/graph/badge.svg?token=P2LEVXVKN7)](https://codecov.io/gh/OscarSalgado/garmin-workouts)

A command-line Python application for managing multi-sport training workouts across **Garmin Connect** and **Intervals.icu**, with optional **Telegram bot** control for remote operation.

All workouts are stored as human-readable YAML files under your version control, giving you full ownership of your training data.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage — Garmin Connect](#usage--garmin-connect)
- [Usage — Intervals.icu](#usage--intervalsicu)
- [Usage — Telegram Bot](#usage--telegram-bot)
- [Workout File Format](#workout-file-format)
- [Training Plans](#training-plans)
- [Deployment with Docker](#deployment-with-docker)
- [Project Structure](#project-structure)
- [Development](#development)

---

## Features

- **Version-controlled workouts** — all workout definitions are YAML files, easy to diff and track
- **Multi-sport** — running, cycling, swimming, strength, yoga, pilates, cardio
- **Garmin Connect sync** — create, update, delete, and schedule workouts in a rolling 2-week window
- **Intervals.icu sync** — upload and two-way sync training plans with the Intervals.icu platform
- **Race event management** — link race events to training workouts
- **Reusable components** — share step templates across workouts with `!include` directives and YAML anchors
- **Performance analytics** — TSS, normalized power, intensity factor, training load metrics
- **Athlete zones** — per-sport heart rate zones, FTP, and critical velocity (vVO2)
- **Telegram bot** — remote control of common operations without a terminal
- **Docker support** — run the bot as a persistent container

---

## Architecture Overview

```
garminworkouts/          # Core Garmin Connect integration
  config/                # YAML config reader, !include loader, workout generators
  garmin/                # Garmin API client, sync logic, event/note management
  models/                # Workout, step, event, target, pace, power, duration models
  utils/                 # Math (TSS, NP), validators, functional helpers

intervalsicu/            # Intervals.icu platform integration
  intervals/             # REST API client, sync logic, threshold detection

trainingplans/           # Training plan file generation and management
performance/             # Race performance analytics

bot.py                   # Telegram bot entry point
account.py               # Athlete credentials and performance profile
```

The application uses **Garth** for Garmin OAuth2 SSO with MFA support. Tokens are persisted in `./garminconnect/` to avoid repeated authentication.

---

## Installation

**Requirements:** Python 3.10–3.14

```shell
git clone https://github.com/OscarSalgado/garmin-workouts.git
cd garmin-workouts
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuration

### Credentials and athlete profile

Set the following environment variables, or store them in a `.env` file at the project root:

```dotenv
# Garmin Connect credentials
GARMIN_USERNAME=your@email.com
GARMIN_PASSWORD=yourpassword

# Athlete performance profile
vV02=5:00          # Critical velocity (min/km)
fmin=45            # Minimum heart rate (bpm)

# Running zones
rfmax=185          # Running VO2max heart rate (bpm)
rflt=168           # Running lactate threshold (bpm)
rFTP=300W          # Running FTP (watts, or pace e.g. "4:30")

# Cycling zones
cfmax=180          # Cycling VO2max heart rate (bpm)
cflt=162           # Cycling lactate threshold (bpm)
cFTP=280W          # Cycling FTP (watts)

# Swimming zones
sfmax=178          # Swimming VO2max heart rate (bpm)
sflt=160           # Swimming lactate threshold (bpm)

# Optional — Telegram bot
BOT_TOKEN=your_telegram_bot_token

# Optional — Intervals.icu
intervals_api_key=your_api_key
intervals_athlete_id=your_athlete_id
```

### Planning config

Define your training plans in `events/planning/planning.yaml`:

```yaml
Half2025:
  workouts:
    - trainingplans/Running/Self/Half/Intermediate/*.yaml
  year: 2025
  month: 12
  day: 14 # Race/goal date
```

### Athlete targets config

`target.yaml` (project root) holds per-sport thresholds used for zone calculations and workout metric embedding.

---

## Usage — Garmin Connect

All commands are run as:

```shell
python -m garminworkouts <command> [options]
```

### Training plan management

| Command                     | Description                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| `trainingplan-import PLAN`  | Create or update all workouts for a plan on Garmin Connect, scheduled around the race date |
| `trainingplan-reset PLAN`   | Delete all workouts tagged with the given plan from Garmin Connect                         |
| `trainingplan-metrics PLAN` | Print TSS, normalized power, and intensity factor for every workout in the plan            |
| `event-import PLAN`         | Import race events and their associated workouts                                           |

Example:

```shell
python -m garminworkouts trainingplan-import Half2025
python -m garminworkouts trainingplan-metrics Half2025
```

> The sync window is limited to **±2 weeks from today**. Workouts outside this window are created on their scheduled date but not modified until they fall into the window.

### Zone and challenge operations

| Command            | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `user-zones`       | Push athlete heart rate and power zones to Garmin Connect |
| `challenge-signup` | Register the athlete for available Garmin Challenges      |

### Workout utilities

| Command           | Description                                       |
| ----------------- | ------------------------------------------------- |
| `workout-export`  | Download all Garmin Connect workouts as YAML      |
| `activity-get ID` | Retrieve details for a specific logged activity   |
| `activity-list`   | List recent activities                            |
| `event-get ID`    | Retrieve details for a specific event             |
| `event-list`      | List upcoming events                              |
| `find-events`     | Discover race events matching the athlete profile |

---

## Usage — Intervals.icu

```shell
python -m intervalsicu <command> [options]
```

| Command                    | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `athlete-import`           | Sync athlete profile data to Intervals.icu                        |
| `trainingplan-import PLAN` | Upload training plan workouts to Intervals.icu                    |
| `trainingplan-update PLAN` | Two-way sync a training plan between local YAML and Intervals.icu |
| `workout-export-yaml`      | Download workouts from Intervals.icu as YAML                      |
| `thresholds-detect`        | Compute aerobic and anaerobic thresholds using activity data      |

---

## Usage — Telegram Bot

Start the bot:

```shell
python bot.py
```

Or via Docker (see [Deployment with Docker](#deployment-with-docker)).

Once running, the bot presents an inline keyboard. Available actions map directly to the CLI commands:

- `trainingplan-import`
- `user-zones`
- `challenge-signup`
- `event-import`

---

## Workout File Format

Workouts are defined as YAML files. The format is sport-agnostic; the `sport` field determines how targets and durations are interpreted.

### Fields

| Field         | Required | Description                                                    |
| ------------- | -------- | -------------------------------------------------------------- |
| `name`        | Yes      | Workout name (must match the filename convention)              |
| `description` | No       | Free text; key metrics are auto-appended on import             |
| `sport`       | Yes      | `running`, `cycling`, `swimming`, `strength`, `cardio`, `yoga` |
| `date`        | No       | `{year, month, day}` — absolute date override                  |
| `load`        | No       | Manual training load score                                     |
| `steps`       | Yes      | Ordered list of workout steps (see below)                      |

### Step fields

| Field         | Description                                                             |
| ------------- | ----------------------------------------------------------------------- |
| `type`        | `warmup`, `cooldown`, `interval`, `recovery`, `rest`, `repeat`, `other` |
| `description` | Step label                                                              |
| `duration`    | End condition — see table below                                         |
| `target`      | Performance target — see table below                                    |

### Duration (end condition) formats

| Format       | Meaning                          |
| ------------ | -------------------------------- |
| `"0:20:00"`  | Time: 20 minutes                 |
| `"5km"`      | Distance: 5 kilometres           |
| `"500m"`     | Distance: 500 metres             |
| `lap.button` | Manual lap press                 |
| `"500cal"`   | 500 calories                     |
| `"150bpm"`   | Until heart rate reaches 150 bpm |

### Target formats

| Type              | Example                                       | Description       |
| ----------------- | --------------------------------------------- | ----------------- |
| `power.zone`      | `{type: power.zone, min: 0.75, max: 0.85}`    | 75–85 % FTP       |
| `heart.rate.zone` | `{type: heart.rate.zone, zone: 2}`            | HR zone 2         |
| `pace.zone`       | `{type: pace.zone, min: "4:30", max: "5:00"}` | Pace range min/km |
| `no.target`       | `{type: no.target}`                           | No target         |

### Reusable components

Include shared step files with the `!include` directive:

```yaml
steps:
  - !include inc/warmup.yaml
  - type: interval
    duration: "0:20:00"
    target: { type: power.zone, min: 0.88, max: 0.92 }
  - !include inc/cooldown.yaml
```

Reuse steps within a file with YAML anchors:

```yaml
steps:
  - !include inc/warmup.yaml
  - &MAIN_SET
    - &UNDER { type: interval, duration: "2:00", target: { type: power.zone, min: 0.92, max: 0.95 } }
    - &OVER { type: interval, duration: "1:00", target: { type: power.zone, min: 1.05, max: 1.08 } }
    - *UNDER
    - *OVER
    - type: recovery
      duration: "3:00"
      target: { type: power.zone, min: 0.50, max: 0.55 }
  - *MAIN_SET
  - *MAIN_SET
  - !include inc/cooldown.yaml
```

### Cycling example

```yaml
name: "Tempo 3x15"
sport: cycling
steps:
  - !include inc/warmup.yaml
  - &TEMPO
    type: interval
    duration: "0:15:00"
    target: { type: power.zone, min: 0.88, max: 0.93 }
  - type: recovery
    duration: "0:05:00"
    target: { type: power.zone, min: 0.50, max: 0.55 }
  - *TEMPO
  - type: recovery
    duration: "0:05:00"
    target: { type: power.zone, min: 0.50, max: 0.55 }
  - *TEMPO
  - !include inc/cooldown.yaml
```

### Running example

```yaml
name: "Easy Long Run"
sport: running
steps:
  - type: interval
    description: "Easy aerobic"
    duration: "1:30:00"
    target: { type: pace.zone, min: "5:30", max: "6:30" }
```

### Race event example

```yaml
name: "Half Marathon 2025"
sport: running
date: { year: 2025, month: 12, day: 14 }
goal: "1:30:00"
distance: 21.1
location: "Madrid, Spain"
time: "09:00"
steps:
  - !include workouts/running/race/race_sub90.yaml
```

---

## Training Plans

Training plans are collections of YAML workout files organised under `trainingplans/`:

```
trainingplans/
  Running/
    Self/
      5k/Beginner/HeartRate/
      Half/Intermediate/
  Cycling/
    Self/
      base2026/
  Strength/
  Swim/
  Triathlon/
```

Plans are registered in `events/planning/planning.yaml` with glob patterns and a race date. The import command resolves the patterns, builds `Workout` objects, and syncs them to Garmin Connect and/or Intervals.icu.

The plan name is embedded in the workout description so the tool can identify and manage only workouts belonging to a specific plan, leaving manually created workouts untouched.

---

## Deployment with Docker

Build and start the Telegram bot as a persistent service:

```shell
docker compose up -d
```

The `docker-compose.yml` requires the following environment variables to be set in your shell or a `.env` file:

```dotenv
GARMIN_USERNAME=...
GARMIN_PASSWORD=...
vV02=...
fmin=...
rfmax=... rflt=... rFTP=...
cfmax=... cflt=... cFTP=...
sfmax=... sflt=...
BOT_TOKEN=...
VOLUME=/path/to/your/data          # Directory containing events/ and garminconnect/
```

The container mounts two directories from `$VOLUME`:

- `events/` — planning config and race event definitions
- `garminconnect/` — persisted OAuth tokens (avoids re-authentication on restart)

---

## Project Structure

```
garminworkouts/
  __main__.py            # CLI entry point and command dispatcher
  config/
    configreader.py      # YAML workout/event loader with validation
    includeloader.py     # Custom !include YAML tag
    generators/          # Auto-generators for cycling, running, swimming, strength workouts
  garmin/
    garminapi.py         # Low-level HTTP client with Garth OAuth2
    garminworkout.py     # Workout CRUD and schedule operations
    garminclient.py      # High-level sync logic (calendar, events, notes, plans)
    garminevent.py       # Race event management
    garminnote.py        # Training note management
    garminactivity.py    # Activity retrieval
    garminbiometric.py   # Wellness and biometric data
    garmindownload.py    # FIT file downloads
  models/
    workout.py           # Workout model with metric calculations (TSS, NP, IF)
    workoutstep.py       # Individual step model
    event.py             # Race event model
    target.py            # Performance target model
    pace.py              # Running pace conversions
    power.py             # Cycling/running power model and zone calculations
    duration.py          # Flexible duration parsing (time, distance, reps, calories)
    trainingplan.py      # Training plan metadata
    note.py              # Calendar note model
    strength.py          # Strength exercise library (150+ exercises)
    yoga.py              # Yoga pose library (100+ poses)
    types.py             # Enums: sport, step, condition, target types
    fields.py            # Garmin API field name constants
    date.py              # Date parsing relative to race dates
    time.py              # HH:MM:SS time parsing
    extraction.py        # Data extraction from workout/event models
  utils/
    math.py              # Normalized power, intensity factor, TSS
    validators.py        # argparse validators
    functional.py        # flatten(), filter_empty()
    envdefault.py        # Environment variable loader

intervalsicu/
  __main__.py            # Intervals.icu CLI entry point
  intervals/
    api.py               # REST API client (Basic Auth)
    client.py            # High-level sync logic
    extraction.py        # Format conversion from Garmin to Intervals.icu
    workout.py           # Workout formatting and upload
    target.py            # Target handling for Intervals.icu
    threshold.py         # Aerobic/anaerobic threshold detection (scikit-learn)

trainingplans/
  workout.py             # MesoCreator — mesocycle and periodization generator
  lists.py               # Plan file list utilities

performance/
  performance.py         # Race performance tracking and trend analysis

bot.py                   # Telegram bot (async, python-telegram-bot)
account.py               # Athlete credentials and performance profile
target.yaml              # Per-sport threshold configuration
events/
  planning/
    planning.yaml        # Training plan definitions with goal dates
```

---

## Development

### Running tests

```shell
pytest --cov=garminworkouts --cov-report=xml tests
```

Or use the pre-configured VS Code task: **pytest with coverage**.

### Linting

```shell
flake8 garminworkouts intervalsicu
```

### Test tooling

- **pytest** — test framework
- **pytest-cov** — coverage reporting
- **pytest-vcr** — HTTP cassette recording for reproducible API tests
- **pytest-httpserver** — local HTTP server for integration tests
- **unittest.mock** — object mocking

### Key dependencies

| Package               | Purpose                                  |
| --------------------- | ---------------------------------------- |
| `garth`               | Garmin OAuth2 SSO with MFA               |
| `pyyaml`              | YAML parsing and generation              |
| `requests`            | HTTP client                              |
| `python-telegram-bot` | Telegram bot framework                   |
| `python-decouple`     | `.env` / environment variable management |
| `scikit-learn`        | Threshold detection (linear regression)  |
| `pandas` / `numpy`    | Data processing and analytics            |
| `scipy`               | Scientific computing                     |
