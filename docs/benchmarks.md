# Benchmarks

This page is intentionally conservative. Add dated rows only after running the command on the stated environment.

| Date | Environment | Command | Verdict | Tier | Notes |
|---|---|---|---|---|---|
| 2026-06-13 | local macOS smoke | `apeiron fetch https://example.com --json` | success | fast | Requires `fetch` extra |

## Reproduce

```bash
apeiron doctor --json
apeiron fetch "https://example.com" --json
```

For protected or JavaScript-heavy sites, include the full command, install profile, proxy/browser setup, and whether Docker infrastructure was running.
