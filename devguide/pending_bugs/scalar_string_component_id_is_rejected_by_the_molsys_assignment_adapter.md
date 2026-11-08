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
