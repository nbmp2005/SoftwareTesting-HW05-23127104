# Test design

## Model the business transaction

Use transaction controllers so the report distinguishes login, reads, and each mutation. The same ordered workflow must appear in Load, Stress, and Spike plans:

`login -> users -> coupons -> create category -> create/import product -> create coupon`

Extract the JWT with JSONPath `$.token` and category ID with `$.id`. Send `Content-Type: application/json` and `Authorization: Bearer ${token}` after login. Prefer one CSV row per virtual user with `Recycle on EOF = false` and `Stop thread on EOF = true` when enough rows exist.

Generate unique values without making results irreproducible. Combine CSV fields such as `run_id`, `vu_seed`, and `row_seed`; JMeter's thread number or timestamp may be appended. Record the actual run ID. Coupon codes should use uppercase alphanumerics and remain unique across reruns.

Minimum assertions per request:

- HTTP response code matches the endpoint's actual success contract (currently often `200`, not assumed `201`).
- Login JSON contains a non-empty token.
- Category/product/coupon creation JSON contains an ID or the documented success marker.
- Response duration assertion is used only as an explicit service-level objective, not as proof of correctness.
- Optional JSON structure assertions confirm expected fields and prevent a fast error page from being counted as success.

## Starting workload profiles

These are calibration seeds, not measured thresholds:

| Scenario | Suggested starting shape | Purpose |
| --- | --- | --- |
| Load | 20 VUs, 120 s ramp-up, 8 min steady, 60 s ramp-down | Validate expected traffic under stable concurrency |
| Stress | 10 -> 20 -> 40 -> 60 VUs, 2 min per stage, then recovery | Find the first sustained breach and saturation point |
| Spike | 10 VUs baseline, jump to 80 in <=10 s for 60 s, return to 10 for 2 min | Observe burst impact and recovery |
| Soak | Start below the last stable stress stage, sustain 10-15 min | Establish stability, leak trend, and hardware-specific ceiling |

Calibrate after a smoke test and hardware observation. Reduce values if localhost saturates immediately; increase stages if no bottleneck appears. Document every revision.

## Report-view allocation

Use a distinct type in each plan. A safe mapping is:

- Load: Summary Report.
- Stress: Aggregate Report.
- Spike: View Results Tree for a small/debug run only; disable it for the full high-load run and preserve an equivalent distinct report artifact or explicitly document the limitation.

GUI listeners consume memory and distort high-load results. Execute actual load non-GUI and generate HTML from JTL. If the course requires the named listener to exist in the plan, keep it disabled during measurement and show it only during smoke/debug evidence.

## Human review checklist

- All three plans use the identical endpoint sequence.
- CSV columns exactly match variable references.
- Each mutation is unique and uses the category ID created by that iteration.
- No test intentionally submits wrong admin passwords under concurrent load.
- Assertions reject error JSON and wrong response codes.
- Timers represent admin behavior; mutation operations should normally have modest think time, not zero-delay loops unless the purpose is explicitly stress.
- JTL saves timestamps, elapsed time, label, response code/message, success, bytes, sent bytes, latency, connect time, and thread counts.
- Setup, test, and teardown data behavior is explicit.
