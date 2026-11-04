---
summary: Reference bond helpers reject documented NumPy atom-name arrays.
issue: uibcdf/molsysmt#550
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: reproduced
area: [build, argdigest, tests]
guard: tests/element/group/test_template_atom_name_containers.py
normative:
blocked_by: []
supersedes: []
---

# Reference template atom-name containers

**Reported:** MolSysViewer's PR #543 native intake, independently reproduced
on main d9255c85c. **Correction:** source ee3f303c2cca86163120151bac92200890b8f8de
normalizes the three documented flat name containers. Receiving merge
aa1527bc26b5c065c4c97f65de99fbe168f7f826 retains that fix and the independently
qualified metadata candidate fbb09782c3f66735762bd4a507314db692927f97.

## What and how

Saccharide, small-molecule and terminal-capping reference helpers call
`atom_names.index(...)`. A NumPy array has no such method. For NAG C1/C2/C3,
ATP PG/O1G/O2G and ACE CH3/C/O, both the family helper and general dispatcher
succeed with lists/tuples and raise AttributeError with documented NumPy inputs.
Nonflat inputs also produce accidental TypeError/InternalAlgorithmError or an
empty result rather than consistent input validation.

## Why

Callers already holding native name arrays cannot use the declared interface.
A Viewer-only conversion would hide the provider defect. The stored reference
connectivity and successful list results are not demonstrated to be incorrect.

## Correction

A small private flat-name normalizer in the existing ArgDigest argument owner
accepts one-dimensional lists, tuples and arrays of strings and returns an
independent list. The three legacy public helpers call it after their existing
unknown-group check, keeping their signatures and family lookup behavior.
The general dispatcher delegates unchanged. No new public utility, competing
chemical store or dataset is introduced; the generic nested-name digester and
other family helpers retain their existing behavior.

Valid names retain their order and first-occurrence duplicate behavior; explicit
index maps are neither selected nor renumbered. Read-only/strided names and maps
are not modified. Invalid dimensions or non-string name entries raise the
existing public ArgumentError with a flat-sequence diagnostic. Known empty
inputs remain empty; unknown/unmatched small molecules remain empty, while
saccharide/cap lookup errors retain their existing diagnostics. General mapping
validation and the other helpers' complete return contracts remain under #548.

## Receiving

- Original selection: 66 failures and 81 passes. Thirty-six failures are the
  NumPy lookup AttributeError; remaining cases expose malformed-name handling.
- The corrected 147-case matrix passes without omissions or warnings. It covers
  both entry paths, three containers, default/nonconsecutive index mappings,
  row ordering, first duplicates, empty names, readonly/strided inputs and
  documented invalid/unknown outcomes, using literal independent bond controls.
- Wider group/template, build and private-digester receiving plus three changed
  module doctests passes 846 cases without omissions, 54.70 seconds. Its five
  warnings are legacy H5MSM reads.
- A bounded old/new list-compatibility probe passes 96 cases across NAG, ATP,
  ACE, NME, NHE and NH2 reference variants, reversed atom order, explicit/default
  maps and both sorting modes. That is compatibility, not new chemical validation.
  The probe supplies the same read-only reference dictionary to both paths in a
  private process to avoid repeated shard decoding; production loading is unchanged.

The initial unbounded catalogue sweep was stopped (exit 143) when repeated
shard deserialization was identified. It is not a successful or complete
catalogue assessment. The independent future optimization is tracked in #553;
no cache or shared mutable dictionary is introduced in this repair.

Docstrings, the existing group tutorial, Foundations, recipe and Module 03 are
updated. Existing notebook code/outputs/IDs/metadata are preserved. The explicit
three-family return documentation also addresses part of #548; it does not close
that separate seven-helper contract review. Final documentation receiving passes 568 cases without omissions, 44.91
seconds. Its 529 warnings are 514 Sphinx/MyST deprecations, eight legacy H5MSM
reads, six headless-plot notices and one intentional attribute-drop control.
The first documentation run had one real-target fixture failure (567 passes):
the miniature API build needed the existing group tutorial in its real-source
anchor list. The warning assertion remains strict; no fake target is added.
Ruff, developer-guide/index checks and all 14 fast gates pass.
The [receiving receipt](../../../devtools/data/template_bond_array_receiving_550_20261104.json)
retains inputs, warnings, successful scopes and unsuccessful probes.

## Provenance and scope

Linux x86_64, shared Python 3.14.7, NumPy 2.4.6, two workers and published Pytest
Receptor 1.2.1. The shared compiled backend and bundled data stay unchanged.
Raw evidence is in `.pytest_cache/template-bond-contracts-548-550/`.
No new algorithm, coordinate calculation, physical-unit policy, scientific
attribution boundary, dependency floor, topology inference or publication is
introduced. Compiled acceleration is not needed for this flat-input boundary.

## Resolution and combined receiving — 2026-11-04

The isolated correction and frozen metadata extensions merge without conflicts.
On receiving source aa1527bc2, all 2,938 group/addon/inventory/integration cases
pass without omissions (344.10 seconds). The 1,615 warnings comprise 1,608 legacy
H5MSM reads, four intentional attribute-drop controls, two unregistered-invalid-
keyword diagnostics and one invalid-determinant control. The separate combined
documentation and three module-doctest selection passes 568 cases without
omissions (42.93 seconds), retaining the same 529 disclosed warnings as the
initial isolated receiving. All 14 fast gates and whole-tree Ruff checks pass.

The guard exercises literal expected mapped bonds through both public routes,
including readonly/strided NumPy inputs. Reintroducing a direct ndarray.index
lookup fails the positive array cases; accepting malformed name dimensions
fails the explicit ArgumentError cases. It protects the reported mechanism
rather than merely recognizing a return type or matching help text.

The [combined receiving receipt](../../../devtools/data/template_bond_array_main_receiving_550_20261104.json)
retains exact source, JUnit hashes and warning counts. The registered metadata
matrix qualifies fbb09782c, not this subsequent native repair; final release
and installed-pair qualification retain their separate exact-source gates.
#548's remaining four helper contracts and #549's naming review stay open.
