# djapi




## Setup

```shell
poetry install
poetry shell
```

## Run

```shell
poetry uvicorn djapi.asgi:application --reload --port 8000
```

## Migrate DB

```shell
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

## Test
To run test you need to run postgres db in docker container or locally.

```shell
export DB_NAME=db
poetry run pytest .
```

## Get schema

```shell
curl -X GET "http://localhost:8000/schema/" -H  "accept: application/json"
```
