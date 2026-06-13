# Benchmarks

Apeiron includes a bundled smoke benchmark for the main promise of the project: can it turn real public web sources into useful LLM-ready content?

```bash
apeiron bench
apeiron bench --json
```

The output is an `Apeiron Web Access Score` plus one result per URL. Each result includes:

- pass/fail
- category
- verdict
- tier
- extracted character count
- elapsed time
- failure reason

## Reproduce

```bash
apeiron doctor --json
apeiron bench --json
```

## Default Case Set

The bundled cases live in `apeiron/data/benchmark_cases.json`. The initial set is intentionally small and public:

- documentation pages
- normal HTML pages
- research abstract/PDF URLs
- media-adjacent developer sources

Keep default cases stable, public, and legal to access. Do not add private, credentialed, or intentionally abusive targets.

## Reporting Results

This page is intentionally conservative. Add dated rows only after running the command on the stated environment.

| Date | Environment | Command | Score | Notes |
|---|---|---|---|---|
| 2026-06-13 | local macOS dev venv, no browser/document extras | `apeiron bench --json` | 4/8, 50.00% | Baseline smoke run; PDF extraction needs the document extra |

For protected or JavaScript-heavy sites, include the full command, install profile, proxy/browser setup, and whether Docker infrastructure was running.
