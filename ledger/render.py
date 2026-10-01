"""Rewrite the README status block from ledger/ledger.json (the stats-file rule)."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parents[1]
L = json.loads((R / "ledger/ledger.json").read_text())
block = (f"<!-- ledger:start -->\n**n = {L['n_merged']} merged contributions** "
         f"· {L['n_open']} open · {L['n_closed_unmerged']} closed without merge "
         f"· {L['n_issues']} issues opened  \n"
         f"_Computed from GitHub by `ledger/ledger.py` at {L['generated']}._\n<!-- ledger:end -->")
p = R / "README.md"; t = p.read_text()
p.write_text(re.sub(r"<!-- ledger:start -->.*?<!-- ledger:end -->", block, t, flags=re.S))
print(block)
