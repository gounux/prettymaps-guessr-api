# Prettymaps guesser API

## Setup

This bot uses poetry, that can be installed using `python3 -m pip install poetry`.

- install project's dependencies: `poetry install`
- install project's pre-commit hooks: `poetry run pre-commit install`

## Run

Launch the API using following command:

```bash
poetry run uvicorn api:app --reload
```

## Tests

Run tests using following command:

```bash
poetry run pytest
```
