FROM python:latest
WORKDIR /usr/src/app

COPY requirements.txt  ./
RUN pip install -r requirements.txt
RUN pip install alembic
RUN pip install uvicorn

COPY app.py alembic.ini ./
COPY src ./src
COPY alembic ./alembic
COPY wait-for-postgres.sh ./

# install psql
RUN apt-get update
RUN apt-get -y install postgresql-client

# make wait-for-postgres.sh executable
RUN chmod +x wait-for-postgres.sh

EXPOSE 8000

CMD ["app"]
