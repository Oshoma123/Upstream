"""Generate CITATION.cff from AUTHORS.json.

Zenodo's GitHub integration takes the DOI record's creators, ORCIDs and
affiliations from CITATION.cff. Generating it from the single author block
means the DOI record cannot disagree with the repository.
"""
import json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
VERSION, RELEASED = sys.argv[1], sys.argv[2]
ORCID = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")

def orcid_ok(o):
    if not ORCID.match(o): return False
    d = o.replace("-", ""); t = 0
    for ch in d[:-1]: t = (t + int(ch)) * 2
    r = (12 - t % 11) % 11
    return d[-1] == ("X" if r == 10 else str(r))

a = json.loads((R / "AUTHORS.json").read_text())["authors"]
for p in a:
    assert orcid_ok(p["orcid"]), f"bad ORCID for {p['name']}: {p['orcid']}"

q = lambda s: '"' + s.replace('"', '\\"') + '"'
L = ["cff-version: 1.2.0",
     'message: "If you use UPSTREAM, please cite it as below."',
     'title: "UPSTREAM: an evidence-led program of contribution to open-source metabolomics software"',
     "type: software", "authors:"]
for p in a:
    L += [f"  - family-names: {q(p['family'])}", f"    given-names: {q(p['given'])}",
          f"    orcid: \"https://orcid.org/{p['orcid']}\"", f"    affiliation: {q(p['affiliation'])}"]
L += [f'version: "{VERSION}"', f'date-released: "{RELEASED}"', "license: MIT",
      'repository-code: "https://github.com/Oshoma123/Upstream"',
      "keywords:"] + [f"  - {k}" for k in (
      "metabolomics", "mass spectrometry", "open source", "research software",
      "MassBank", "matchms", "GNPS", "Bioconductor", "MetaboLights")]
L += ["abstract: >",
      "  UPSTREAM is a program of contribution to the open-source software and",
      "  open data the metabolomics community depends on: matchms, the",
      "  RforMassSpectrometry Bioconductor packages, MassBank-data, the GNPS2",
      "  documentation and workflow repositories, and metabolights-utils. It",
      "  provides a ledger that counts merged contributions directly from GitHub,",
      "  a written protocol every contribution follows (evidence first, duplicate",
      "  check, upstream's own validation run locally, disclosed AI assistance),",
      "  and a backlog of evidence-backed candidates. At this version no",
      "  contribution has yet been filed: the ledger reads zero, and the first",
      "  contribution (three MassBank records using CAS numbers as compound names)",
      "  is verified and drafted but not submitted."]
(R / "CITATION.cff").write_text("\n".join(L) + "\n")
print("CITATION.cff written for", [p["name"] for p in a])
