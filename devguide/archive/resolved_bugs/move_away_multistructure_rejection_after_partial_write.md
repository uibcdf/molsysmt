---
summary: move_away rejects multiple structures after partial publication.
issue: uibcdf/molsysmt#457
status: resolved
opened: 2026-10-25
closed: 2026-10-25
severity: high
verification: measured
area: [structure]
guard: tests/structure/move_away/test_move_away_contract.py::test_multiple_structures_reject_before_any_write
normative:
blocked_by: []
supersedes: []
---

# move_away rejects multiple structures after partial publication

**Reported:** 2026-10-25 during authorized addon receiving under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.
**Status:** resolved with native pre-publication validation and independent numerical guards.

## What

What — Explicit-direction `structure.move_away(..., in_place=True)` can modify coordinates before raising `NotImplementedMethodError` for multiple structures.

How — Reproduced without Viewer on source fc2936bf9, Python 3.14/Linux:
```python
import molsysmt as msm
import numpy as np
p = msm.pyunitwizard
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0, 8, 3])
before = p.get_value(msm.get(molsys, coordinates=True), to_unit='nm').copy()
try:
    msm.structure.move_away(molsys, selection=[0, 2, 4], center_of_selection=[0, 2],
        reference_center_of_selection=[1, 3], structure_indices=[2, 0],
        direction=[1, 0, 0], in_place=True)
except Exception as error:
    print(type(error).__name__)  # NotImplementedMethodError
assert np.array_equal(before, p.get_value(msm.get(molsys, coordinates=True), to_unit='nm'))  # fails
```

## How

The explicit in-place route in molsysmt/structure/move_away.py calls native
center before checking the supported single-structure direction/coordinate
shapes. With moving atoms [0, 2, 4], source [0, 2], reference [1, 3], selected
structures [2, 0] and direction [1, 0, 0], it raises NotImplementedMethodError
after changing coordinates on structures 0 and 2. If initial source/reference
centers happen to coincide, that example can look like a no-op; distinct
populations make the partial write visible.



## Why

Public coordinate editing can publish invalid or incomplete scientific results.
The addon cannot infer rollback or add an alternate scientific algorithm. Only
single-structure nondegenerate displacement receives positive qualification.

## What is measured and what is assumed

The pure-MolSysMT reproduction script and JSON are retained in temporary source
receiving evidence. The issue reproduction uses the same bundled pentalanine
file, structure subset and arguments. No Viewer call is required for the defect.
The report does not certify every direction/weight/reference combination.

## What was refuted

This is not a frontend or synchronization failure. It reproduces before any
viewer or addon participates. Existing successful single-structure tests do not
exercise these failing populations or axes.

## Scope and exclusions

The native move_away boundary owns the repair. No runtime observer, automatic
scientific replay, fallback method, or new molecular Undo is requested.

## Acceptance criteria

Check unsupported cases before publication or implement the broader native
contract explicitly. Add pytest for auto/explicit direction, copy/in-place,
scalar/list/nonconsecutive/repeated structures, reference shape combinations and
coordinate/box/interaction preservation on rejection. Native valid single
structure behavior must remain covered. This receiving does not demand new
multi-structure support; pre-write rejection is sufficient.

## Provenance

Native source fc2936bf9efd198f02f1d195107e5a5e6f62d13b; Linux x86-64;
Conda molsyssuite@uibcdf_3.14, Python 3.14. Bundled
pentalanine/traj_pentalanine.h5msm, structure subset [0, 8, 3]. The fresh native
reproductions ran on 2026-10-25 and retain their original JSON in the receiving
receipt. No package installation or cross-platform qualification is asserted.


## Resolution — 2026-10-25

The public signature and single-structure scope are preserved. Both primary and
reference axes must resolve to exactly one requested structure; repeated indices
are not silently deduplicated or broadcast. Unsupported axes reject before any
coordinate editor is invoked. Empty/out-of-range axes remain invalid.

The existing direction digester and automatic direction calculation share a
small private scale-safe vector normalizer. It rejects zero/nonfinite vectors
before division, preserves the caller's array, and handles finite magnitudes
whose naive norm would overflow or underflow. Distance must contain one finite
real length value. Zero and negative offsets retain the documented two-mode
semantics; even zero distance needs a defined automatic direction. Center
calculations and explicit unit conversions use the existing form-agnostic
geometry and PyUnitWizard owners.

Automatic mode delegates a Cartesian displacement to `translate`. Explicit mode
constructs the final target from the initial reference center and normalized
offset, then delegates to `center` once. Source containment, weight validation,
rigid geometry and native output ownership remain with those general tools.
No clone or rollback layer is added for in-place calls. Only independent output
requires its normal system copy. The general empty-population centroid error
found by these guards is repaired in `get_center` under uibcdf/molsysmt#459,
rather than hidden in a consumer exception handler.

The initial 98-case contract selection produced 33 failures and 65 passes on
the original source. Besides the reproduced corruption/partial-write cases,
this selection specifies early diagnostic/cardinality checks and extreme-vector
normalization. Later guards add invalid weights, signed/zero distances, source
syntax, file references and original reproduction inputs. One test draft used
`get_mass`'s system-level default rather than `element="atom"`; correcting the
independent oracle did not change production chemistry or masses.

## Verification

The broad command is:

```bash
MPLBACKEND=Agg python -m pytest tests/structure tests/pbc \
  tests/scientific_truth/structure tests/_private/argdigest \
  tests/build/remove_overlapping_molecules \
  tests/documentation/test_move_away_examples.py \
  tests/molsysviewer_molsysmt/test_structure_move_away_tools.py \
  -m 'not network' --receptor=llm -n 12
```

It passes **2,174 tests in 41.44 seconds**, without failures or omissions. The
530 retained warnings comprise 513 legacy-H5MSM, eight requested-GPU CPU
fallbacks, eight deliberate tiny-memory-budget warnings and one structural
attribute drop. This does not qualify an actual GPU backend. The focused
native/center/digestion/documentation/real-view selection passes 818 cases in
18.18 seconds. Both geometry docstring doctests pass in 8.31 seconds.

Independent Cartesian oracles cover input MolSys/Structures, external read-only
H5MSM references, self-reference snapshots, separate numeric/mass weights,
repeated atom populations, source containment, nm/angstrom/pm policies, selected
structure scope, rigid atom differences, independent/in-place returns and
interaction invalidation. Rejected inputs preserve coordinates, boxes, analysis
identity and evaluated coverage. Real MolSysViewer receiving checks that the
same native rejection leaves the scene synchronized, without substitute science.

The Toolbox and Common Core Module 16 notebooks execute successfully (9.1 and
11.5 seconds), including a unit-labelled comparison plot and executable rejection
examples. Their first sandboxed execution could not open Jupyter's local socket;
normal execution with that capability passed, without changing notebook science.
Foundations, Cookbook, runtime help and addon guidance reflect the same contract.
Final local/CI checks are recorded at closure. No final installed pair, supported
platform matrix, release, tag, staging upload or dependency-floor change is
inferred from these source results.


## Final local checks — 2026-10-25

After adding the explicit copy-budget guards, the consolidated focused selection
passes **820 tests in 21.02 seconds**, with the same 82 legacy-H5MSM warnings.
The new guards observe zero whole-system copies in place and one for independent
explicit output. There is no timing or peak-memory benchmark claim.

Ruff lint and formatting, all 251 public docstring checks, signature/stability
validation and all fourteen fast release gates pass. A fresh Sphinx HTML build
completes successfully. The existing warning population remains under
uibcdf/molsysmt#144, including the course heading hierarchy required by its local
instructions and the tutorial's existing admonition formatting. No warning-free
build is claimed. The smoke tier now executes the native displacement contract,
empty-centroid guard and documented placement examples; its hosted result is
verified separately for the published commit.
