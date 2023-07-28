FROM python:3.11

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

VOLUME db

ENTRYPOINT ["flask", "run"]
