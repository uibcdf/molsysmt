---
summary: Scalar atom ID updates disagree with native string storage.
issue: uibcdf/molsysmt#383
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: medium
verification: reproduced
area: [basic, form, argdigest]
guard: tests/form/molsysmt_Topology/test_atom_id_updates.py
normative:
blocked_by: []
supersedes: []
---

# Scalar atom ID updates disagree with native string storage

**Reported:** ElastNetMT cache regression work, uibcdf/elastnetmt#27.
**Status:** Resolved. Scalar label updates now round-trip through the public API; closure evidence follows below.

## What

On a PDB-origin native MolSys, `msm.set(molsys, selection=[0], atom_id=101)`
passes digestion but raises a Pandas string-column assignment TypeError.
Using `atom_id='101'` instead raises an ArgumentError in digestion. Atom IDs
are labels stored as strings, independently of source atom indices.

## How

The `atom_id` value digester wraps a scalar integer in a list but rejects a
scalar string. The native Topology setter then assigns numeric values directly
to the string column. Correct scalar admission in digestion and normalize
identifiers at the native storage boundary, including trusted adapter calls.
Do not impose string storage on external forms with different representations.

## Why

Public molecular edits used by clients cannot update a single atom identifier.
Replacing an entire column with integers can also destroy the native string
invariant even when Pandas accepts the assignment.

## Evidence and scope

Reproduced on `a462b49c5566e8de993f83825576dc3860e9cfb1`, Linux, Python
3.14.7, using the bundled 181L PDB converted through the public API. Both scalar
failures were executed. This correction covers atom identifiers, not atom
indices or a redesign of all identifier setters. Query booleans and builder
semantics remain unchanged. Labels need not be numeric or unique.

## Acceptance criteria

Public MolSys/Topology get/set round trips accept scalar integer/string labels,
preserve lexical labels and normalize integer vectors without changing
unselected atoms. Full-column, subset and trusted adapter writes preserve
string storage. H5MSM 0.5 retains edited labels. Regression assertions must
check the actual public values and source atom indices.

## Resolution and verification — 2026-10-13

The digester now admits scalar strings alongside integers. The native setter normalizes numeric labels before assignment and retains a string column for complete writes, including trusted adapter calls. Integer/string scalars broadcast; aligned vectors preserve unselected atoms and lexical labels. No external form storage convention was changed.

Executed source verification on Linux/Python 3.14.7, Pandas 2.3.3: the 455-test combined regression scope passes with 12 workers and pytest-receptor, including form setters/getters, digestion, edits/invalidation, structure axes, mixed attribute delivery and strict API docstring rendering. A supplementary 18-case atom-ID module also covers final full-column scalar broadcasting. Public get/set doctests pass. The new lightweight recipe and new independent Toolbox/course sections execute with the development Python 3.14; unrelated legacy sections were preserved without reexecution. Foundations and the documentation manifest are updated. Sphinx HTML compilation succeeds with existing warning debt under uibcdf/molsysmt#144. Ruff, public docstring validation and the fast repository gates pass.

This corrects existing pre-1.0 contracts. No frozen artifact, tag, package coordinate or provider floor is changed. Exact replacement-candidate qualification remains owned by uibcdf/molsysmt#334.
