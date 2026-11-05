# syntax=docker/dockerfile:1

# ---- builder: compiles wheels (gcc available here only) ----
FROM python:3.15.0-slim-bookworm AS builder

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# pyyaml has no cp315 wheel yet: install it as pure Python (no compiler/libyaml needed).
# Remove once pyyaml publishes a cp315 wheel.
ENV PYYAML_FORCE_LIBYAML=0

COPY pyproject.toml README.md LICENSE ./
COPY garminworkouts ./garminworkouts
# pyproject.toml is the single source of truth; deps are unpinned -> always latest at build time
RUN pip wheel --no-cache-dir . -w /wheels

# ---- runtime: no compiler, non-root ----
FROM python:3.15.0-slim-bookworm

WORKDIR /usr/src/app

ENV PYYAML_FORCE_LIBYAML=0

RUN --mount=type=bind,from=builder,source=/wheels,target=/wheels \
    pip install --no-cache-dir --no-index --find-links=/wheels garmin-workouts \
    && pip freeze > /usr/src/app/requirements.lock

COPY . .

RUN useradd --system --uid 10001 --no-create-home app \
    && mkdir -p events garminconnect \
    && chown app:app events garminconnect

USER app

CMD ["python", "-u", "bot.py"]
