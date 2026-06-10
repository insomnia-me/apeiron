from __future__ import annotations


def extract_trafilatura(html: str, url: str = "") -> str:
    try:
        import trafilatura

        text = trafilatura.extract(
            html,
            url=url,
            include_comments=False,
            include_tables=True,
            include_images=False,
            include_links=True,
            output_format="markdown",
        )
        return text or ""
    except Exception:
        return ""
