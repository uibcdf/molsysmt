---
summary: move_away publishes NaNs for degenerate directions.
issue: uibcdf/molsysmt#456
status: resolved
opened: 2026-10-25
closed: 2026-10-25
severity: high
verification: measured
area: [structure]
guard: tests/structure/move_away/test_move_away_contract.py
normative:
blocked_by: []
supersedes: []
---

# move_away publishes NaNs for degenerate directions

**Reported:** 2026-10-25 during authorized addon receiving under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.
**Status:** resolved with native pre-publication validation and independent numerical guards.

## What

What — `structure.move_away()` publishes NaN coordinates when source/reference centers coincide (including its defaults), or when `direction=[0, 0, 0]`. No exception is raised.

How — On source fc2936bf9, Python 3.14/Linux, load bundled pentalanine and run either call on a fresh copy:
```python
import molsysmt as msm
import numpy as np
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0, 8, 3])
msm.structure.move_away(molsys, in_place=True)  # alternatively direction=[0, 0, 0]
assert np.isfinite(msm.pyunitwizard.get_value(msm.get(molsys, coordinates=True))).all()  # fails
```

## How

The native default uses the same population for source and reference, so its
automatic direction is zero. In molsysmt/structure/move_away.py the direction is
divided by its norm without validating it. Explicit zero vectors are normalized
similarly by molsysmt/_private/argdigest/argument/direction.py. Both routes
publish NaNs without a scientific exception.

On a fresh bundled pentalanine MolSys, structure.move_away(molsys, in_place=True)
or the same call with direction=[0, 0, 0] returns None, emits a RuntimeWarning
and leaves nonfinite coordinates on structure 0. The independent route and
other degenerate variants need owning scientific tests; this report does not
claim they were all measured.



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

Reject undefined/nonfinite directions before writes, or document and implement
an explicit accepted zero-displacement policy. Retain coordinates, box and
interaction coverage on rejection. Include native pytest across automatic and
explicit modes, independent/in-place results, references, weights and structure
scopes, alongside valid finite displacement checks.

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


## Tutorial rendering follow-up — 2026-10-25

The first successful noninteractive tutorial execution retained numerical outputs
but did not embed its comparison figure under the forced Agg backend. Enabling
Jupyter's inline plotting in that tutorial and reexecuting it (6.9 seconds) saves
one PNG figure showing the independently asserted 1/3/2 nm separations. The saved
image is visually inspected; numerical code and library sources are unchanged.
This is a documentation rendering correction, not new scientific evidence or a
replacement of the original regression results.
