#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vinod Dhiman and UAGT contributors
"""Collect organic, third-party-sourced adoption metrics into /evidence/.

Design principle (section 7 + NFR5): every number must be (a) sourced from a third
party, (b) timestamped in UTC, and (c) reproducible — each record carries the source,
the exact endpoint queried, and the capture time. Organic only: no manufactured signals.

What it captures now (GitHub-native, reliably available):
  - stars, forks, watchers (subscribers), network, open issues   [REST API]
  - traffic: 14-day views/uniques and clones/uniques             [Traffic API*]
  - top referrers and paths (rolling 14-day)                     [Traffic API*]
  - per-release asset download counts                            [Releases API]
  * Traffic endpoints require push access; the GITHUB_TOKEN in CI provides it.
    The 14-day window means this MUST run at least biweekly or data is lost.

Stubbed for later (clear extension points below): Zenodo DOI stats, PyPI/npm
downloads, dependents/"used by", academic citations, web backlinks.

Outputs (append-only, committed so the trail is itself version-controlled):
  evidence/snapshots/<UTC>.json   full timestamped snapshot
  evidence/metrics.csv            cumulative flat history (one row per scalar signal)
  evidence/dashboard.html         rendered from metrics.csv

Usage:
  GITHUB_TOKEN=... python scripts/collect_metrics.py --repo owner/name
  python scripts/collect_metrics.py --dry-run          # no network; CI structure check
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVIDENCE = ROOT / "evidence"
API = "https://api.github.com"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gh_get(path: str, token: str):
    """GET a GitHub API path. Returns (data, error_message)."""
    req = urllib.request.Request(
        f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {token}",
            "User-Agent": "uagt-metrics",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} on {path}"
    except urllib.error.URLError as e:
        return None, f"network error on {path}: {e.reason}"


def record(signals: list, signal: str, value, source: str, endpoint: str, ts: str, extra=None):
    entry = {"signal": signal, "value": value, "source": source, "endpoint": endpoint, "timestamp_utc": ts}
    if extra is not None:
        entry["detail"] = extra
    signals.append(entry)


def collect_github(repo: str, token: str, ts: str) -> list:
    owner_repo = f"/repos/{repo}"
    signals: list = []

    meta, err = gh_get(owner_repo, token)
    if err:
        raise RuntimeError(f"could not read {repo}: {err}")
    for key, sig in [
        ("stargazers_count", "stars"),
        ("forks_count", "forks"),
        ("subscribers_count", "watchers"),
        ("network_count", "network"),
        ("open_issues_count", "open_issues"),
    ]:
        record(signals, sig, meta.get(key, 0), "GitHub REST API", owner_repo, ts)

    # Traffic (14-day rolling window; push access required).
    views, err = gh_get(f"{owner_repo}/traffic/views", token)
    if not err and views:
        record(signals, "views_14d", views.get("count", 0), "GitHub Traffic API", f"{owner_repo}/traffic/views", ts)
        record(signals, "views_unique_14d", views.get("uniques", 0), "GitHub Traffic API", f"{owner_repo}/traffic/views", ts)
    clones, err = gh_get(f"{owner_repo}/traffic/clones", token)
    if not err and clones:
        record(signals, "clones_14d", clones.get("count", 0), "GitHub Traffic API", f"{owner_repo}/traffic/clones", ts)
        record(signals, "clones_unique_14d", clones.get("uniques", 0), "GitHub Traffic API", f"{owner_repo}/traffic/clones", ts)
    refs, err = gh_get(f"{owner_repo}/traffic/popular/referrers", token)
    if not err and isinstance(refs, list):
        record(signals, "top_referrers", len(refs), "GitHub Traffic API",
               f"{owner_repo}/traffic/popular/referrers", ts, extra=refs)

    # Release asset downloads.
    releases, err = gh_get(f"{owner_repo}/releases", token)
    if not err and isinstance(releases, list):
        total = sum(a.get("download_count", 0) for r in releases for a in r.get("assets", []))
        record(signals, "release_downloads", total, "GitHub Releases API", f"{owner_repo}/releases", ts)

    return signals


def collect_zenodo(record_id: str | None, ts: str) -> list:
    """Zenodo record stats (views/downloads). Pass the concept record id to track all
    versions; the concept DOI 10.5281/zenodo.<id>. No auth required for public records."""
    if not record_id:
        return []
    endpoint = f"https://zenodo.org/api/records/{record_id}"
    req = urllib.request.Request(endpoint, headers={"Accept": "application/json", "User-Agent": "uagt-metrics"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            rec = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError):
        return []
    stats = rec.get("stats", {}) or {}
    signals: list = []
    for key, sig in [
        ("views", "zenodo_views"),
        ("unique_views", "zenodo_unique_views"),
        ("downloads", "zenodo_downloads"),
        ("unique_downloads", "zenodo_unique_downloads"),
    ]:
        if isinstance(stats.get(key), (int, float)):
            record(signals, sig, stats[key], "Zenodo stats", endpoint, ts)
    return signals


# --- Stubbed channels (wire these up at/after launch) -----------------------
def collect_pypi(package: str | None, ts: str) -> list:
    """TODO: pypistats / npm download counts — only if an installable helper is published."""
    return []


def write_snapshot(signals: list, repo: str, ts: str, evidence_dir: Path) -> Path:
    snap = {"captured_at_utc": ts, "repo": repo, "signals": signals}
    snap_dir = evidence_dir / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)
    path = snap_dir / f"{ts.replace(':', '').replace('-', '')}.json"
    path.write_text(json.dumps(snap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def append_csv(signals: list, repo: str, ts: str, evidence_dir: Path) -> Path:
    csv_path = evidence_dir / "metrics.csv"
    new = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["timestamp_utc", "repo", "signal", "value", "source"])
        for s in signals:
            if isinstance(s["value"], (int, float)):  # scalars only in the flat history
                w.writerow([ts, repo, s["signal"], s["value"], s["source"]])
    return csv_path


def render_dashboard(evidence_dir: Path) -> Path | None:
    csv_path = evidence_dir / "metrics.csv"
    if not csv_path.exists():
        return None
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    latest: dict[str, dict] = {}
    for r in rows:
        latest[r["signal"]] = r  # rows are append-ordered, so last wins
    cells = "".join(
        f"<tr><td>{r['signal']}</td><td>{r['value']}</td>"
        f"<td>{r['source']}</td><td>{r['timestamp_utc']}</td></tr>"
        for r in latest.values()
    )
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UAGT — Adoption Evidence</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:2rem;color:#1a1d21}}
table{{border-collapse:collapse}}td,th{{border-bottom:1px solid #d7dce2;padding:.4rem .7rem;text-align:left}}
.note{{color:#5b6470;font-size:.9rem;max-width:46rem}}</style></head><body>
<h1>UAGT adoption evidence</h1>
<p class="note">Latest value per signal. Every figure is third-party-sourced, UTC-timestamped,
and reproducible from <code>evidence/snapshots/</code> (organic only — see NFR5). History in
<code>evidence/metrics.csv</code>; {len(rows)} records, {len(latest)} signals.</p>
<table><thead><tr><th>Signal</th><th>Latest value</th><th>Source</th><th>As of (UTC)</th></tr></thead>
<tbody>{cells}</tbody></table>
</body></html>
"""
    out = evidence_dir / "dashboard.html"
    out.write_text(html, encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Collect organic adoption metrics into /evidence/.")
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"),
                    help="owner/name (defaults to $GITHUB_REPOSITORY)")
    ap.add_argument("--evidence-dir", default=str(DEFAULT_EVIDENCE))
    ap.add_argument("--dry-run", action="store_true", help="no network; verify structure only")
    args = ap.parse_args()

    evidence_dir = Path(args.evidence_dir)
    ts = utc_now()

    if args.dry_run:
        # Exercise the render path on whatever history exists; never call the network.
        render_dashboard(evidence_dir)
        print(f"dry-run OK (no network). evidence dir: {evidence_dir}")
        return 0

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("error: set GITHUB_TOKEN (needs repo scope; push access for traffic).", file=sys.stderr)
        return 1
    if not args.repo:
        print("error: --repo owner/name (or $GITHUB_REPOSITORY) is required.", file=sys.stderr)
        return 1

    signals = collect_github(args.repo, token, ts)
    signals += collect_zenodo(os.environ.get("ZENODO_RECORD_ID"), ts)
    signals += collect_pypi(os.environ.get("PYPI_PACKAGE"), ts)

    snap = write_snapshot(signals, args.repo, ts, evidence_dir)
    csv_path = append_csv(signals, args.repo, ts, evidence_dir)
    dash = render_dashboard(evidence_dir)

    scalars = {s["signal"]: s["value"] for s in signals if isinstance(s["value"], (int, float))}
    print(f"captured {len(signals)} signals @ {ts}")
    print("  " + ", ".join(f"{k}={v}" for k, v in scalars.items()))
    print(f"wrote {snap.relative_to(ROOT) if snap.is_relative_to(ROOT) else snap}")
    print(f"wrote {csv_path}")
    if dash:
        print(f"wrote {dash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
