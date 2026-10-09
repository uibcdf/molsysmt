---
summary: Empty bonded-to operands break valid selections and hydrogen-bond roles
issue: uibcdf/molsysmt#355
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: high
verification: reproduced
area: [selection, basic, api]
guard: tests/basic/select/test_empty_bonded_to.py::test_hydrogen_free_protein_roles_and_buch_keep_explicit_empty_coverage
normative:
blocked_by: []
supersedes: []
---

# Empty bonded-to operands break valid selections

**Reported:** 2026-10-09 by MolSysViewer during uibcdf/molsysviewer#186.
**Status:** Resolved; empty connectivity operands and hydrogen-free role calculation succeed.

## What

The general MolSysMT selector concatenates neighbor arrays even when the right
operand matches no atoms. Valid expressions such as `all bonded to atom_type=='H'`
therefore raise an ArgumentError wrapping `ValueError: need at least one array
to concatenate` on a hydrogen-free model. Hydrogen-bond acceptor exclusions and
donor inclusion rules consume this general tool, so Buch role assignment fails
before an explicit empty scientific result can be produced.

The original 1TCD protein has 3,983 atoms and no explicit H. Reproduce with
`msv.demo['1TCD']` and `view.interactions.hbonds.get_buch_hbonds(name='no-hydrogens',
structure_indices='all')`, then close the view. The native bundled TcTIM H5MSM
provides an offline provider regression with the same atom/hydrogen inventory.

## How

`basic.selector.molsysmt.select_bonded_to` obtains the right operand's neighbor
lists, then calls `np.concatenate` without checking outer emptiness. Treat that
list as an empty integer neighbor set and use the existing intersection/set
subtraction logic. Strip the operand boundaries before delegating so the valid
`all` operand remains recognized rather than queried as a pandas column.

This fixes the reusable selector. Neither detector-specific catches nor implicit
hydrogen preparation are needed. Scientific criteria, thresholds and units stay
unchanged. Missing/ambiguous chemistry continues to use its existing diagnostics.

## Why

No matching atoms is a legitimate selection outcome. `bonded to` an empty set
is empty; `not bonded to` it retains the left side. Native role assignment must
respect that distinction and preserve evaluated-empty evidence when donor-H
pairs are absent, without implying an H reconstruction or biological absence.

## Evidence and refuted assumptions

After correcting the initial test's mistaken assumption that public `select`
returns an ndarray (it returns an index list), twelve controls fail on original
source: seven on empty-neighbor concatenation, five because a whitespace-delimited
`all` operand is parsed as a column. Tests cover Topology/MolSys, empty operands
on both sides, logical composition, present isolated atoms and the real protein.

The correction preserves public index-list output, so an empty selection does
not require a new dtype contract. Roles and optional `Interactions` retain their
existing typed-array contracts. The real-protein role oracle is independent
attribute membership arithmetic, excluding GLN NE2 without running the selector
being tested. Source atom tables and coordinates must remain unchanged.

## Acceptance

- Valid positive/negative connectivity queries follow empty-set semantics.
- Empty left operands and present atoms without neighbors also remain valid.
- Ordinary `all` operands and nested logical composition are recognized.
- The exact 1TCD Viewer Python path succeeds with zero observations.
- Roles and explicit empty analysis retain shape, examined scope and structure
  coverage; a named H5MSM round trip retains that coverage without reconstructing H.
- Public selection and both existing hydrogen-bond method regressions pass.
- Docstrings, Foundations, Toolbox, Cookbook and course explain empty evidence.

## Provenance and scope

Linux, shared Python 3.14.7 development environment, original source after the
independent #356 addition correction (`b3ceb1177`), preserved Rust extension.
The Viewer checkout is independently modified; it is preserved and only exercised
as a Python source consumer. This is not browser/session, installed-pair or
replacement-candidate qualification. The publication pause remains in force.

## Resolution — 2026-10-09

The selector now obtains the valid empty neighbor set instead of concatenating
an empty sequence; operand-boundary whitespace is normalized before delegation.
Existing intersection/subtraction logic supplies the result. No hbond-specific
catch, atom creation, coordinate editing or scientific-method change is added.

`python -m pytest tests/basic/select tests/interactions/hbonds tests/hbonds
--receptor=llm -n12`: **213 passed**, including all twelve new regressions.
The real-protein guard checks an independent acceptor-membership oracle, typed
empty donor pairs/triples, examined atom scope, evaluated structure coverage,
named H5MSM persistence and unchanged atom tables/coordinates. It fails at role
identification if the original selector defect returns.

The exact public consumer reproduction also succeeds:
`view = molsysviewer.demo['1TCD']`,
`view.interactions.hbonds.get_buch_hbonds(name='no-hydrogens', structure_indices='all')`,
then `view.close()`. The stored named result has zero occurrences and structure
0 explicitly evaluated. This is source-level Python evidence only; no browser
runtime or installed replacement file is qualified by it.

Docstrings, Foundations, selection Toolbox, H-bond Cookbook and Common Core
Module 7 explain empty matches and explicit-H evidence. Notebook code/output
cells are unchanged.

`python -m pytest molsysmt/basic/select.py
molsysmt/interactions/hbonds/get_acceptor_atoms.py
molsysmt/interactions/hbonds/get_donor_atoms.py
molsysmt/interactions/hbonds/get_buch_hbonds.py --doctest-modules
--receptor=llm -n12`: **3 passed**, including the new empty-selection example.
Repository-wide `ruff check .` and `ruff format --check .` pass.
`python devtools/scripts/release_gate.py` passes **14/14 fast gates** on the
combined #355/#356 source, including developer-guide, dependency/source-route,
course (156 notebooks), resource, citation, Rust hot-path and public-API checks.
These checks do not execute or waive paused replacement-artifact gates.
