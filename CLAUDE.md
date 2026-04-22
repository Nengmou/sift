# Sift — Claude Code context

Sift is an AI-powered content discovery app for ML/AI practitioners. It surfaces authentic,
low-anxiety signal from curated sources and delivers a daily digest email.

## Dev setup

```bash
python3.13 -m venv .venv && source .venv/bin/activate
pip install uv
uv pip install --system -e ".[dev]"
cp .env.example .env   # fill in at minimum SECRET_KEY and DATABASE_URL
alembic upgrade head   # creates sift.db (SQLite) or migrates Postgres
uvicorn api.main:app --reload
```

Tests:
```bash
pytest tests/ -v
```

## Pipeline overview

```
ingest (scripts/ingest.py)
  └─ HN · RSS · Reddit · Twitter · YouTube
       └─ deduplicate → persist ContentItem (quality_score=NULL)

score (scripts/score.py)
  └─ LLM via OpenRouter (Gemini Flash) → quality/authenticity/calmness scores
       └─ fallback heuristics when OPENROUTER_API_KEY is absent

deliver (scripts/deliver.py)
  └─ per-user interest filtering → rank_items_for_user() → Resend email
```

Railway cron schedules (railway.toml):
- ingest: `0 */2 * * *` (every 2 h)
- score:  `30 */2 * * *` (every 2 h, 30 min after ingest)
- deliver: `*/15 * * * *` (every 15 min, matches per-user delivery_time windows)

## Key conventions

### `metadata_json` vs `"metadata"`
`ContentItem.metadata_json` is the Python attribute name; the DB column is `"metadata"`.
`metadata` is reserved by SQLAlchemy's Declarative API — never rename it back.

```python
# correct
item.metadata_json = {"why_this": "..."}
ContentItem(metadata_json={"subreddit": "MachineLearning"})
```

### SQLite / Postgres dual compatibility
`db/session.py` conditionally omits `pool_size`/`max_overflow` for SQLite and sets
`check_same_thread=False`. Use generic `JSON` (not `postgresql.JSON`) and `String(36)`
(not `postgresql.UUID`) in models. SQLite is the default for local dev; set `DATABASE_URL`
to a Postgres URL for staging/prod.

### Optional connectors
Twitter and YouTube connectors are only instantiated when the corresponding API key is
present (`settings.has_twitter`, `settings.has_youtube`). HN, RSS, and Reddit require no
keys. LLM scoring falls back to keyword heuristics when `OPENROUTER_API_KEY` is absent —
the app is fully functional without any paid API keys.

### Reddit uses httpx, not PRAW
`ingestion/reddit.py` calls the public JSON API directly (`https://www.reddit.com/r/{sub}/hot.json`).
PRAW is not a dependency — don't add it.

### YouTube fetches metadata only (no transcripts)
`ingestion/youtube.py` fetches video title and description via the Data API v3. Full transcript
ingestion (originally planned via yt-dlp) is not implemented. As a result, video content is
scored on description text only, which underrepresents depth. This is a known gap — if scoring
quality for YouTube videos needs improvement, transcript extraction is the lever.

### Deduplication
`scripts/ingest.py` deduplicates against the most recent 500 items using:
1. URL canonicalization (strips UTM and tracking params, sorts remaining query params)
2. Fuzzy title match (SequenceMatcher ≥ 0.97)

### Email dry-run
`DRY_RUN_EMAIL=true` (default) logs emails instead of sending. Set to `false` and add
`RESEND_API_KEY` for real sending. Magic links are printed to the server log in
`ENVIRONMENT=development`.

## Scoring philosophy

Three dimensions, all 0–1 floats (higher = better):
- **quality_score** — depth, originality, technical substance
- **authenticity_score** — personal practitioner voice vs. performative/PR content
- **calmness_score** — calm, grounded framing (1 = calmer; 0 = doom/hype)

**Do not** add engagement metrics (likes, views, shares) to scoring. The editorial bias is
toward authentic builders over pundits and engagement farmers.

### News vs. authentic: two paths

Each ingested item is tagged with `metadata_json["kind"]` = `"news"` or `"authentic"`.
First-party lab/corporate content is news; third-party practitioner content is authentic.
Classification rules live in `config/sources.py`:

- **YouTube**: `YOUTUBE_NEWS_CHANNEL_IDS_SET` (channel-based)
- **RSS**: `NEWS_RSS_FEED_URLS` (feed-URL-based)
- **Twitter**: `TWITTER_NEWS_ACCOUNTS_SET` (author-based)
- **HN / Reddit**: `kind_from_url()` against `NEWS_DOMAINS` — community aggregators
  classify items by their *destination URL host* (a link to openai.com surfaced by HN
  is still news).

Two-path composite rank (see `scoring/ranker.py:compute_rank`):
```
news:      score = relevance × (quality×0.6 + calmness×0.4)
authentic: score = relevance × (authenticity×0.5 + calmness×0.3 + quality×0.2)
```
News drops authenticity because a polished corporate release shouldn't be penalized on
a dimension that doesn't apply. Relevance is a multiplier derived from LLM
tag–to–interest matching (0–1); no-match items score 0 and fall out. For untagged
items, token overlap against interest labels is used as the relevance proxy.

### Delivery quota: 20% news / 80% authentic

`rank_items_for_user(items, user, target_size=N)` enforces a 20/80 split on the final
list. For the 5-item email digest that's 1 news + 4 authentic; for the 20-item web feed,
4 + 16. If one bucket is short, the other backfills. Callers that want the raw
diversity-capped list omit `target_size`.

Diversity caps enforce max 3 items per platform and max 2 per publisher in the final list.

## Source curation

All curated lists live in `config/sources.py` — edit there to add/remove sources without
touching ingestion logic. All YouTube entries should be `UC…` channel IDs (not `@handles`)
to avoid expensive Search API quota usage.

## Current milestone

All MVP features are code-complete. Outstanding before beta launch:
- Deploy to Railway and verify the pipeline runs against a live Postgres DB
- Manual ingest run → confirm content flows into DB → send a test digest email
- Onboard 20–50 beta users

## Alembic

```bash
alembic upgrade head                        # apply migrations
alembic revision --autogenerate -m "msg"    # generate new migration
```

`db/migrations/env.py` falls back to `settings.database_url` when `DATABASE_URL` env var
is absent, so migrations work in local dev without exporting the variable.
