---
summary: MDTraj selection rejects valid group-free topologies with NAType.
issue: uibcdf/molsysmt#495
status: resolved
opened: 2026-10-27
closed: 2026-10-27
severity: medium
verification: measured
area: [form, select, mdtraj]
guard: tests/form/molsysmt_Topology/test_mdtraj_missing_hierarchy.py::test_group_free_external_selection_preserves_atom_correspondence
normative:
blocked_by: []
supersedes: []
---

# MDTraj selection rejects valid group-free topologies with NAType.

**Reported:** 2026-10-27, isolated while receiving the bound TPSA reader under
uibcdf/molsysviewer#264; independently reproduced without Viewer.
**Status:** Resolved and locally qualified. Native source hierarchy is unchanged;
external selectors use the owner adapter without consumer workarounds.

## What

A valid group-free native system converted from RDKit cannot be selected through MDTraj syntax. The numerically equivalent selection works. This is independently reproducible without MolSysViewer or TPSA.

```python
from rdkit import Chem
import molsysmt as msm
source = msm.convert(Chem.MolFromSmiles('CCO.COC'), to_form='molsysmt.MolSys')
msm.select(source, selection=[0])  # [0]
msm.select(source, selection='index 0', syntax='MDTraj')
# ArgumentError: ... list indices must be integers or slices, not NAType
```

Observed on source `c905d8ac753e98ec11959fac5ccbe049311d2068`, Python 3.14. The native molecule axis has two molecules after the #491 repair; missing groups remain intentional rather than a malformed atom graph.

## How

The MolSysMT Topology → MDTraj Topology converter builds MDTraj groups/chains from native hierarchy, then indexes its group list using each atom's missing group index (`pd.NA`). This fails before the requested external selector can run. Decide an explicit, loss-aware adapter policy for this input rather than repairing caller topology or translating selections in consumers.

## Why and acceptance

Group-free systems are valid inputs for native chemistry and molecule-level readers, including TPSA. The syntax parameter currently suggests external selection support but the adapter reports an internal NAType failure. Support an explicitly documented temporary hierarchy in the target adapter, or reject unsupported hierarchy with an actionable diagnostic. Preserve source atom order/chemistry and do not mutate or invent groups in the source. Add pytest guards for group-free and partially assigned hierarchy, empty/nonempty selections and a positive ordinary-hierarchy path.

Related: uibcdf/molsysmt#491; uibcdf/molsysmt#494 (separate builder insertion defect); uibcdf/molsysviewer#264.

Record: `devguide/archive/resolved_bugs/mdtraj_selection_rejects_group_free_topologies_with_natype.md`.


## What is measured and what is assumed

The pasted public-call reproductions execute on committed source c905d8ac7
(native code inherited from 97a8dc08c). Observations are reproduced; neither a
fix nor a general policy for all molecular hierarchies is established here.

## Scope and exclusions

Keep the native repair reusable and preserve source chemistry, molecule identity
and correspondence. This report does not change TPSA criteria or authorize a
consumer-specific reconstruction. The neighboring builder/selection issues are
separate themes, as are the previously closed #491/#493 repairs.

## Provenance

2026-10-27, Linux x86-64, Python 3.14, molsyssuite@uibcdf_3.14 development
interpreter, isolated source snapshot of c905d8ac7 with retained ABI3 backend.
No installed-package or cross-platform qualification is claimed.

## Adapter correction — 2026-10-27

The native Topology-to-MDTraj adapter now supplies missing hierarchy only in its
external target. Declared group/chain rows retain their order and labels. Missing
groups use UNL placeholders per known reference molecule and chain; atoms without
a known molecule receive separate placeholders. Missing chains use one fallback
chain. A partially assigned group's single known chain is used for its target
group; conflicting known chains or invalid parent indices raise clear errors.
The native hierarchy, chemical assignments and coordinates remain unchanged.

UNL was chosen deliberately: MDTraj classifies UNK as a protein group, which
would invent a biological classification for missing hierarchy. Metadata-based
selectors therefore operate on explicitly documented target data, while atom
indices retain correspondence with the source selection. Native subset extraction
keeps its existing sorted-order behavior; explicit permutation is performed
through the separate general permute_atoms tool, not hidden in this adapter.

Actual charge/bond preservation, partial hierarchy, empty/subset/permuted sources,
normal metadata, no-result selectors and downstream TPSA are contract-tested.
The existing bound TPSA consumer guard now requires a successful native result
instead of accepting the former ArgumentError as an alternative. This does not
change MDTraj or PyParsing dependency floors and is separate from #486's parser
version follow-up.

## Qualification closeout — 2026-10-27

The expanded local scope passes 2,404 tests with one explicitly retained strict
xfail for the separate open #499 defect (134.83 seconds). The final focused
source/builder controls pass 40 tests with that same one xfail. All 59 bound
TPSA receiving tests pass after requiring positive selector success; three
builder doctests and 496 notebook-schema controls pass. All 14 fast gates,
scoped Ruff, docstring and signature checks pass.

The new group-free hierarchy recipe executes in 12.3 seconds. Five existing
Tools/Form/course notebooks retain their code cells and saved outputs; their
legacy scenarios are not requalified by the prose-only additions. HTML exits
zero with 32 existing header/directive/orphan warnings under the #144 debt;
none comes from the new recipe. No warning-debt reduction, whole-suite,
installed-pair, cross-platform, benchmark or release qualification is claimed.
See the [dated receipt](../../../devtools/data/group_free_builder_mdtraj_20261027.json)
for commands, environment, source hashes and the explicit expected-failure scope.
