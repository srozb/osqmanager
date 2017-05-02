FROM python:3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client mysql-client\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /usr/src/app/osqmanager
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
