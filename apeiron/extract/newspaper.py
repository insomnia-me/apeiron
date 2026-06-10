from __future__ import annotations


def extract_newspaper(html: str, url: str = "") -> str:
    try:
        from newspaper import Article

        article = Article(url)
        article.set_html(html)
        article.parse()
        return article.text or ""
    except Exception:
        return ""
