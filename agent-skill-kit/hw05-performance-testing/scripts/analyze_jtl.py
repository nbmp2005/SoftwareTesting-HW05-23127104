#!/usr/bin/env python3
"""Summarize a CSV-format JMeter JTL without modifying the source file."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def percentile(values: list[float], percentile_value: float) -> float:
    """Return a linearly interpolated percentile (inclusive endpoints)."""
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile_value / 100.0
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    required = {"timeStamp", "elapsed", "label", "responseCode", "success"}
    if not rows:
        raise ValueError("JTL contains no samples")
    missing = required.difference(rows[0])
    if missing:
        raise ValueError(f"Missing required JTL columns: {', '.join(sorted(missing))}")

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["label"]].append(row)
    groups["__overall__"] = rows

    output: dict[str, object] = {}
    for label, samples in groups.items():
        elapsed = [float(sample["elapsed"]) for sample in samples]
        timestamps = [int(sample["timeStamp"]) for sample in samples]
        failures = sum(not parse_bool(sample["success"]) for sample in samples)
        start = min(timestamps)
        end = max(ts + int(float(sample["elapsed"])) for ts, sample in zip(timestamps, samples))
        duration_seconds = max((end - start) / 1000.0, 0.001)
        output[label] = {
            "samples": len(samples),
            "failures": failures,
            "error_rate_percent": round(failures * 100.0 / len(samples), 4),
            "throughput_samples_per_second": round(len(samples) / duration_seconds, 4),
            "duration_seconds": round(duration_seconds, 3),
            "elapsed_ms": {
                "mean": round(sum(elapsed) / len(elapsed), 3),
                "min": min(elapsed),
                "median": round(percentile(elapsed, 50), 3),
                "p90": round(percentile(elapsed, 90), 3),
                "p95": round(percentile(elapsed, 95), 3),
                "p99": round(percentile(elapsed, 99), 3),
                "max": max(elapsed),
            },
            "response_codes": dict(sorted(Counter(sample["responseCode"] for sample in samples).items())),
        }
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV-format JMeter .jtl file")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    result = summarize(rows)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
