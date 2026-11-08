---
summary: Scalar string component_id is rejected by the MolSys assignment adapter
issue: uibcdf/molsysmt#647
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: medium
verification: reproduced
area: [basic, argdigest]
guard: tests/basic/test_set_component_id.py::test_scalar_component_ids_use_the_chemical_owner_contract
normative:
blocked_by: []
supersedes: []
---

# Scalar component IDs through an owning MolSys

## What

The public MolSys setter rejects `component_id="changed"` for a selected component,
although the downstream ChemicalStates setter explicitly supports lexical scalar
labels and one-item vectors. IDs remain strings; this is a caller-route mismatch,
not a request to change index/ID semantics.

## Executed evidence

The original #646 comparison-control campaign on owner source `026437d16` reaches
eight failures at the label assignment, before comparison: native/H5MSM sources,
normal/pm-fs-coulomb policies and both requested comparison output formats.
The retained baseline has 34 failures and 20 passes; 26 failures reproduce #646,
while these eight identify this distinct setter route.
The process exits 1 under a 2 GiB memory cap, one CPU and zero swap; peak is
183,128,064 bytes. No full-library or consumer workflow acceptance is claimed.

```python
import molsysmt as msm
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=3, n_components=2)
msm.set(molsys, element="atom", component_index=[0, 0, 1])
msm.set(molsys, element="component", component_id=["101", "W"])
msm.set(molsys, element="component", selection=[1], component_id="changed")
# ArgumentError from the MolSys form setter's value digestion
```

The component_id digester recognizes basic.set and ChemicalStates/Dict setter
callers for assignment normalization, but omits the intervening MolSys form
setter caller. That caller falls through to the legacy integer/sequence branch.
This does not establish an ArgDigest provider defect.

## Intended outcome and acceptance

Receive the scalar path independently and align valid ID assignment through
MolSys with its stored chemical owner. Preserve lexical spelling, numeric-to-string
normalization, null/broadcast/selection semantics and source atomicity. Reject
Boolean IDs and test supported scalar/vector inputs through native chemical
owner forms under normal/nondefault unit policies. Comparison flags and strict
chemical matching remain separate. Do not skip digestion or change tables in a
consumer. No repair is implemented by this report.

## Independent baseline and repair

The dedicated 138-case public setter battery fails twenty cases and passes
118 controls on `ff03bf6bb`: scalar lexical/unit-like labels, None clearing
and empty-selection requests fail only through MolSys, for both atom and
component destinations and both unit policies. Standalone ChemicalStates and
ChemicalStatesDict controls already pass. All failures originate in the same
value-digestion caller omission; no test authoring error is included.

The local correction recognizes only the exact MolSys atom/component ID setter
callers in the existing assignment branch. Both reuse the canonical chemical
normalizer before trusted delegation; no second normalization algorithm, broad
caller bypass or selector/compare change is added. Existing ArgDigest/SMonitor
provide validation and structured errors. No new optional-engine, scientific
attribution, dependency or physical-unit operation is introduced. Prepared-source receiving passes 279 cases, including the 138 new setter controls, all 54 comparison controls, existing chemical-component/append tests and the updated MolSys component-setter doctest. The measured test peak is 248,209,408 bytes. Clean committed-source and fast-gate acceptance remain pending.

## Resolution — 2026-11-07

Qualified source `d020ff4a4e005c1e6076a9f417446685465fdf71` passes **279 clean-source cases**
with zero skips, failures or errors. This includes 138 new ID-assignment controls,
54 comparison controls, existing chemical-component/recovered-append tests and
the changed public MolSys component-setter doctest. All fourteen fast gates
and applicable whole-library/addon plus affected-test Ruff checks pass. Final
test peak is 248,082,432 bytes under one CPU, a 2 GiB process-tree cap and zero
swap; no OOM or resource interruption. No kernel, dependency, storage schema,
chemistry or comparison algorithm is changed.

The guard checks literal lexical/string storage, integer normalization, null
clearing, scalar broadcasting and both atom/component destinations through
MolSys, standalone ChemicalStates and ChemicalStatesDict. Related controls
verify selected order, empty selections, invalid values, unchanged unrelated
metadata/membership and normal/nondefault unit-policy authority. Restoring
the original caller restriction reproduces twenty refusals in this same battery.
There is no skipped-digestion workaround or duplicate normalization logic.

The [source receiving record](../../../devtools/data/component_id_assignment_receiving_647_20261107.json)
preserves original and final results, source hashes and resource bounds. Only
Markdown cells changed in the tutorial/course: code cells, saved outputs, IDs
and notebook metadata remain unchanged. Full notebook/HTML execution, complete
library/consumer workflow, installed/platform and release acceptance remain
separate. The experimental stored-H policy under #645 remains open.
