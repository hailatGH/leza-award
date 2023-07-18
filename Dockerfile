FROM python:3.8-slim

ENV POSTGRES_USER lezaadmin  
ENV POSTGRES_PASSWORD StrongP@ssword1212 
ENV POSTGRES_DB leza-award-db
ENV DEBUG True
ENV URL https://leza-award-backend.greenmoss-076a1cd8.francecentral.azurecontainerapps.io/
ENV AZURE_ACCOUNT_NAME lezastoragev100
ENV AZURE_ACCOUNT_KEY Fbmz+x083HxEZ9O21cQr4O8xZyXj4FpeNevGE8Ckd3aWyUPjLB4BGyzZ0giMnh2OqKLW8uHHctC9+ASt4pkTdw==
ENV AZURE_LOCATION lezastorage
ENV AZURE_CONTAINER lezastorage
ENV POSTGRES_HOST leza-award-db.postgres.database.azure.com

COPY ./requirements.txt /requirements.txt
COPY ./src /app
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    /py/bin/python manage.py makemigrations && \
    /py/bin/python manage.py migrate --run-syncdb && \
    /py/bin/python manage.py collectstatic --no-input

ENV PATH="/py/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./src /app

EXPOSE 8000
CMD exec gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --timeout 0 core.wsgi:application
