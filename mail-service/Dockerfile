FROM python:latest

ARG TAG
ENV TAG=${TAG}

ARG ENVIRONMENT
ENV ENVIRONMENT=${ENVIRONMENT}

WORKDIR /app

COPY ./src /app/src
COPY ./requirements.txt /app

RUN python3 -m pip install -r requirements.txt

CMD python3 -m src.main ${TAG}