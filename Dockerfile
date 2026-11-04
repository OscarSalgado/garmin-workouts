FROM python:3.15.0-slim-bookworm

ARG PLATFORM

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# pyyaml has no cp315 wheel yet: install it as pure Python (no compiler/libyaml needed).
# Remove once pyyaml publishes a cp315 wheel.
ENV PYYAML_FORCE_LIBYAML=0

COPY . .
# pyproject.toml is the single source of truth; deps are unpinned -> always latest at build time
RUN pip install --no-cache-dir --upgrade pip . && rm -rf /root/.cache/pip

CMD ["python", "-u", "bot.py"]
