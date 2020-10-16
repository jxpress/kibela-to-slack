FROM python:3.8-slim

RUN set -ex \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
  ca-certificates \
  make \
  gcc \
  curl \
  jq \
  zlib1g-dev \
  unzip \
  xz-utils

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - \
  && apt-get install -y nodejs \
  && nodejs -v \
  && npm -v \
  && npm install -g serverless

ENV PATH $PATH:/root/.poetry/bin
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

RUN mkdir -p /app
WORKDIR /app

COPY poetry.lock /app
COPY pyproject.toml /app
RUN poetry install

COPY . /app
