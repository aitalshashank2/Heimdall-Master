FROM python:3.8.5-alpine

LABEL maintainer="Shashank Aital"

ENV PYTHONUNBUFFERED 1

RUN mkdir /Heimdall

WORKDIR /Heimdall

COPY requirements.txt /Heimdall/

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
