# Security Policy

## Scope

Apeiron is intended for fetching public URLs and converting public content into agent-friendly text. It is not a credential bypass tool and does not grant permission to access private systems, private data, or content you are not authorized to access.

## Safe Defaults

- Git-based learning commits are disabled by default.
- To opt in, set `APEIRON_GIT_COMMIT=true`.
- When enabled, Apeiron only stages `strategies.json` and `apeiron/learn/heuristics.py`.
- Docker-based infrastructure is optional.

## Responsible Use

Use Apeiron in accordance with applicable law, site terms, robots policies where relevant, and your own organization's security rules. Do not use it for credential stuffing, private data collection, account abuse, or evasion of access controls.

## Reporting

Please open a private security advisory or contact the maintainer before publishing details of a vulnerability.
