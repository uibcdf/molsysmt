---
summary: Assign and validate AutoDock atom types under a named scheme
issue: uibcdf/molsysmt#222
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [build, attribute]
guard:
normative:
blocked_by: []
supersedes: []
---

# Assign and validate AutoDock atom types under a named scheme

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Provide chemically grounded AutoDock atom typing as an explicitly identified parameter scheme.

## How

Classify atoms using element, bonding, aromaticity and chemical context rather than names; validate full coverage and define how the scheme is stored alongside atom_ff_type.

## Why

PDBQT requires AutoDock types, while an unqualified atom_ff_type value does not identify its typing rules.

## What is measured and what is assumed

**Inspected:** Inspected native MolecularMechanics storage and DockingMT preparation. Meeko documents SMARTS-based AutoDock4 typing.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Inferring types from atom or residue names was rejected because names do not reliably encode chemical context.

## Scope and exclusions

Atom typing and scheme provenance; no partial-charge calculation or DockingMT scoring choice.

## Acceptance criteria

- Representative aromatic, donor, acceptor, halogen, and unsupported cases have explicit tested assignments or errors.
- Tests distinguish polar hydrogens that remain in the selected PDBQT profile from mergeable nonpolar hydrogens using chemical context rather than atom names.
- The selected scheme and its version are inspectable; PDBQT export can require compatible typing.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#5.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
