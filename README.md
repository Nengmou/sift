# sift
In a world of noisy, performative social media, Sift surfaces authentic, practice-oriented, and anxiety-reducing content—so users can consume less stress and more substance.

## Local development

```bash
python3.13 -m venv .venv && source .venv/bin/activate
pip install uv
uv pip install --system -e ".[dev]"
cp .env.example .env       # fill in SECRET_KEY at minimum
alembic upgrade head       # creates sift.db
uvicorn api.main:app --reload
```

App runs at http://localhost:8000. Stop the server with `Ctrl+C`.

To run the pipeline manually:
```bash
python -m scripts.ingest   # fetch content from all sources
python -m scripts.score    # score unscored items via LLM (or heuristic fallback)
python -m scripts.deliver  # send digest emails (dry-run by default)
```

Tests:
```bash
pytest tests/ -v
```

## Deployment

Railway services are defined in [railway.toml](/Users/nengmou/Projects/sift/railway.toml):
- `web`
- `migrate`
- `ingest`
- `score`
- `deliver`

Production deploy sequence:
1. Deploy the latest code.
2. Run the `migrate` service first to apply `alembic upgrade head`.
3. Confirm the migration completed successfully.
4. Verify the `web` service is up and `GET /healthz` returns `200`.
5. After that, rely on the scheduled `ingest`, `score`, and `deliver` services.

Operational note:
- `migrate` is a one-shot service and is expected to exit after finishing successfully.
- `/livez` is liveness-only for Railway health checks.
- `/healthz` verifies database readiness.

Launch readiness checklist:
- [docs/launch-checklist.md](/Users/nengmou/Projects/sift/docs/launch-checklist.md)
