---
summary: Align SMARTS and bound-feature fixtures with inherited molecule boundaries.
issue: uibcdf/molsysmt#500
status: open
opened: 2026-10-27
closed:
severity: medium
verification: reproduced
area: [tests, topology, addons]
guard:
normative:
blocked_by: []
supersedes: []
---

# Align SMARTS and bound-feature fixtures with inherited molecule boundaries

**Reported:** 2026-10-27, while receiving the bound molecular descriptors under
uibcdf/molsysviewer#264. Opened with the principal maintainer's authorization.
**Status:** open; two fixture factories are being adapted without changing science.

## What

The #494 hierarchy repair correctly rejects a new group spanning multiple inherited source molecules, but two older test factories still declare that invalid hierarchy:

- `tests/topology/get_substructure_matches/test_reference_selections.py::declared_system`
- `tests/molsysviewer_molsysmt/test_feature_sites_tools.py::feature_system`

They put all atoms of disconnected multi-molecule RDKit sources in one LIG group. Scientific readers are never reached.

## Evidence

Owner source `3781031d0c1d08f34b2aa966ad0b82bf3b64a31d`, CI smoke [40571118517](https://github.com/uibcdf/molsysmt/actions/runs/40571118517): native step reports 6 failed, 123 setup errors, 2,678 passed, 4 optional skips. Both failure groups end at `MolSysBuilder.add_group` with `A group cannot span multiple inherited source molecules`. The addon step is not reached. The analogous bound-feature factory has the same all-atoms group construction.

```python
from rdkit import Chem
import molsysmt as msm
source = msm.convert(Chem.MolFromSmiles('CCC.CCl.C=O'))
builder = msm.MolSysBuilder(source)
builder.add_group(list(range(builder.n_atoms)), group_name='LIG')
# StructuralInconsistencyError: ... multiple inherited source molecules.
```

## Proposed correction and acceptance

Respect the actual inherited molecule axis when declaring fixture groups: get each molecule's source atom membership through the public MolSysMT query and add a LIG group for each. Retain the existing atom order, names, chemistry, coordinates, chain label and scientific selection/matching assertions. Assert that molecule counts and membership remain unchanged. Do not relax #494, merge source molecules, translate selectors in the addon or weaken the scientific assertions.

Receive both focused files and the applicable hosted source gate. Preserve the original failed run and earlier qualification identities. The separate populated-state atom insertion defect #499 is outside this fixture correction.

Related: uibcdf/molsysmt#494, uibcdf/molsysmt#495, uibcdf/molsysviewer#264.

Record: `devguide/pending_bugs/align_smarts_and_bound_feature_fixtures_with_inherited_molecule_boundaries.md`.


## What is measured and what is assumed

The original owner CI on 3781031d0 reports six failures and 123 setup errors
in one native file; both groups have the same invalid cross-molecule group
construction. The affected bound-feature factory uses the same construction.
The native builder rejection agrees with its documented preserved-identity
contract. Updating test hierarchy does not justify changes to readers, model
parameters or expected matching/selection populations.

## Scope and exclusions

Only these two fixture factories change. Groups follow public source molecule
membership queries, keeping the existing atom order, names, chemistry,
coordinates and chain label. Assertions guard molecule counts/memberships and
all existing scientific expectations remain. No consumer workaround or model
change is introduced. Native #499 and GUI/installed qualification are separate.

## Acceptance criteria

Both focused files and affected descriptor readers pass. The regression gate on
the corrected source must execute the originally blocked native and bound tiers.
Keep the original failed run as non-success evidence; close with the actual
source and guard after qualification.

## Provenance

Original CI: Linux/Python 3.14, 3781031d0, run 40571118517. Directed local work
uses molsyssuite@uibcdf_3.14, a frozen committed source snapshot and retained ABI3
backend. No installed-package or cross-platform qualification is claimed.


## Local correction

Both factories now query the original molecule atom memberships and create one
LIG group per inherited molecule. Source atom order, names, chemistry, geometry,
chain label and all existing scientific assertions remain. Added assertions
require unchanged molecule counts and memberships. Both focused files pass all
210 cases, zero failures/errors/skips. No reader, builder guard, selection engine
or model parameter is changed. Hosted closure remains pending on the corrected
source; original 40571118517 stays failure evidence.
