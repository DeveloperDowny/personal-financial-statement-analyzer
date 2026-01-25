## Dev env setup

### Setup python
```
python -m pip install uv
uv venv --python=3.12
.venv\Scripts\activate
uv sync
uv sync --extra dev
```

## Contribution Guidelines
- Always create feature branch from dev branch
- Create PRs against dev branch

## Run pytest
uv run --python 3.12 --with pytest-cov --with ".[test]" 
