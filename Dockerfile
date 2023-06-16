FROM python:3.10

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install fastapi-users-db-sqlalchemy==5.0.0

COPY . .

CMD gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
