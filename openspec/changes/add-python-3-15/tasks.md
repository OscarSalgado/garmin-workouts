# Tasks

## 1. CI

- [x] 1.1 Add `"3.15"` to the `build` job matrix in `.github/workflows/ci.yml` and set `PYYAML_FORCE_LIBYAML: "0"`
  for that matrix entry only. Verify: the 3.15 job installs and passes in a PR run.
- [x] 1.2 Confirm the `tag` and image gating treat a failing 3.15 job as a failure. Verify: `result` job fails when
  `build` fails (no `continue-on-error` on 3.15).

## 2. Docker

- [ ] 2.1 Set `ENV PYYAML_FORCE_LIBYAML=0` in the `Dockerfile` before the `pip install`. Verify:
  `docker build` succeeds for linux/amd64 and linux/arm64.
- [ ] 2.2 Check whether `gcc` is still required by any dependency; remove it from the `apt-get` line only if the
  build succeeds without it on both platforms.

## 3. Metadata and docs

- [x] 3.1 Add the `Programming Language :: Python :: 3.15` classifier to `pyproject.toml`.
- [x] 3.2 Update the README requirement to "Python 3.10-3.15".
- [x] 3.3 Remove `pytest-vcr` from the `test` extra in `pyproject.toml`. Verify: `pytest` still passes.
