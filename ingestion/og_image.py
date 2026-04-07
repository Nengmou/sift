"""Lightweight og:image extractor — fetches just enough HTML to find the meta tag."""
import re

import httpx

# Only read the first 10KB — og:image is always in <head>
_MAX_BYTES = 10_240

_OG_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
    re.IGNORECASE,
)
# Also match the reversed attribute order: content before property
_OG_IMAGE_RE_ALT = re.compile(
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
    re.IGNORECASE,
)


async def fetch_og_image(
    client: httpx.AsyncClient, url: str, *, timeout: float = 5.0
) -> str | None:
    """Fetch the first ~10KB of *url* and extract the og:image URL.

    Returns None on any error (timeout, non-HTML, parse failure).
    """
    try:
        resp = await client.get(
            url, follow_redirects=True, timeout=timeout,
            headers={"Range": f"bytes=0-{_MAX_BYTES}"},
        )
        if "text/html" not in resp.headers.get("content-type", ""):
            return None
        html = resp.text[:_MAX_BYTES]
        match = _OG_IMAGE_RE.search(html) or _OG_IMAGE_RE_ALT.search(html)
        if match:
            return match.group(1).replace("&amp;", "&")
    except Exception:
        pass
    return None
