---
summary: MDTraj selection rejects valid group-free topologies with NAType.
issue: uibcdf/molsysmt#495
status: open
opened: 2026-10-27
closed:
severity: medium
verification: reproduced
area: [form, select, mdtraj]
guard:
normative:
blocked_by: []
supersedes: []
---

# MDTraj selection rejects valid group-free topologies with NAType.

**Reported:** 2026-10-27, isolated while receiving the bound TPSA reader under
uibcdf/molsysviewer#264; independently reproduced without Viewer.
**Status:** open; the scientific owner is responsible for correction and a native
pytest guard. The consumer adds no topology or selector workaround.

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

Record: `devguide/pending_bugs/mdtraj_selection_rejects_group_free_topologies_with_natype.md`.


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
