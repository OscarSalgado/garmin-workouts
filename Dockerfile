FROM python:3.15.0-slim-bookworm

ARG PLATFORM

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .
# pyproject.toml is the single source of truth; deps are unpinned -> always latest at build time
RUN pip install --no-cache-dir --upgrade pip . && rm -rf /root/.cache/pip

CMD ["python", "-u", "bot.py"]
