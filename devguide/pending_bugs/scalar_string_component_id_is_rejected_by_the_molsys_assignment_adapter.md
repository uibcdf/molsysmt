---
summary: Scalar string component_id is rejected by the MolSys assignment adapter
issue: uibcdf/molsysmt#647
status: active
opened: 2026-11-07
closed:
severity: medium
verification: reproduced
area: [basic, argdigest]
guard:
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
