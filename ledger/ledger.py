"""Compute the UPSTREAM contribution ledger from GitHub.

n is never typed. It is counted here, from the GitHub API, at run time, and
every document that quotes it interpolates ledger/ledger.json.

Definitions (stated because each changes the number):
  merged      a pull request authored by the contributor and merged by an
              upstream maintainer into a target repository. THIS is n.
  open        an authored PR awaiting review.
  closed      an authored PR closed without merge. Reported, never hidden:
              a ledger that only shows successes is not a ledger.
  issues      issues authored in target repositories, reported separately
              and never added to n.

Usage:  python ledger/ledger.py [--author LOGIN] [--out ledger/ledger.json]
GITHUB_TOKEN is used if set (higher rate limit); not required.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com/search/issues"
ROOT = Path(__file__).resolve().parents[1]


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "upstream-ledger"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def search(query: str) -> list[dict]:
    items, page = [], 1
    while True:
        url = f"{API}?q={urllib.parse.quote(query)}&per_page=100&page={page}"
        data = _get(url)
        items += data.get("items", [])
        if len(items) >= data.get("total_count", 0) or not data.get("items"):
            return items
        page += 1
        time.sleep(2)


def classify(item: dict) -> str:
    pr = item.get("pull_request")
    if pr is None:
        return "issue"
    if pr.get("merged_at"):
        return "merged"
    return "open" if item["state"] == "open" else "closed"


def build(author: str, targets: list[dict], fetch=search) -> dict:
    rows = []
    for t in targets:
        for it in fetch(f"repo:{t['repo']} author:{author}"):
            rows.append({
                "repo": t["repo"], "community": t["community"],
                "number": it["number"], "title": it["title"], "url": it["html_url"],
                "status": classify(it), "opened": it["created_at"][:10],
                "merged": ((it.get("pull_request") or {}).get("merged_at") or "")[:10] or None,
            })
        time.sleep(2)
    rows.sort(key=lambda r: (r["opened"], r["repo"], r["number"]))
    count = lambda s: sum(r["status"] == s for r in rows)
    by_comm = {}
    for r in rows:
        if r["status"] == "merged":
            by_comm[r["community"]] = by_comm.get(r["community"], 0) + 1
    return {
        "author": author,
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "n_merged": count("merged"), "n_open": count("open"),
        "n_closed_unmerged": count("closed"), "n_issues": count("issue"),
        "merged_by_community": by_comm,
        "n_repos_with_merge": len({r["repo"] for r in rows if r["status"] == "merged"}),
        "contributions": rows,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--author", default=json.load(open(ROOT / "ledger/config.json"))["github_login"])
    ap.add_argument("--out", default=str(ROOT / "ledger/ledger.json"))
    a = ap.parse_args()
    targets = json.load(open(ROOT / "targets.json"))["targets"]
    led = build(a.author, targets)
    Path(a.out).write_text(json.dumps(led, indent=2) + "\n")
    print(f"{a.author}: merged={led['n_merged']} open={led['n_open']} "
          f"closed-unmerged={led['n_closed_unmerged']} issues={led['n_issues']}")


if __name__ == "__main__":
    main()
