# Report and submission

## Required report chain

The report must let a reviewer trace:

`requirement -> workload design -> final JMX/CSV -> execution evidence -> raw JTL -> computed metric -> conclusion -> human review`

Include scope and endpoint mapping, environment/hardware, data strategy, plan tables, execution notes, three distinct report views, results, stress/soak threshold, defects/issues, AI analysis and corrections, optimization feasibility, continuous-testing proposal with flow chart and trade-offs, video/repository links, and limitations.

The AI critique must be 200-300 words and discuss a real error/omission, why AI missed it, the student's correction with raw evidence, and a learned collaboration principle. Do not finalize it before real JTL analysis exists.

## Continuous performance testing

Propose a commit watcher with path/risk filtering. Run a cheap baseline on relevant backend/database changes, compare p95 against a versioned baseline under equivalent hardware/workload, flag statistically or practically meaningful regressions, retain artifacts, and require human triage. Discuss compute cost, noisy shared runners, warm-up, baseline drift, flaky networks, false alarms, and the risk of skipping changes.

## Final audit

- Markdown and PDF main report exist.
- Three correctly named JMX files, three complete JTL files, and three HTML folders exist.
- CSV data files and exact run parameters exist.
- Resource/hardware screenshots show the required information and hostname.
- Demo is unlisted, >=6 minutes total, Vietnamese narration, same-frame tool/resource monitor, and includes skill demonstration.
- AI critique and audit report exist in Markdown and PDF.
- Git commit log is exported to a text file after the required incremental commits.
- README contains self-assessment and summary.
- GitHub Issues include only genuine observed issues with evidence.
- ZIP uses `23127104_HW05_AI_Performance_NNN.zip`, with NNN in 000-100.

Report missing items as blockers; do not mark placeholders as complete.
