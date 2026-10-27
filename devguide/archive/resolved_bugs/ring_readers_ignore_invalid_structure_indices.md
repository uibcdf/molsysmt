---
summary: Ring readers silently accept invalid resident structure indices.
issue: uibcdf/molsysmt#483
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [physchem, topology, selection]
guard: tests/topology/test_ring_structure_scope.py::test_ring_readers_reject_invalid_structure_scope
normative:
blocked_by: []
supersedes: []
---

# Ring readers silently accept invalid resident structure indices.

**Reported:** 2026-10-26, native-only audit before aromatic addon receiving.
**Status:** Resolved in the native shared boundary; no consumer compensation.

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

See the [native audit receipt](../../../devtools/data/molsysviewer_tools_aromatic_native_audit_20261026.json).

## Resolution

The shared ring context now validates the original source structure scope before
detaching chemistry. It reuses the existing chemical-frame and common index
validators. Explicit lists require a known axis, including empty lists; `all`
or None permits native chemistry-only sources. Known empty structural axes
retain their ordinary empty-list behavior. External forms without a direct
count getter keep their existing native conversion route to obtain conformer
counts; native chemistry-only domains do not gain a fictitious axis by conversion.

The 50-case scope module initially fails 30 cases and passes 20 after correcting
partial-domain fixture ownership. Its controls cover both ring readers, native,
complementary and H5MSM inputs, negative/out-of-range indices, numeric/nonspatial
selections, repeated nonconsecutive lists, unknown structural axes and ambiguous
structure-state associations. H5MSM guards reject structural payload reads during
numeric chemical recognition. No new coordinates or per-structure occurrences
are computed.

## Local validation and lifecycle

The final combined focused modules pass 148 cases. The affected topology,
aromaticity/CIP/charge, hydrogen/halogen/hydrophobic/metal/water-interaction and
preparation regression passes 884 cases in 46.57 seconds with twelve workers
and pytest-receptor. One unrelated pre-existing sequence-alignment node needs
its public RCSB download; it passes separately with network access in 19.46
seconds, rather than counting a sandbox DNS failure as a molecular defect.
The first broad run exposed 15 external conformer-count compatibility failures;
the final helper retains that pre-existing conversion path and all pass.
The retained 35 warnings are expected legacy-H5MSM and deliberate memory-budget
controls; no warning is hidden.

The final public examples and affected docstrings, User Guide, Cookbook and four
course property modules reflect source-axis and state-selection semantics.
Seven notebook edits are prose-only and preserve all code, outputs and metadata.
The [shared receipt](../../../devtools/data/chemical_graph_selection_20261026.json)
retains source digests, commands, outcomes and limits. Local source evidence does
not qualify installed packages, all platforms, a full suite or a release.
