# Tasks

## 1. Build context

- [x] 1.1 Rewrite `.dockerignore` as an allowlist (`*` then `!` entries for the runtime files and data
  directories). Verify: `docker build --no-cache -t gw-test . && docker run --rm gw-test sh -c 'ls -a /usr/src/app'`
  shows no `.git`, `.claude`, `openspec`, `autonomy`, `build`, `.env`, token directories or notebooks.

## 2. Image

- [x] 2.1 Split the `Dockerfile` into a builder stage (`gcc`, `pip wheel . -w /wheels`) and a runtime stage that
  installs from `/wheels` without `gcc`. Verify: `docker run --rm gw-test sh -c 'command -v gcc'` exits non-zero.
- [x] 2.2 Create user `app` (uid 10001), `chown` only `events/` and the token directory, and set `USER app`.
  Verify: `docker run --rm gw-test id -u` prints `10001`.
- [x] 2.3 Write `pip freeze` to `/usr/src/app/requirements.lock` during the build.
  Verify: `docker run --rm gw-test cat /usr/src/app/requirements.lock` lists `garminconnect==…`.

## 3. Compose and docs

- [x] 3.1 Document the one-time `chown 10001` of `${VOLUME}` in the README and fix the compose file if needed.
  Verify: `docker compose up` starts the bot and it can write to `events/` and the token store.
- [x] 3.2 Verify the multi-arch build still works: `docker buildx build --platform linux/amd64,linux/arm64 .`
  succeeds.
