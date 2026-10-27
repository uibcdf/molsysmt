---
summary: Chemical-graph readers reject external syntax for the default reference state.
issue: uibcdf/molsysmt#482
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

# Chemical-graph readers reject external syntax for the default reference state.

**Reported:** 2026-10-26, native-only audit before aromatic addon receiving.
**Status:** Open; no scientific selector or index compensation in the consumer.

## What
`physchem.get_aromatic_rings` and `physchem.get_aromaticity` reject a valid external MDTraj atom selector with their default reference chemical state. Direct `msm.select` and equivalent numeric reader queries work. This is related to uibcdf/molsysmt#480 but affects the reusable chemical-graph/ring selection helpers independently of the readiness assessor.

## How
```python
import molsysmt as msm
builder = msm.MolSysBuilder(msm.convert(msm.systems['caffeine']['caffeine.sdf']))
group = builder.add_group(list(range(builder.n_atoms)), group_name='CAF', group_id='1')
builder.add_chain([group], chain_id='A')
molsys = builder.build()
# Explicit setup supplies the hierarchy MDTraj requires and declared ring flags.
flags = msm.physchem.get_aromaticity(molsys)
msm.set(molsys, element='atom', atom_is_aromatic=flags['atom_is_aromatic'])
msm.set(molsys, element='bond', bond_is_aromatic=flags['bond_is_aromatic'])
indices = msm.select(molsys, selection='all and all', syntax='MDTraj')
assert len(indices) == 24
for reader in [msm.physchem.get_aromatic_rings, msm.physchem.get_aromaticity]:
    reader(molsys, selection=indices)  # succeeds
    reader(molsys, selection='all and all', syntax='MDTraj')  # ArgumentError: syntax
```
`topology._chemical_graph.select_chemical_atoms` and `topology._rings.ring_result` resolve the state to an integer and pass it to `basic.select`. The common selector rejects external string syntax with a non-reference state request even when the reader's user requested the default reference.

## Why
The expert addon mirrors public reader parameters and must preserve intended populations without translating selectors or silently changing state semantics. This blocks external-syntax receiving under uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Please review other callers of the shared helpers, including existing topology readers.

## Acceptance criteria
Native pytest should compare default-reference external syntax with the intended numeric population for both readers and affected shared-helper consumers; retain full-graph evaluation, sorted source indices, whole-ring selection and detached outputs. Cover reference/non-reference and structure-associated states, and keep unsupported external state semantics explicit. A fix must not weaken the common selector's state safety or add consumer-specific workarounds.

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
