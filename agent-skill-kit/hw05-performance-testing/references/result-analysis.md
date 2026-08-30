# JTL analysis and threshold derivation

## Required method

Analyze only a real CSV-format JTL and preserve it unchanged. First confirm column names and whether times are milliseconds. Split results by sampler label and report an overall row only when aggregation is meaningful.

Use `scripts/analyze_jtl.py <input.jtl> --output <analysis.json>` for a reproducible first pass. Cross-check at least one sample count, one error count, and p95 independently in JMeter or a second calculation.

Throughput is `completed samples / observation duration`; it is not concurrent users. Error rate is `failed samples / all samples * 100`. Percentiles must be computed from individual elapsed values, not averaged from subgroup percentiles. State the percentile interpolation method when exact reproduction matters.

## Finding the stress and soak thresholds

A stable stage must satisfy the student's declared criteria for the full observation window, for example:

- error rate <= 1%;
- p95 <= an explicitly justified target;
- throughput does not plateau while concurrency rises;
- CPU and memory do not remain saturated;
- no continuing memory growth or unrecovered latency after the spike.

The stress threshold is the highest stage that remains stable, not simply the stage with maximum RPS. The endurance threshold must come from a real 10-15 minute sustained run on the student's hardware and include stable RPS, p95/error rate, peak or ceiling memory, CPU behavior, and trend over time.

## Misinterpretation hunt

For every AI claim, create a four-column record: AI claim, raw evidence, verdict, correction. Typical traps include:

- treating p95 as the slowest request;
- using mean latency as a tail-latency guarantee;
- treating application errors as infrastructure saturation without checking response codes;
- comparing unlike workload windows;
- claiming a memory leak from one high endpoint instead of a sustained upward trend;
- deriving database causality from JTL alone;
- confusing latency, connect time, and elapsed time;
- calling the fastest run best despite failed assertions.

## Optimization judgement

Classify each recommendation as feasible, conditional, unsupported, or hallucinated. Link it to measured evidence and source architecture. For this SUT, SQLite WAL, indexes, serialization of writes, or batching may be plausible only after database contention/query evidence. A connection pool recommendation must account for the SQLite driver and actual access pattern. Do not claim it will help solely because it is a common web-performance suggestion.
