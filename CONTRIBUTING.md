# Contributing

Thanks for helping Apeiron improve.

## Local Setup

```bash
git clone https://github.com/insomnia-me/apeiron.git
cd apeiron
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,mcp,fetch]"
```

## Checks

Run these before opening a pull request:

```bash
python -m pytest -q
python -m ruff check apeiron tests
python -m mypy apeiron
python -m build
python -m twine check dist/*
```

## Guidelines

- Add tests for behavior changes.
- Keep live-network tests out of required CI unless they are isolated in a smoke job.
- Be honest in docs: mark experimental capabilities as experimental.
- Do not add broad bypass claims without reproducible benchmark evidence.
