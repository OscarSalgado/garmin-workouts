# Proposal

## Why

The bot image built by `Dockerfile` and pushed to Docker Hub by `image.yml` copies the whole build context and runs
as root:

- **`.dockerignore` is incomplete.** It does not exclude `.git` (full history, 280+ local commits), `.claude/`,
  `openspec/`, `autonomy/`, `.openlore/`, `.hermes/`, `build/`, `*.egg-info/`, `.ruff_cache/`, notebooks,
  `technical_audit_*.json`, or any token store placed inside the repo (`.garminworkouts-cache/`, `garminconnect/`).
  It lists `docker-compose.yaml` while the file is `docker-compose.yml`. A local `docker build` from a working copy
  can therefore bake account data into a pushed image.
- **Root user.** The container runs `bot.py` as root with write access to the whole app directory.
- **Build toolchain shipped.** `gcc` is installed in the final image.
- **Not reproducible.** Dependencies are unpinned by design (`pyproject.toml`), so two builds of the same commit can
  differ; there is no record of what an image actually contains.

## What Changes

- Switch `.dockerignore` to an allowlist: ignore everything (`*`), then re-include only `garminworkouts/`,
  `bot.py`, `account.py`, `pyproject.toml`, `README.md`, `LICENSE`, `target.yaml`, `trainingplans/`, `workouts/`.
- Multi-stage build: build wheels in a builder stage with `gcc`, install them into a slim runtime stage without it.
- Run as a non-root user (`app`, uid 10001) that owns only the mounted data directories.
- Keep `pyproject.toml` unpinned, but record the resolved set: `pip freeze > /usr/src/app/requirements.lock` in the
  image, so a broken image can be reproduced and rolled back.

## Capabilities

### New Capabilities
- `container-image`: contents, user and reproducibility of the published bot image.

### Modified Capabilities

## Impact

- Files: `Dockerfile`, `.dockerignore`, `docker-compose.yml` (volume ownership note), README Docker section.
- Respects the project decision to keep dependencies unpinned (commit `916d4c02`); only records them.
- Existing volumes must be writable by uid 10001 (`chown` once; documented).
