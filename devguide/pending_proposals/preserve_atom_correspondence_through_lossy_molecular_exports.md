---
summary: Preserve atom correspondence through lossy molecular exports
issue: uibcdf/molsysmt#223
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Preserve atom correspondence through lossy molecular exports

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Return an explicit mapping between source and exported atoms when a molecular form omits or merges atoms.

## How

Define a post-conversion mapping artifact with retained, omitted, and merged source atoms, reasons, charge aggregation, and source state identity; keep the source MolSys unchanged. For the PDBQT example, the selected atom-typing policy, rather than atom names, determines which hydrogens are retained or merged.

## Why

PDBQT hydrogen conventions and returned docking poses require atom identity beyond a preflight conversion-fidelity report.

## What is measured and what is assumed

**Inspected:** Inspected molsysmt/basic/conversion_report.py and current PDBQT proposal; Meeko documents hydrogen merging by atom type.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Treating the existing preflight conversion report as the completed atom map was rejected because it does not record the resulting atom-level projection.

## Scope and exclusions

Reusable mapping contract and PDBQT exemplar; no universal atom matching between unrelated molecules.

## Acceptance criteria

- A loss-aware export yields a stable source-to-output and output-to-source mapping with reasons for omitted or merged atoms.
- Tests cover retained polar hydrogens, merged nonpolar hydrogens, charge aggregation, and unchanged source identity.
- Tests reject a name-based hydrogen projection when atom names and chemical types disagree.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#5, uibcdf/dockingmt#8.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
