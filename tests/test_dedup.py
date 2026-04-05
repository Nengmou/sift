from types import SimpleNamespace

from scripts.ingest import canonicalize_url, is_duplicate


def make_existing(url: str, title: str):
    return SimpleNamespace(url=url, title=title)


def test_canonicalize_strips_utm_params():
    url = "https://example.com/post?utm_source=x&utm_medium=y&id=42"

    assert canonicalize_url(url) == "https://example.com/post?id=42"


def test_is_duplicate_exact_url():
    existing = make_existing("https://example.com/post?id=42", "Any title")

    assert is_duplicate(
        "https://example.com/post?utm_source=x&id=42",
        "Different title",
        existing,
    )


def test_is_duplicate_fuzzy_title():
    existing = make_existing("https://example.com/a", "A practical guide to agents")

    assert is_duplicate(
        "https://example.com/b",
        "A practical guide to agents ",
        existing,
    )


def test_is_duplicate_different_url_and_title():
    existing = make_existing("https://example.com/a", "A practical guide to agents")

    assert not is_duplicate(
        "https://example.com/b",
        "Completely unrelated topic",
        existing,
    )
