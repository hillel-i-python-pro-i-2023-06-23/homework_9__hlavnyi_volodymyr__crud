#FROM python:3.11
FROM python:3.11-slim as base

RUN set -ex \
    && RUN_DEPS=" \
    build-essential \
    tk-dev \
    mesa-common-dev \
    wget \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN \
  wget \
    -O sqlite.tar.gz \
    https://www.sqlite.org/src/tarball/sqlite.tar.gz?r=release \
    && \
    tar xvfz sqlite.tar.gz

RUN \
  ./sqlite/configure --prefix=/usr && \
  make && \
  make install \
  && \
  # Smoke test
  sqlite3 --version

ENV PYTHONUNBUFFERED=1
ENV AM_I_IN_A_DOCKER_CONTAINER True

ARG WORKDIR=/wd
ARG USER=user

WORKDIR ${WORKDIR}

RUN useradd --system ${USER} && \
    chown --recursive ${USER} ${WORKDIR}

RUN apt update && apt upgrade -y

COPY --chown=${USER} requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

COPY --chown=${USER} ./app.py app.py
COPY --chown=${USER} ./application application

USER ${USER}

VOLUME ${WORKDIR}/db

ENTRYPOINT ["flask", "run"]
