---
summary: Enumerate ligand protomers under explicit protonation-site rules
issue: uibcdf/molsysmt#230
status: blocked
opened: 2026-09-22
closed:
verification: inspected
area: [build, attribute]
guard:
normative:
blocked_by: [uibcdf/molsysmt#220]
supersedes: []
---

# Enumerate ligand protomers under explicit protonation-site rules

**Reported:** 2026-09-22, during the MolSysMT–DockingMT chemical preparation review.
**Status:** Blocked post-1.0 proposal; the named dependency must be resolved first.

## What

Generate a bounded set of ligand protonation microstates from declared ionizable sites without claiming pH-dependent populations.

## How

Use an explicit named site-rule set or user-specified sites; alter formal charge and hydrogen inventory with parent-to-child heavy-atom mapping, deduplicate chemically equivalent states and record the rules used.

## Why

Protomers can change the atoms and charge of the ligand supplied to docking; state selection needs traceable alternatives rather than an implicit single guess.

## What is measured and what is assumed

**Evidence:** Inspected MolSysMT chemical-state storage and uibcdf/molsysmt#220; no public general protomer enumerator was identified. pKa prediction and microstate populations have not been validated.
**Assumed:** Scientific generality beyond the bounded fixtures is not established.

## What was refuted

A pH cutoff or implied population based only on site enumeration was rejected; prediction and ranking require a separately justified model.

## Scope and exclusions

Explicit-site protomer generation for simple acid/base fixtures after uibcdf/molsysmt#220; no pKa prediction, equilibrium weights, metal coordination or receptor residue protonation.

## Acceptance criteria

- Simple acid/base fixtures yield expected protonated and deprotonated states with correct formal charges, hydrogen counts, heavy-atom correspondence and provenance.
- Limits, unsupported or ambiguous sites, duplicate states and atom-inventory representation are defined and tested; no pH probability is reported without a model.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#220, uibcdf/dockingmt#4.

## Provenance

Source inspection on the local checkout `e9df1d1bd`, Python 3.13.14,
2026-09-22. No timing, pKa, or microstate-population measurement was made.
