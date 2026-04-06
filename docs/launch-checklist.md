# Launch Checklist

## 1. Deploy Infrastructure

1. Set all Railway env vars from [.env.example](/Users/nengmou/Projects/sift/.env.example).
2. Run the `migrate` service.
3. Confirm the `web` service is up.
4. Confirm:
   - `GET /livez` returns `200`
   - `GET /healthz` returns `200`

## 2. Validate Each Source Live

1. Run `ingest`.
2. Confirm fresh rows land in the database for:
   - `rss`
   - `reddit`
   - `hn`
   - `youtube`
   - `twitter` if X credentials and API tier support it
3. Inspect a raw sample from each source before evaluating scoring quality.

## 3. Validate Scoring and Ranking

1. Run `score`.
2. Confirm scored rows receive:
   - `quality_score`
   - `authenticity_score`
   - `anxiety_score`
3. Review a few users’ ranked feeds manually.
4. Confirm platform, publisher, and content-type caps improve diversity without collapsing feed length.

## 4. Validate Delivery Surfaces

1. Test signup.
2. Test magic-link login.
3. Test `/feed`.
4. Test `/settings`.
5. Send a real digest through Resend.
6. Check that `why this?` copy is useful in both web and email.

## 5. Validate Cron Behavior

1. Confirm Railway cron services run on schedule:
   - `ingest`
   - `score`
   - `deliver`
2. Verify `deliver` respects per-user delivery windows.

## 6. Validate X Specifically

1. Confirm your X API tier supports the current connector implementation.
2. If not, disable X for launch rather than allowing noisy failures.

## 7. Run a Beta Editorial Review Loop

1. Add 10–20 beta users.
2. Inspect what each user actually receives.
3. Identify recurring noise sources.
4. Tune source lists and ranking behavior before wider rollout.

## 8. Keep a Minimal Ops Runbook

Document:
- Railway deploy order
- how to rerun `migrate`
- how to trigger `ingest`, `score`, and `deliver`
- what to check if the feed is empty
- what to check if email delivery fails

## Exit Criteria

Launch-ready means:
- Railway deploy is stable
- migrations are reliable
- all intended sources ingest successfully
- recommendation quality is acceptable in manual review
- digest delivery works with real email
- a small beta cohort can use the product without obvious failures
