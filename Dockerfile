FROM python:3.9.1-alpine

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /src/

COPY requirements.txt tmp/requirements.txt

RUN set -eux \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    build-base \
    python3-dev \
    bash \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r tmp/requirements.txt \
    && rm -rf /root/.cache/pip \
    && rm -rf tmp \
    && apk del --no-cache .build-deps

EXPOSE 8000

WORKDIR /src
