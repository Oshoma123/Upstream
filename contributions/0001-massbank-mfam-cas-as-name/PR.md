<!-- target: MassBank/MassBank-data  base: dev  head: Oshoma123:fix/mfam-cas-as-name -->
# mFam: replace CAS numbers used as compound names in three MC05 records

Three records in `mFam/` use the CAS registry number as the compound name, in
both `CH$NAME` and `RECORD_TITLE`:

| Record | Name now | Proposed name | CAS kept as |
|---|---|---|---|
| MSBNK-mFam-MC05_000155 | `1912-33-0` | Methyl indole-3-acetate | `CH$LINK: CAS 1912-33-0` |
| MSBNK-mFam-MC05_000015 | `1032-65-1` | 2'-Deoxycytidine 5'-monophosphate | `CH$LINK: CAS 1032-65-1` |
| MSBNK-mFam-MC05_000066 | `10366-91-3` | 2-(Glucopyranosyloxy)benzoic acid | `CH$LINK: CAS 10366-91-3` |

Each record already carries a full structure, so the names come from the
records' own `CH$SMILES` / `CH$IUPAC`. The CAS numbers are kept, moved to
`CH$LINK: CAS` and placed first per §2.2.8 (alphabetical by database name).
Nothing else changes: structures, peaks, metadata and stereochemistry are as
they were. Each file gains one line.

**Checks run**
- Each proposed name parsed with OPSIN 2.9.0 gives an InChIKey whose first
  block matches the record's `CH$LINK: INCHIKEY`. (The records carry no
  stereochemistry; that is unchanged.)
- All three CAS check digits are valid.
- MassBank Validator v1.3.0 passes on the patched files.

For MC05_000066, "Salicylic acid 2-O-glucoside" is the more familiar name. I
used the systematic form because it could be checked mechanically, and I'm
happy to switch if you prefer.

Found while auditing name fields in the 2026.03 release.

_Analysis and drafting were AI-assisted; I reviewed the changes and the checks above._
