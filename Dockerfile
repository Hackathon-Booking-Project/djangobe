FROM python:3.7-alpine3.11

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache postgresql-libs \
    && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    && pip install -r requirements.txt

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait
