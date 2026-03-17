## Dev env setup

### Setup python

```
python -m pip install uv
uv venv --python=3.12
.venvScriptsactivate
uv sync
uv sync --extra dev
```

## Contribution Guidelines

- Always create feature branch from dev branch
- Create PRs against dev branch

## Pre-commit setup

```bash
uv sync --group dev
uv run pre-commit install
uv run pre-commit run --all-files
```

## Run pytest

````cmd
uv run --python 3.12 --with pytest-cov --with .[test] pytest -Werror --cov=datasette --cov-config=.coveragerc --cov-report xml:coverage.xml --cov-report term```
````
