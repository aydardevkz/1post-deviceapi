FROM python:3.9-slim

LABEL maintainer="ADR"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/var/www/html/onepost

RUN apt-get update \
    && apt install -y gcc \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip

WORKDIR $APP_HOME

COPY ./requirements/base.txt ./requirements/base.txt
COPY ./requirements/production.txt ./requirements/production.txt
COPY ./requirements/local.txt ./requirements/local.txt

RUN pip install -r ./requirements/production.txt

COPY . .

RUN chmod +x start.sh
RUN chmod +x start_dev.sh
