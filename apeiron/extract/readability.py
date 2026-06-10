from __future__ import annotations


def extract_readability(html: str) -> str:
    try:
        from readability import Document

        doc = Document(html)
        content = doc.summary()
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.ignore_tables = False
        return h.handle(content)
    except Exception:
        return ""
