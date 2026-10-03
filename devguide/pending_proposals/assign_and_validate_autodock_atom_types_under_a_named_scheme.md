---
summary: Assign and validate AutoDock atom types under a named scheme
issue: uibcdf/molsysmt#222
status: partial
opened: 2026-09-22
closed:
verification: reproduced
area: [build, attribute]
guard:
normative:
blocked_by: []
supersedes: []
---

# Assign and validate AutoDock atom types under a named scheme

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Partial. Explicit label decoding and bounded writer validation
are implemented; chemical assignment and an inspectable named-scheme contract
are prioritized in the current preparation sequence and remain pending.

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



## Explicit label decoding checkpoint — 2026-10-03

`molsysmt.element.atom.get_atom_type_from_atom_ff_type` decodes an existing
label or one-dimensional label collection under `typing_scheme='autodock4'`.
Standard labels map to chemical element symbols, independently of atom names.
Custom, macrocycle glue and hydrated-ligand pseudoatom labels fail explicitly.
An empty collection still requires a supported named scheme. Tests are in
`tests/element/atom/test_get_atom_type_from_atom_ff_type.py` and the public
contract is documented in the atom-type tutorial and Master course.

A shared private scalar primitive supplies both the public value tool and
PDBQT parsing/writing. The PDBQT writer requires the scheme declaration and
checks each label against the stored chemical element. It performs no new
assignment, aromaticity perception or donor/acceptor classification. AutoDock
labels remain separate atom_ff_type assignments; no competing chemical store
or placeholder scheme attribute was introduced. General scheme provenance in
native storage and chemically justified label assignment remain outstanding.

## Preparation work ordering — 2026-10-03

The maintainer requested chemical preparation alongside real SDF/PDBQT
validation. Follow [the maintained sequence](../roadmap.md) and the consumer
profile review in uibcdf/dockingmt#33. Related template and fixed-state H
capabilities are owned by uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Prioritization does not establish implementation, scientific coverage or a new
blanket 1.0 gate. Keep this issue's acceptance criteria and general-tool owner
distinct from format parsing and DockingMT protocol decisions.
