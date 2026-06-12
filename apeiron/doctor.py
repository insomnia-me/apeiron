from __future__ import annotations

import importlib.util
import shutil
import sys
from importlib.metadata import PackageNotFoundError, version
from typing import Any

from apeiron.version import __version__

PACKAGE_CHECKS = {
    "httpx": "minimal",
    "curl_cffi": "fetch",
    "trafilatura": "fetch",
    "markitdown": "documents",
    "yt_dlp": "media",
    "mcp": "mcp",
    "patchright": "browser",
    "camoufox": "browser",
    "cloakbrowser": "browser",
    "browser_use": "browser",
}


def _package_status(module_name: str) -> dict[str, str | bool]:
    installed = importlib.util.find_spec(module_name) is not None
    package_name = module_name.replace("_", "-")
    found_version = ""
    if installed:
        try:
            found_version = version(package_name)
        except PackageNotFoundError:
            found_version = "installed"
    return {"installed": installed, "version": found_version}


def collect_diagnostics() -> dict[str, Any]:
    packages = {name: _package_status(name) for name in PACKAGE_CHECKS}
    docker_installed = shutil.which("docker") is not None
    services = {
        "docker": {
            "installed": docker_installed,
            "hint": "Needed only for optional SearXNG and FlareSolverr infrastructure.",
        },
        "searxng": {
            "url": "http://localhost:4004",
            "hint": "Run scripts/start-infra.sh for local meta-search.",
        },
        "flaresolverr": {
            "url": "http://localhost:8191",
            "hint": "Run scripts/start-infra.sh for optional FlareSolverr tier.",
        },
    }

    missing = [name for name, status in packages.items() if not status["installed"]]
    recommendations = []
    if missing:
        recommendations.append("Install extras with: pip install -e '.[fetch,mcp]' or pip install -e '.[all]'.")
    if not docker_installed:
        recommendations.append("Docker is optional; install it only if you need SearXNG or FlareSolverr.")

    return {
        "apeiron_version": __version__,
        "python_version": sys.version.split()[0],
        "packages": packages,
        "services": services,
        "recommendations": recommendations or ["All core diagnostics look usable."],
    }


def format_diagnostics(report: dict[str, Any]) -> str:
    lines = [
        f"Apeiron {report['apeiron_version']}",
        f"Python {report['python_version']}",
        "",
        "Packages:",
    ]
    for name, status in report["packages"].items():
        marker = "ok" if status["installed"] else "missing"
        version_text = f" ({status['version']})" if status["version"] else ""
        lines.append(f"  - {name}: {marker}{version_text}")
    lines.extend(["", "Services:"])
    for name, status in report["services"].items():
        if "installed" in status:
            marker = "ok" if status["installed"] else "missing"
            lines.append(f"  - {name}: {marker} - {status['hint']}")
        else:
            lines.append(f"  - {name}: {status['url']} - {status['hint']}")
    lines.extend(["", "Recommendations:"])
    lines.extend(f"  - {item}" for item in report["recommendations"])
    return "\n".join(lines)
