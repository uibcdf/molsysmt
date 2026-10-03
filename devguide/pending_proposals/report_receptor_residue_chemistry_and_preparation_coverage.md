---
summary: Report receptor residue chemistry and preparation coverage
issue: uibcdf/molsysmt#218
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [build, diagnostics]
guard:
normative:
blocked_by: []
supersedes: []
---

# Report receptor residue chemistry and preparation coverage

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open. Bounded receptor coverage is prioritized in the current
chemical-preparation sequence; implementation remains pending.

## What

Expose which receptor residues have been assessed against a chemical template and what is missing or inconsistent.

## How

Report template match, missing or unexpected heavy atoms and hydrogens, bond and protonation coverage, and an explicit unassessed status for unsupported residues. A parent-residue alias used for sequence normalization is not evidence that the modified residue has the parent's atom inventory.

## Why

Existing native heavy-atom and protonation paths process known amino-acid templates and can leave other residues unevaluated without a returned coverage report.

## What is measured and what is assumed

**Inspected:** Inspected molsysmt/build/get_missing_heavy_atoms.py and molsysmt/build/reconcile_protonation.py. Broad nonstandard-residue repair has not been validated.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Treating absence from a missing-atom list as proof of completeness was rejected because unsupported residues can be skipped.

## Scope and exclusions

Assessment and diagnostics first; repair algorithms for specific nonstandard residues and environment-dependent pKa remain separate.

## Acceptance criteria

- Every selected residue reports assessed, incomplete, or unassessed with a reason and supported template identity.
- Tests distinguish complete standard residues, incomplete residues, and unsupported nonstandard residues.
- The MSE fixture is assessed against selenium chemistry or marked unassessed; it is never reported as requiring MET sulfur. The same rule applies to modifications with additional atoms, such as SEP.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#177, uibcdf/molsysmt#227,
uibcdf/molsysmt#228, uibcdf/molsysmt#249.
Cross-component implementation links: uibcdf/dockingmt#4.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## Preparation work ordering — 2026-10-03

The maintainer requested chemical preparation alongside real SDF/PDBQT
validation. Follow [the maintained sequence](../roadmap.md) and the consumer
profile review in uibcdf/dockingmt#33. Related template and fixed-state H
capabilities are owned by uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Prioritization does not establish implementation, scientific coverage or a new
blanket 1.0 gate. Keep this issue's acceptance criteria and general-tool owner
distinct from format parsing and DockingMT protocol decisions.
