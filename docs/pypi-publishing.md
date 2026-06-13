# PyPI Publishing

Apeiron uses the distribution name `apeiron-agent` because `apeiron` already belongs to another PyPI project.

## Recommended: Trusted Publishing

PyPI supports GitHub Actions Trusted Publishing, including pending publishers for new projects. Configure this once in PyPI:

- PyPI project name: `apeiron-agent`
- Owner: `insomnia-me`
- Repository: `apeiron`
- Workflow name: `publish.yml`
- Environment name: `pypi`

After that, publishing a GitHub Release or manually running the `Publish to PyPI` workflow will build and upload `apeiron-agent` without storing a long-lived PyPI token.

## Manual Token Fallback

If you prefer manual upload:

```bash
rm -rf dist build *.egg-info
python -m build
python -m twine check dist/*
python -m twine upload dist/*
```

Use `__token__` as the username and a PyPI API token as the password.
