from __future__ import annotations


def test_doctor_reports_core_environment():
    from apeiron.doctor import collect_diagnostics

    report = collect_diagnostics()

    assert report["apeiron_version"]
    assert report["python_version"]
    assert "httpx" in report["packages"]
    assert "docker" in report["services"]
    assert report["recommendations"]
