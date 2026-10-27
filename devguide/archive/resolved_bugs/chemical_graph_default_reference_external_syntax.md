---
summary: Chemical-graph readers reject external syntax for the default reference state.
issue: uibcdf/molsysmt#482
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [physchem, topology, selection]
guard: tests/topology/test_chemical_reference_selection.py::test_default_reference_external_selector_matches_intended_population
normative:
blocked_by: []
supersedes: []
---

# Chemical-graph readers reject external syntax for the default reference state.

**Reported:** 2026-10-26, native-only audit before aromatic addon receiving.
**Status:** Resolved in the native shared boundary; no consumer compensation.

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

See the [native audit receipt](../../../devtools/data/molsysviewer_tools_aromatic_native_audit_20261026.json).

## Resolution

The private shared atom selector now requires an explicit `reference_request`
flag. All 18 call sites in 13 consuming modules pass the original public request
semantics; the two ring-result callers do likewise. Numeric chemistry views
retain their selected-state reference; rich selectors receive the literal
reference sentinel only when that is what the caller requested. Explicit and
structure-associated requests keep their resolved state and existing restrictions.
This fixes aromaticity, ring recognition and related graph/site/preparation
consumers without weakening basic.select or adding consumer-side translations.
No scientific criterion, units, coordinates, attribution or producer version changes.

The before-fix selection module fails 80 cases and passes 18. A reserved pytest
parameter name in the first collection attempt is excluded; the later rotatable
output-key correction is test authoring, not a provider defect. The final 98
cases compare intended numeric populations across six public readers and native,
complementary and H5MSM sources, reference/None requests, empty matches, detached
arrays, whole-ring selection and a reference index 1 distinct from structure state
0. Unsupported explicit/associated external requests remain rejected.

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
