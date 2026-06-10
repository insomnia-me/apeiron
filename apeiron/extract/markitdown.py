from __future__ import annotations

import tempfile
from pathlib import Path


def extract_markitdown(file_path: str | Path) -> str:
    try:
        from markitdown import MarkItDown

        md = MarkItDown()
        result = md.convert(str(file_path))
        return result.text_content or ""
    except Exception:
        return ""


def extract_markitdown_from_bytes(content: bytes, suffix: str = ".pdf") -> str:
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(content)
            tmp = f.name
        text = extract_markitdown(tmp)
        Path(tmp).unlink(missing_ok=True)
        return text
    except Exception:
        return ""
