FROM python:3.12-slim as base

RUN pip install "poetry==1.8.3"

WORKDIR /tmp
COPY poetry.lock pyproject.toml ./
RUN poetry export --without-hashes --without dev > requirements.txt

FROM python:3.12-slim

RUN apt-get update && \
    apt-get install zbar-tools -y

WORKDIR /app

COPY --from=base /tmp/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app

CMD ["python", "main.py"]
