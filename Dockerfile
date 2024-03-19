FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR app
# Копируем папку src из текущего каталога внутрь контейнера
COPY ./src /app/src
# Копируем папку models из текущего каталога внутрь контейнера
COPY ./models /app/models

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

# Копируем app.py из текущего каталога внутрь контейнера
COPY ./app.py /app/
