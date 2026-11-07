---
summary: Topology extraction accepts invalid atom subsets as the complete source
issue: uibcdf/molsysmt#622
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [native, extract]
guard: tests/native/test_topology_operations.py::test_extract_rejects_invalid_atom_subsets_without_changing_source
normative:
blocked_by: []
supersedes: []
---

# Topology extraction accepts invalid atom subsets as the complete source

**Reported:** 2026-11-06, during MDTraj API-floor qualification for #524 under #334.
**Status:** Corrected and contract-tested in `35a0457f015a197d1daa65c5bc6fe1b4f7f9bf0c`;
public delivery and board closeout follow independent receiving.

## What

On source `0d0f2fe0b2e5e2ebc0551107b112c0b0790541a4`:

```python
from molsysmt.native import Topology

molsys = Topology(n_atoms=3)
for indices in ([0, 1, 3], [-1, 0, 1], [2, 0, 2]):
    result = molsys.extract(atom_indices=indices)
    print(result.n_atoms, result is molsys)
# 3 True, for all three invalid subsets
```

The duplicate full-length subset also passes a public conversion to
`mdtraj.Topology`, returning all three original atoms.

## How

`Topology.extract` in [topology.py](../../../molsysmt/native/topology.py) treats an
explicit list with length `n_atoms` as the full set without checking its values.
Shorter selections reach positional Pandas extraction, where negative positions
or duplicates can also be interpreted as valid inventory selections. The owner
must validate a flat unique in-range subset before its full-set shortcut or
hierarchy extraction. Keep the `all` shortcut and sorted subset order.

## Why

The returned stable inventory can silently disagree with the requested atom
domain. Native users and converters that delegate to Topology are affected.
Source aliasing makes the erroneous full-set result particularly misleading.
This is included data-integrity behavior, not an experimental detector.

## What is measured and what is assumed

The retained six-operation probe records three direct native successes on
invalid full-length lists. Two public conversions reject range violations;
the duplicate conversion returns the wrong full inventory. This is a bounded
counterexample, not evidence that every form accepts every invalid list.

## What was refuted

Repeating an atom is valid in an attribute query, but native extraction constructs
one new inventory axis. Existing ChemicalStates and partial MolSys extraction
already require unique atom positions. The initial MDTraj fixture incorrectly
assumed deduplication; it was corrected to a unique subset, with the original
failed run retained. That correction does not remove the independent invalid
full-length Topology counterexamples. No MDTraj compatibility shim or chemical
ownership change is needed.

## Scope and exclusions

Validate native Topology extraction and its public extraction/conversion
consumers. Preserve explicit full-set copy/alias behavior, ascending subset
order, empty subsets, hierarchy and string IDs. Do not change repeated attribute
queries, structure-index selections, permutation, or unrelated digesters.

## Acceptance criteria

- Full-length and partial duplicate, negative and out-of-range lists raise a
  catalog-backed ArgumentError before an inventory is returned or copied.
- Both copy modes and trusted delegation retain the domain requirement; source
  tables remain unchanged on rejection.
- Direct, form-agnostic native and native-to-MDTraj routes reject repetitions.
- Valid all/full/subset/empty extraction keeps copy, order and hierarchy contracts;
  direct attribute queries retain repetitions.
- Public docstrings, maintained guidance, User Guide and course explain the
  distinction; affected checks pass and public source is independently verified.

## Dependencies and risks

No new dependency or backend is needed. Validate in the native owner before the
length shortcut. Reuse its sorted array for uniqueness and hierarchy extraction,
rather than add another sort or hash-based store. This regression shares the
native-integrity milestone and adds no progress points to the audit plan.

## Provenance

Linux x86_64, existing development Python 3.14.7, 2026-11-06. The original ignored
receipt is `native-extraction-invalid-full-axis-probe.json` in the audit cache.
Maintained guards belong in
[test_topology_operations.py](../../../tests/native/test_topology_operations.py).

## Resolution and receiving

The native owner validates normalized integer shape, bounds and uniqueness
before its complete-axis shortcut. The same sorted array serves duplicate
detection and hierarchy extraction. The `all` path retains its original shortcut;
no lookup index, extra chemical store, provider shim or backend is introduced.
ArgDigest remains the public boundary and rejected domains use the existing
SMonitor ArgumentError. A malformed trusted array still fails at the data owner.

The original maintained counterexamples fail 27 cases while nine valid controls
pass. The final integrated profile passes **1,971 cases, zero failures or skips**,
with Pytest Receptor and twelve workers. It includes owner/extraction/conversion,
native addition, recovered append, chemical component extraction, public
doctests and documentation tests. The
[receiving receipt](../../../devtools/data/topology_extraction_receiving_622_20261106.json)
retains command scope, exit codes, hashes, original failures and authoring mistakes
separately; overlapping intermediate runs are not added to a unique-test total.

Its 563 warnings comprise 514 Sphinx deprecations, 31 intentional legacy-H5MSM
warnings, eight controlled attribute-drop warnings, six noninteractive plot
warnings and four unassessed side-chain warnings. No new extraction warning
is used instead of rejecting invalid inventory indices. Ruff lint and formatting
pass. Four human autosummary edits, the native backend and all changed notebook
code/outputs/IDs/metadata remain unchanged. This is source receiving, not an
installed package, platform matrix or final release qualification.
