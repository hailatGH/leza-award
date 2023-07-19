FROM python:3.8-slim

COPY ./requirements.txt /requirements.txt
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    /py/bin/python manage.py makemigrations && \
    /py/bin/python manage.py makemigrations accounts && \
    /py/bin/python manage.py makemigrations vote && \
    /py/bin/python manage.py migrate && \
    /py/bin/python manage.py migrate accounts && \
    /py/bin/python manage.py migrate vote && \
    /py/bin/python manage.py migrate --run-syncdb 

ENV PATH="/py/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./src /app

EXPOSE 8000