import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ledger"))
from ledger import build, classify  # noqa: E402

T = [{"repo": "MassBank/MassBank-data", "community": "MassBank"},
     {"repo": "matchms/matchms", "community": "matchms"}]

def item(n, state, merged=None, pr=True):
    d = {"number": n, "title": f"t{n}", "html_url": f"u{n}", "state": state,
         "created_at": "2026-10-01T00:00:00Z"}
    if pr:
        d["pull_request"] = {"merged_at": merged}
    return d

FAKE = {
    "repo:MassBank/MassBank-data author:X": [item(1, "closed", "2026-10-05T00:00:00Z"),
                                             item(2, "open"), item(3, "closed")],
    "repo:matchms/matchms author:X": [item(4, "open", pr=False)],
}

def test_classify():
    assert classify(item(1, "closed", "2026-10-05T00:00:00Z")) == "merged"
    assert classify(item(2, "open")) == "open"
    assert classify(item(3, "closed")) == "closed"
    assert classify(item(4, "open", pr=False)) == "issue"

def test_n_counts_only_merged_prs():
    led = build("X", T, fetch=lambda q: FAKE.get(q, []))
    assert led["n_merged"] == 1            # only the merged PR
    assert led["n_open"] == 1 and led["n_closed_unmerged"] == 1
    assert led["n_issues"] == 1            # reported, never added to n
    assert led["merged_by_community"] == {"MassBank": 1}

def test_rejected_prs_are_reported_not_hidden():
    led = build("X", T, fetch=lambda q: FAKE.get(q, []))
    assert any(r["status"] == "closed" for r in led["contributions"])

def test_empty_ledger_is_zero_not_missing():
    led = build("X", T, fetch=lambda q: [])
    assert led["n_merged"] == 0 and led["contributions"] == []
