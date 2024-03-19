FROM python:3.10-slim

WORKDIR app

COPY ./requirements.txt /app/

RUN pip install -r /app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY ./app.py /app/
