---
summary: Define small-molecule chemical-state enumeration with atom correspondence
issue: uibcdf/molsysmt#220
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

# Define small-molecule chemical-state enumeration with atom correspondence

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Specify a reusable contract for enumerating ligand tautomers, protomers, and stereochemical states with explicit identity.

## How

Define separate selectable operations and provenance for each transformation, including how atoms and bonds correspond when hydrogen counts or bond orders change. Specify whether states with different atom inventories can share one MolSys or must be separate MolSys objects linked by an explicit map. Validate the contract on representative ligands before implementation breadth is promised.

## Why

Docking can require distinct input states, but those states should remain general molecular-system objects with traceable relationships.

## What is measured and what is assumed

**Inspected:** The existing chemical-state model was inspected; no public general enumerator or representative validation set was identified.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

One opaque combined enumeration operation was rejected because conformers, protomers, tautomers, and stereoisomers have different identity changes.

## Scope and exclusions

Contract and representative operations; no exhaustive microstate prediction, pKa accuracy claim, or DockingMT selection policy.

## Acceptance criteria

- The public contract distinguishes each state dimension and records parent-to-child atom correspondence or an explicit failure to map.
- Representative examples define duplicate handling, stereochemical ambiguity, and state provenance; follow-on implementation scope is explicit.
- The representation of added, removed, or relocated hydrogen atoms is defined without inventing stable atom IDs where no one-to-one correspondence exists.

## Dependencies and risks

Related implementation work: uibcdf/molsysmt#229 for tautomer and stereoisomer enumeration, and uibcdf/molsysmt#230 for protomer enumeration. Conformer generation remains separate in uibcdf/molsysmt#219.
Cross-component implementation links: uibcdf/dockingmt#4.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
