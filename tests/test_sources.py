from config.sources import (
    NEWS_DOMAINS,
    NEWS_RSS_FEED_URLS,
    RSS_FEEDS,
    TWITTER_NEWS_ACCOUNTS_SET,
    YOUTUBE_AUTHENTIC_CHANNEL_IDS,
    YOUTUBE_CHANNEL_IDS,
    YOUTUBE_NEWS_CHANNEL_IDS,
    YOUTUBE_NEWS_CHANNEL_IDS_SET,
    kind_from_url,
)


def test_youtube_news_and_authentic_are_disjoint():
    assert set(YOUTUBE_NEWS_CHANNEL_IDS).isdisjoint(YOUTUBE_AUTHENTIC_CHANNEL_IDS)


def test_youtube_channel_ids_is_union_with_no_dupes():
    assert len(YOUTUBE_CHANNEL_IDS) == len(set(YOUTUBE_CHANNEL_IDS))
    assert set(YOUTUBE_CHANNEL_IDS) == (
        set(YOUTUBE_NEWS_CHANNEL_IDS) | set(YOUTUBE_AUTHENTIC_CHANNEL_IDS)
    )


def test_youtube_news_set_matches_list():
    assert YOUTUBE_NEWS_CHANNEL_IDS_SET == frozenset(YOUTUBE_NEWS_CHANNEL_IDS)


def test_news_rss_feeds_are_registered_in_rss_feeds():
    missing = NEWS_RSS_FEED_URLS - set(RSS_FEEDS)
    assert not missing, f"NEWS_RSS_FEED_URLS not in RSS_FEEDS: {missing}"


def test_kind_from_url_classifies_news_domain():
    for host in ("openai.com", "www.anthropic.com", "deepmind.google"):
        assert kind_from_url(f"https://{host}/some/path") == "news"


def test_kind_from_url_classifies_non_news_domain():
    assert kind_from_url("https://simonwillison.net/2026/04/post") == "authentic"
    assert kind_from_url("https://news.ycombinator.com/item?id=123") == "authentic"


def test_kind_from_url_handles_empty_url():
    assert kind_from_url(None) == "authentic"
    assert kind_from_url("") == "authentic"


def test_news_domains_cover_news_rss_hosts():
    """Every domain we treat as news via RSS should also classify as news via URL."""
    from urllib.parse import urlsplit
    for feed_url in NEWS_RSS_FEED_URLS:
        host = urlsplit(feed_url).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        assert host in NEWS_DOMAINS, f"{host} missing from NEWS_DOMAINS"


def test_twitter_news_accounts_is_frozenset():
    assert isinstance(TWITTER_NEWS_ACCOUNTS_SET, frozenset)
    assert "OpenAI" in TWITTER_NEWS_ACCOUNTS_SET
    assert "karpathy" not in TWITTER_NEWS_ACCOUNTS_SET
