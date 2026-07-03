#!/usr/bin/env python3
"""Summarise the token spend and $ cost of the current Claude Code session.

Reads the session transcript JSONL (the per-turn token usage Claude Code writes
for free) and prints a compact token + $ report. The arithmetic happens here, in
plain Python — it costs no model tokens. This is a single agent, so there's just
the one session; the report shows what it cost to read files, think, and
self-check across the run.

Usage:
  python3 scripts/session-token-cost.py                 # newest transcript for this repo
  python3 scripts/session-token-cost.py --transcript X  # an explicit .jsonl path
  python3 scripts/session-token-cost.py --json          # machine-readable output

Note: excludes the final reporting turn(s) after this script runs; the undercount
is small.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

# Per-million-token USD pricing. Cache write = 1.25x input (5-minute TTL) or 2x
# input (1-hour TTL); cache read = 0.1x input. Update these if pricing changes.
PRICING = {  # model family -> (input, output) per MTok
    "fable":  (10.0, 50.0),
    "opus":   (5.0, 25.0),
    "sonnet": (3.0, 15.0),
    "haiku":  (1.0, 5.0),
}
CACHE_WRITE_5M = 1.25
CACHE_WRITE_1H = 2.0
CACHE_READ = 0.1


def family_for(model: str) -> str | None:
    m = (model or "").lower()
    for fam in PRICING:
        if fam in m:
            return fam
    return None


def default_transcript() -> str | None:
    slug = os.getcwd().replace("/", "-")
    base = os.path.expanduser(f"~/.claude/projects/{slug}")
    files = glob.glob(os.path.join(base, "*.jsonl"))
    if not files:
        files = glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    return max(files, key=os.path.getmtime) if files else None


def aggregate_usage(path: str) -> tuple[dict, set]:
    """Sum usage per exact model id, deduped by message id (one billed API
    response = one id), matching the built-in `/usage` figures."""
    latest: dict = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = obj.get("message") if isinstance(obj, dict) else None
            if not isinstance(msg, dict):
                continue
            usage = msg.get("usage")
            if not isinstance(usage, dict):
                continue
            key = msg.get("id") or obj.get("uuid") or len(latest)
            latest[key] = (msg.get("model", ""), usage)

    by_model: dict = {}
    unknown: set = set()
    for model, usage in latest.values():
        fam = family_for(model)
        if fam is None:
            if model:
                unknown.add(model)
            continue
        cc = usage.get("cache_creation") or {}
        row = by_model.setdefault(
            model,
            {"model": model, "family": fam, "input": 0, "output": 0,
             "cache_5m": 0, "cache_1h": 0, "cache_read": 0, "turns": 0},
        )
        row["turns"] += 1
        row["input"] += usage.get("input_tokens", 0) or 0
        row["output"] += usage.get("output_tokens", 0) or 0
        row["cache_read"] += usage.get("cache_read_input_tokens", 0) or 0
        row["cache_5m"] += cc.get("ephemeral_5m_input_tokens", 0) or 0
        row["cache_1h"] += cc.get("ephemeral_1h_input_tokens", 0) or 0
    return by_model, unknown


def tokens_in(row: dict) -> int:
    return row["input"] + row["output"] + row["cache_5m"] + row["cache_1h"] + row["cache_read"]


def cost_for(row: dict) -> float:
    in_rate, out_rate = PRICING[row["family"]]
    return (
        row["input"] * in_rate
        + row["output"] * out_rate
        + row["cache_5m"] * in_rate * CACHE_WRITE_5M
        + row["cache_1h"] * in_rate * CACHE_WRITE_1H
        + row["cache_read"] * in_rate * CACHE_READ
    ) / 1_000_000


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--transcript", help="Path to the session .jsonl")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    args = ap.parse_args()

    path = args.transcript or default_transcript()
    if not path or not os.path.exists(path):
        print("Token/cost report: no session transcript found.", file=sys.stderr)
        return 1

    by_model, unknown = aggregate_usage(path)
    models = sorted(by_model.values(), key=cost_for, reverse=True)
    total_tokens = sum(tokens_in(r) for r in models)
    total_cost = sum(cost_for(r) for r in models)

    if args.json:
        out = {
            "transcript": path,
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "models": [
                {
                    "model": r["model"],
                    "turns": r["turns"],
                    "input_tokens": r["input"],
                    "output_tokens": r["output"],
                    "cache_write_5m_tokens": r["cache_5m"],
                    "cache_write_1h_tokens": r["cache_1h"],
                    "cache_read_tokens": r["cache_read"],
                    "total_tokens": tokens_in(r),
                    "cost_usd": round(cost_for(r), 4),
                }
                for r in models
            ],
            "unknown_models": sorted(unknown),
        }
        print(json.dumps(out, indent=2))
        return 0

    print("**Session cost (token spend)**")
    print()
    print("| Model | In | Out | Cache write | Cache read | Total | Cost |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for r in models:
        print(
            f"| {r['model']} | {r['input']:,} | {r['output']:,} | "
            f"{r['cache_5m'] + r['cache_1h']:,} | {r['cache_read']:,} | "
            f"{tokens_in(r):,} | ${cost_for(r):,.2f} |"
        )
    print(f"| **Total** | | | | | **{total_tokens:,}** | **${total_cost:,.2f}** |")
    if unknown:
        print(f"\n_Unpriced model(s) skipped: {', '.join(sorted(unknown))}._")
    print("\n_Excludes the final reporting turn(s)._")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
