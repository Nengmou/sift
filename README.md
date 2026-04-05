# sift
In a world of noisy, performative social media, Sift surfaces authentic, practice-oriented, and anxiety-reducing content—so users can consume less stress and more substance.

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
