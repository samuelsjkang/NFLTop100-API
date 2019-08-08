FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual build-dependencies \
  gcc libc-dev linux-headers postgresql-dev \
  && pip install -r /requirements.txt \
  && apk del build-dependencies

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
