from __future__ import annotations

from apeiron.types import SearchHit, Source


async def search_reddit(query: str, max_results: int = 5) -> list[SearchHit]:
    """Search Reddit via its JSON API.
    
    Note: Reddit blocks most automated requests in 2026.
    To use this, you need to:
    1. Register an app at https://www.reddit.com/prefs/apps
    2. Set up OAuth with your credentials
    For now returns empty list.
    """
    _ = query
    _ = max_results
    return []
