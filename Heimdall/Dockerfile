FROM python:3.8.5-alpine

ARG GITHUB_URL

LABEL maintainer="Shashank Aital"

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev git openssh

RUN mkdir /Heimdall

RUN git clone $GITHUB_URL

WORKDIR /Heimdall

COPY requirements.txt /Heimdall/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
