FROM python:latest

ARG PRODUCTION
ENV PRODUCTION=${PRODUCTION}

WORKDIR /app

COPY ./src /app/src
COPY ./requirements.txt /app

EXPOSE 8000

RUN python3 -m pip install -r requirements.txt

CMD [ "uvicorn", "src.main:app", "--port=8000", "--host=0.0.0.0" ]
