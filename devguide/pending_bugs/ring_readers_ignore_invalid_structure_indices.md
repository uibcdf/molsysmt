---
summary: Ring readers silently accept invalid resident structure indices.
issue: uibcdf/molsysmt#483
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [physchem, topology, selection]
guard:
normative:
blocked_by: []
supersedes: []
---

# Ring readers silently accept invalid resident structure indices.

**Reported:** 2026-10-26, native-only audit before aromatic addon receiving.
**Status:** Open; no scientific selector or index compensation in the consumer.

## What
Native `topology.get_rings` and `physchem.get_aromatic_rings` silently accept nonexistent structure indices on a resident molecular system when using the default reference state and non-spatial selection. The same source has one structure; index 999 is invalid. `physchem.get_aromaticity` rejects that request.

## How
```python
import molsysmt as msm
molsys = msm.convert(msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol'))
assert msm.get(molsys, n_structures=True) == 1
for reader in [msm.topology.get_rings, msm.physchem.get_aromatic_rings]:
    result = reader(molsys, structure_indices=[999])  # returns rings instead of rejecting
```
The resident chemical-graph/ring path passes the structure selection to an atom resolver that need not consume it. It does not invoke the explicit structure-axis validation used by the aromaticity calculator. Chemical recognition need not load coordinates, but an explicit index request should not silently ignore the known source axis.

## Why
This can conceal wrong caller indices/state scopes. The addon must forward scientific requests without silently discarding them (uibcdf/molsysmt#421; uibcdf/molsysviewer#264); validation belongs in the native reusable boundary.

## Acceptance criteria
Add native pytest coverage of negative/out-of-range explicit structure indices on both ring readers, including non-spatial all/numeric atom selections and applicable resident/file/partial forms. Preserve valid nonconsecutive/repeated selections, source index semantics, ambiguous structure-state rejection and coordinate-free chemical reading. Define the default/explicit-index behavior of sources without a structural axis; no consumer-only range checker or forced coordinate materialization.

## Provenance

Reproduced without Viewer on Linux/Python 3.14, isolated source 312a73200f5c578ba758618ec42179edb0228221, existing ABI3 backend f32ed73f7ef3cf3225e12fbc56b9c4236a4452d758c94661f41860ad00d82c1c. No native rebuild or installed qualification.

## What is measured and what is assumed

The complete-hierarchy caffeine control has one structure. A direct external
`all and all` selection returns all 24 atoms. The equivalent numeric chemical
queries succeed; rich external reader queries fail at the reference-state
boundary. Both ring readers accept [999] and [-1], whereas aromaticity rejects
them. These are native-only source observations, not installed qualification.

## What was refuted

The initial syntax draft used missing MDTraj hierarchy and an expression not
accepted by this installed parser. Those fixture problems are not evidence for
the state-boundary report. Its corrected opening example explicitly declares
group/chain membership and uses a directly verified boolean selector; no
statement about universal MDTraj operator compatibility is inferred.
The valid chemical memberships do not explain away ignored structure indices.

## Scope and exclusions

Do not prepare molecules, translate selectors, guess state indices or validate
scientific arguments differently inside the Viewer wrapper. Native shared
boundaries and their guards own the resolution; chemical-only reads should not
be forced to load whole trajectories or analyses.

See the [native audit receipt](../../devtools/data/molsysviewer_tools_aromatic_native_audit_20261026.json).
