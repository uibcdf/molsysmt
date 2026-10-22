---
summary: ViewerJSON atom extraction retains source bond endpoints
issue: uibcdf/molsysmt#399
status: open
opened: 2026-10-21
closed:
severity: medium
verification: reproduced
area: [form, extract, tests]
guard:
normative:
blocked_by: []
supersedes: []
---


# ViewerJSON atom extraction retains source bond endpoints

**Reported:** 2026-10-21 while reviewing the independent #397/#398 fixes.
**Status:** Open; the extraction adapter is unchanged.

## What

Extracting two atoms from a three-atom ViewerJSON retains both source bonds,
including an endpoint outside the new atom axis:

```python
import molsysmt as msm
from molsysmt.native import Topology
molsys = Topology(n_atoms=3)
molsys.add_bonds([[0, 1], [1, 2]])
payload = msm.convert(molsys, to_form="molsysmt.ViewerJSON")
subset = msm.extract(payload, selection=[1, 2])
assert subset.data["bonds"]["atom_pairs"] == [[0, 1], [1, 2]]
msm.convert(subset, to_form="molsysmt.Topology")
# StructuralInconsistencyError: Bonded atom indices must be between 0 and 1.
```

The intended surviving bond is source (1, 2), remapped to local (0, 1).

## How

`molsysmt/form/molsysmt_ViewerJSON/extract.py` slices atom columns and
coordinates, but copies the bonds block without filtering or endpoint remapping.
It also uses list(np.array(values)[idx]) for atom columns, which may retain
NumPy scalar types. The endpoint failure above is executed evidence; the scalar
risk is source inspection and requires a separately qualified labeled fixture.

## Why

A declared atom subset may carry unrelated bonds or out-of-range endpoints into
native reconstruction or rendering. This adapter is independent of MolSys
extraction and does not demonstrate a defect in native/H5MSM remapping.

## What is measured and what is assumed

**Reproduced:** the exact public example above on Linux/Python 3.14.7, after the
native exporter scalar fix. The subset has two atoms and still carries both
source pairs. Native conversion rejects the out-of-range endpoint.
No client rendering, installed-package or performance claim is made.

## What was refuted

This is not an ID-label interpretation error: the reported failing fields are
positional atom endpoints. The extractor source was not changed by #397/#398.

## Scope and exclusions

Own the atom-selection route and alignment of all bond columns/endpoints,
including legacy endpoint fields and JSON-safe selected atom columns.
Structure-list ordering and duplicate-selection policies must be inspected and
explicitly scoped during implementation; they are not qualified here.
No additional chemistry inference or viewer scene implementation is requested.

## Acceptance criteria

A public guard must check a subset that removes an incident bond and remaps a
retained bond, with aligned order/type columns and no mutation of the source.
Cover a reordered atom selection, zero bonds and standard JSON serialization
before native decoding. Define repeated atom-selection semantics explicitly.

## Provenance

Observed 2026-10-21 in the existing development environment, Linux/Python 3.14.7.
The extraction adapter matches main before the native ViewerJSON repairs.
