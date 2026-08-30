---
name: hw05-performance-testing
description: Design, review, execute, analyze, and audit HW05 JMeter performance tests for the EShop API. Use for Load, Stress, Spike, soak testing, JTL analysis, evidence collection, and submission completeness; never fabricate execution evidence or measured values.
---

# HW05 Performance Testing

Produce a reproducible, evidence-backed HW05 result. Treat the assignment text and the checked-out SUT source as the authorities. Preserve the student's chosen workflow and tool unless it is incompatible with the SUT.

## Choose the operating mode

- For scenario design or JMeter review, read [references/test-design.md](references/test-design.md).
- For running tests, collecting evidence, recovering state, or naming artifacts, read [references/execution-evidence.md](references/execution-evidence.md).
- For JTL analysis, threshold derivation, and AI-misinterpretation review, read [references/result-analysis.md](references/result-analysis.md). Use `scripts/analyze_jtl.py` when a real CSV-format JTL is available.
- For report writing or final submission audit, read [references/report-submission.md](references/report-submission.md).
- Whenever generating or updating Markdown deliverables, also read [references/report-artifacts.md](references/report-artifacts.md). It defines the canonical files, source requirements, and safe incremental update protocol.

Read only the references needed for the requested mode. Read multiple references when the request spans modes.

## Invariants

1. Never invent a `.jtl`, screenshot, hardware specification, hostname, demo link, GitHub issue, commit hash, timestamp, RPS, percentile, memory ceiling, or test outcome.
2. Mark missing real-world evidence as `TODO (REAL EVIDENCE REQUIRED)` and tell the student how to obtain it.
3. Use one end-to-end workflow in all three plans and cover auth-heavy, read-heavy, and transactional endpoint groups.
4. Require CSV-driven inputs and unique mutation data. A 4xx/5xx caused by duplicate test data is not evidence of capacity failure.
5. Keep Load, Stress, and Spike workload shapes distinct. A listener/report type may appear in only one plan.
6. Separate functional defects, security/authorization defects, test-script defects, and performance failures in all analysis.
7. Report at least sample count, throughput, error rate, mean, median, p90, p95, p99, max, response-code distribution, and resource observations. Correlate client and server timestamps.
8. Determine thresholds from a stable baseline and real soak run; never present suggested starting values as measured limits.
9. Preserve raw artifacts. Analyze copies or read-only inputs and record commands/options used.
10. Require a human-review section that states what AI proposed, what the student verified, what changed, and why.
11. When asked to generate or update reports, update the smallest applicable canonical Markdown sections and the matching checklist/README summary. Do not overwrite templates or replace missing evidence with prose.

## EShop Workflow 5 facts verified from source

Default backend: `http://localhost:3000`.

Sequence:

1. `POST /api/login` with `email` and `password`; extract `token`.
2. `GET /api/admin/users` and `GET /api/coupons` with `Authorization: Bearer ${token}`.
3. `POST /api/categories`; extract category `id`.
4. Either `POST /api/products` with one product or `POST /api/admin/import-products` with `{ "products": [...] }`.
5. `POST /api/admin/coupons` with a globally unique `code`.

Current implementation caveats must be reported, not silently normalized:

- Some protected routes authenticate a JWT but do not enforce the admin role.
- `POST /api/products` currently lacks authentication middleware although the requirements say mutating product APIs require admin authorization.
- Coupon `code` is unique; reuse creates database errors unrelated to system capacity.
- Current login code increments failed attempts by 2 and locks for 180 seconds, while the requirements specify +1 and 30 seconds.

## Completion gate

Before declaring work complete, identify every missing real artifact, verify Markdown links, run the submission checker if present, and distinguish ready content from templates awaiting real results.
