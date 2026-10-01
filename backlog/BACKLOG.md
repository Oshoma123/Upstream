# Contribution backlog

Status: `ready` = verified and drafted · `investigate` = finding needs
confirming before anything is drafted · `parked` = no candidate yet.

| # | Target | Candidate | Evidence | Status |
|---|---|---|---|---|
| 0001 | MassBank-data | 3 mFam records use a CAS number as the compound name | `contributions/0001-*`: OPSIN, CAS check digits, RDKit, Validator | **ready** |
| 0002 | MassBank-data | Records with a parseable SMILES but no `CH$LINK: INCHIKEY` (up to 927 in the 2026.03 NIST export) | Most no-InChIKey records are legitimately structure-less (putative IDs, wildcard SMILES). Needs checking per record in the source files, not the export; one sample (NILU "XYLENOL") also looks like a name/structure mismatch | investigate |
| 0003 | GNPS2 docs | The GNPS MGF export defines no InChIKey field, so it can't be joined to structures (SPECGAP v1.0.0) | Check whether current GNPS2 docs say so; if not, a documentation PR | investigate |
| 0004 | matchms | Name-field placeholders: CAS numbers, formulae, SMILES in the compound-name slot, resolved against the record's own structure | Compare with existing matchms filters (`clean_compound_name`, `derive_annotation_from_compound_name`) before proposing anything | investigate |
| 0005 | MsBackendMassbank | Handling of multi-name `CH$NAME` / comma-bearing systematic names | Speculative: needs a failing case first | investigate |
| 0006 | metabolights-utils | none yet | low activity (last push 2026-06) | parked |
