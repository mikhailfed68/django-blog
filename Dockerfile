FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
# stdout и stderr in real time
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev make

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry==1.2.0
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry install

COPY . .
