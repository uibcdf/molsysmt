---
summary: Amino-acid MET supplements reference an undeclared OXT atom
issue: uibcdf/molsysmt#380
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: low
verification: reproduced
area: [data]
guard: tests/data/databases/test_amino_acid_supplement_revision.py
normative:
blocked_by: []
supersedes: []
---

# MET supplemental connectivity contained an undeclared atom

**Reported:** 2026-10-10, validation of restored generators under uibcdf/molsysmt#368.
**Status:** Resolved; owning JSON and the affected bundled bucket are regenerated.

## What

Both MET variants in the amino-acid `extra.json` contained the bond C–OXT, but
neither 19-atom inventory included OXT. The bundled MET record retained those
variants at positions 4 and 5. Supplying the supplement to the restored CCD
generator raised `ValueError: Group MET: each bond must join two declared atoms.`
The existing reader filtered absent endpoints, so the defect did not demonstrate
a runtime exception; it did prevent valid regeneration and stored inconsistent
reference graphs.

## How

The graph was already inconsistent in the supplement, not introduced by parsing
or serialization. Commit ff79047645f8d57ccda6da48ddf39a3d70488974 copied a
second naming variant that retained the dangling bond. Structural validation
exposed the problem while repairing uibcdf/molsysmt#368.

## Why

Reference data must have declared endpoints and a reviewed chemical meaning.
Silently inventing OXT or accepting the inconsistent source would make a
maintenance route unable to preserve its stated contract.

## Scientific review and decision

The declared inventories and the remaining graph correspond to an N-terminal
MET group in a peptide: three hydrogens on N, the methionine side chain, and one
backbone oxygen. The NMET atom inventory and 18 intra-group bonds in
[AmberClassic aminont12.lib](https://github.com/Amber-MD/AmberClassic/blob/656e5c6fcb05149e6aa936e1d69d1426b37ea3c7/dat/leap/lib/aminont12.lib#L2133)
match the first supplement exactly after removal of C–OXT. The second is the
same graph with H1 named H. No force-field charges or atom types are adopted.

As a second inspected reference, ParmEd's amber03 RTP NMET variant has the same
heavy-atom/terminal graph with another hydrogen naming convention and an explicit
C–+N inter-group bond. Its checkout is
9fa8b08b760f57d45a271854ffa4a17f3f2647c0; AmberClassic's checkout is
656e5c6fcb05149e6aa936e1d69d1426b37ea3c7. The general
[wwPDB annotation guidance](https://cdn.rcsb.org/wwpdb/docs/documentation/annotation/wwPDB-B-2025Mar-V4.5.pdf)
describes OXT as a leaving atom in peptide linkage; this does not make OXT absent
from every possible MET inventory.

Decision: retain the declared inventories and remove the two undeclared edges.
Adding OXT would change terminal chemistry and template membership. The existing
CCD variants with OXT are preserved. This repair neither declares a chemical
state nor adds a new terminal preparation policy.

## Resolution and reproducibility

The owning JSON loses exactly two C–OXT entries. A shared deterministic pickle
writer and `molsysmt/data/_make/revise_amino_acid_supplements.py` regenerate only
buckets affected by reviewed before/after supplements. Exact original-variant
matching rejects wrong or ambiguous baselines. Group keys, metadata, variant
counts/positions and unrelated records are preserved. Validation finishes before
output creation, and nonempty destinations are refused.

Only `M.pkl.gz` is replaced. It contains MET alone; its name and four previous
variants are identical to the original record, and variants 4/5 preserve their
atom inventories. Every other bucket and the group-name index is unchanged.
The completion receipt `molsysmt/data/databases/amino_acids/supplement_revision_manifest.json`
records original/revised input hashes, output hash, changed indices, actual
source-code hashes and reported runtime versions. The maintained
[generation guide](../../chemical_group_database_generation.md#revising-an-existing-amino-acid-supplement)
provides reproduction commands from the immutable original inputs.

## What is measured and what is assumed

Before repair, the focused six-case graph/reader selection had **3 failures and
3 passes**: the endpoint guard and two independent graph checks failed; the reader
and OXT-bearing variants already worked. After correction:

```bash
python -m pytest tests/data/databases tests/element/group/amino_acid tests/element/group/test_get_bonded_atom_pairs.py --receptor=llm -n12
```

**72 passes**, Linux/Python 3.14.7, mmcif 1.1.1, 2026-10-10. The guard asserts the
independent reference graph, source/bucket agreement, all supplemental endpoint
inventories, actual CCD regeneration with the full supplement, preserved OXT
variants and reader results with reversed names/nonconsecutive external indices.
Revision tests cover unrelated records, preserved source bytes, deterministic
output/input hashes, missing/ambiguous originals, invalid graphs, prohibited
membership/metadata/count changes and caller-owned destinations.

Changed Python files pass Ruff checks/formatting; the fast release gate passes
**14/14**. The AST signature comparison also passes against the pre-#368
baseline, with only its two documented maintenance-helper retirements waived.

This is source contract testing and reference-graph comparison, not a complete
chemical-state assignment or full-CCD scientific audit. The producer's runtime
version in this development environment reports an older build; source hashes
and original input commit identify the actual maintenance code and inputs.

## What was refuted

- Removing validation would reproduce the invalid graph.
- Adding OXT would alter a valid N-terminal peptide inventory.
- Regenerating the entire corpus would risk unrelated historical CCD/RTP variants
  without being necessary to remove two dangling edges.
- The previous runtime reader's filtering did not make the stored graph valid.

## Scope and exclusions

Two invalid supplemental edges and their exact bundled copies are corrected.
No groups, atom names, coordinates, hydrogen inventories, charges, bond orders,
chemical states, public runtime APIs or release-candidate identities change.
The revision tool accepts trusted maintenance pickles, not untrusted user files;
its whole-directory writes are not atomic transactions.

## Acceptance criteria

All criteria are met: reviewed chemistry, owning-source correction, bounded
reproducible asset replacement, explicit preserved scope, source and reader
guards. The guard fails on the original data and on a future dangling endpoint.

## Provenance

Source/input baseline: 4393d9fdc0d09a0312b8b8218514444f1278a25d.
Original M bucket SHA-256: 6492829b3ba05eb48ee938fd26fe66728ec7b6d34fe2a4d3e30e75f61f9cee41.
Corrected M bucket SHA-256: b1120d738a8a0b526cdd8382a526aed25d55a484ce529c73124b66b4b0ad1cd1.
Linux/Python 3.14.7, mmcif 1.1.1; review and tests on 2026-10-10.
