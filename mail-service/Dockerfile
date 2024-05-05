FROM python:latest

ARG TAG
ENV TAG=${TAG}

ARG PRODUCTION
ENV PRODUCTION=${PRODUCTION}

WORKDIR /app

COPY ./src /app/src
COPY ./requirements.txt /app

RUN python3 -m pip install -r requirements.txt

CMD python3 -m src.main ${TAG}