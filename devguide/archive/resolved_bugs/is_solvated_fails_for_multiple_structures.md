---
summary: is_solvated fails for multiple structures with waters and periodic boxes.
issue: uibcdf/molsysmt#504
status: resolved
opened: 2026-10-27
closed: 2026-11-05
severity: medium
verification: reproduced
area: [build, structure, units]
guard: tests/build/is_solvated/test_structure_contract.py
normative:
blocked_by: []
supersedes: []
---

# Multi-structure native solvation predicate

**Reported:** 2026-10-27 during expert-addon receiving under uibcdf/molsysmt#421.
**Status:** Native repair, client receiving and public documentation complete;
the closing comment identifies the published source checkpoint.

## What

`molsysmt.build.is_solvated()` raises `ValueError` for a resident MolSys with multiple structures, indexed waters and a periodic box. The equivalent one-structure input returns True. Native 4e544cb12dd6bb7738da651827f3b69fa5847a9c, Python 3.14; independently reproduced without Viewer calls while receiving the expert addon under uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.

## How

The synthetic coordinates intentionally do not model equilibrated water: this tests only the function's documented water-count/box-volume predicate. Each unit box is 1 nm³ and contains 16 declared waters.

```python
import numpy as np
import molsysmt as msm
puw = msm.pyunitwizard
for n_structures in [1, 2]:
    builder = msm.MolSysBuilder()
    for _ in range(16):
        oxygen = builder.add_atom(atom_name="O", atom_type="O")
        first = builder.add_atom(atom_name="H1", atom_type="H")
        second = builder.add_atom(atom_name="H2", atom_type="H")
        builder.add_group([oxygen, first, second], group_name="HOH")
        builder.add_bond(oxygen, first)
        builder.add_bond(oxygen, second)
    builder.set_coordinates(puw.quantity(np.zeros((n_structures, 48, 3)), "nm"))
    builder.set_box(puw.quantity(np.repeat(np.eye(3)[None], n_structures, axis=0), "nm"))
    molsys = builder.build()
    try:
        print(n_structures, msm.build.is_solvated(molsys))
    except Exception as error:
        print(n_structures, type(error).__name__, str(error))
```

Observed:

```text
1 True
2 ValueError The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
```

The implementation compares `density_number > 15` in a Python `if`; the multi-structure box-volume array cannot be interpreted as one truth value. It has no public structure-selection argument. No scientific workaround has been added to the addon.

## Why

Users need an explicit and reliable contract for trajectories/ensembles. Please decide and document per-structure output versus an explicit aggregation/selection contract; silently choosing first/any/all would change the scientific meaning. Preserve the single-structure density threshold, units, water/box prerequisites and native argument validation. Test multiple structures with densities above/below/equal to the threshold, mixed densities, no waters/box and equivalent length units, with supported shape and error behavior explicit.

## What is measured and what is assumed

The standalone native reproduction on 4e544cb12, Python 3.14, returns True for
one structure and the quoted ValueError for two. Inputs use identical 1 nm cubed
boxes with 16 indexed O-H-H groups. This is a predicate/shape test, not a
simulation, a water-density model benchmark or a physical solvation claim.

## What was refuted

No Viewer callback, scene state or wrapper computation is required to reproduce
it. Water absence does not expose the branch because native logic short-circuits.
The source cause is the scalar Python condition applied to multiple box volumes;
there is no evidence that selecting a first structure or silently reducing the
array would match the intended scientific contract.

## Scope and exclusions

Native build.is_solvated and its expert bound reader only. No solvation,
coordinate generation, periodic reconstruction or automatic scientific repair is
implemented in this receiving. The addon delegates native outcomes unchanged.

## Acceptance criteria

Define the public multi-structure result/selection/aggregation contract, retain
single-structure behavior and test it with native pytest. Include above/equal/
below/mixed thresholds, no waters/box, length-unit equivalence and supported
shape/error cases. Supply a failing-before/passing-after native guard before
closing; receive the result separately in the addon without a consumer formula.

## Dependencies and risks

The decision belongs to MolSysMT. An implicit first/any/all reduction would change
meaning. The current addon documents the limitation; no publication or universal
multi-structure qualification is claimed.

## Receiving decision — 2026-11-05

The implementation preserves Python bool for one selected structure and returns
a one-dimensional Boolean vector for multiple/empty selections, with keyword-only
`structure_indices='all'`. No first/any/all reduction is applied. This choice
preserves existing one-structure callers while making every ensemble outcome
explicit. Always-array output would change the established one-structure type;
a default ensemble reduction would impose an interpretation. The old positional
skip flag remains in its original slot. Multi-structure no-water/no-box inputs
previously returned one false scalar through an early short circuit; they now
return aligned false vectors too. Consumers using the former scalar shortcut
must select one structure or choose an explicit reduction. Callers needing one consistent array
container may normalize the result themselves; no additional output-mode API is
needed for this repair.

The corrected baseline guard records 28 failures and six passes on unchanged
native code. One failure is an invalid source-snapshot test fixture (a nonexistent
Structures.to_dict method), corrected in receiving; an earlier draft also used
item assignment on the read-only interaction mapping. Neither fixture error is
a production defect. Actual cases reproduce ambiguous multi-structure truth,
missing selector support, missing-water-inventory TypeError, invalid volume
classification and scalar outputs for known multi-structure prerequisites.

The native repair reuses one agnostic basic.get call for indexed water count,
box volume and selected source structure indices. It converts volumes explicitly
to nm cubed and evaluates the unchanged strict density threshold independently.
Missing water count is an explicit unavailable-attribute diagnostic; absent
water/box produces false entries on the selected structure axis. Nonfinite or
nonpositive available volumes are refused. This is a density predicate, not
solvent completeness, simulation validation, a containment test or preparation.
No new Rust kernel, optional engine, dependency floor or published scientific
method is required. Molecular reading stays in the existing form providers.

### Unit-boundary correction

Independent equality controls found that 15 indexed waters in a nominal 1 nm³
box returned false for the nm representation but true for equivalent angstrom
and pm inputs. Conversion yielded a stored volume of 0.9999999999999997 nm³,
which placed the computed density infinitesimally above the threshold. The
predicate now treats densities within eight relative machine epsilons of 15 as
equality; it does not introduce a physical density margin. Values 1e-9 above and
below the threshold retain their intended classifications. This numerical
convention is explicit in the docstring/tutorial and tested for all three units.

A native guard refuses coordinate materialization and passes; a box-only native
Structures domain with a separate water inventory also works. This does not
promise metadata-only I/O for foreign forms: existing H5MSM 0.5 public queries
retain their resident loading boundary. No alternate file loader is added.

### Client and documentation receiving

The existing addon mirror forwards keyword-only structure_indices unchanged and
returns native scalar/vector values. Mixed literal density outputs, source
identity, scene/synchronization state, return independence and explicit native
signature are checked. Two older scalar-only equality assertions were replaced
by the existing structural comparison helper; they now verify array values as
well. A coordinate-read sentinel was corrected to forward the backend's owned
keyword. These test-fixture/assertion corrections are distinct from native bugs.

Current receiving passes 796 affected native/PBC/basic-get/client tests, 41
new native cases with the declared published support-library floors and 544
documentation/schema/course/client-inventory controls. The native doctest passes.
The full updated solvation-predicate tutorial executes successfully (8.7 s) in
the existing environment. The first sandboxed attempt failed before any code
cell because Jupyter could not open local sockets; the authorized loopback
execution succeeds. The stored outputs include the original preparation example
and synthetic ensemble, selection, scalar, explicit-reduction and empty cases.

## Resolution — 2026-11-05

The native predicate and existing addon mirror now support the selected structure
axis without an ambiguous-array truth test. The guard checks literal density
results and output shape/type, empty and repeated selections, missing versus
unavailable prerequisites, invalid indices/volumes, non-default unit policies,
unit-equivalent boundary equality and unchanged molecular/analysis ownership.
Native coordinate-materialization refusal and coordinate-free box-only context
are verified. Four form routes are exercised: native MolSys, explicit domain
composition, MolSysDict and H5MSM 0.5. No all-form or out-of-core guarantee follows.

The existing client signature/ownership suite passes with the new keyword; an
independent mixed-density client case checks `[True, False, True, True]` in the
requested order, single-structure Python bool, unchanged primary identity and
unchanged sync status. There is no browser, Qt, installed-package or release
qualification claim. The existing scientific-evidence registry remains the
authority for the heuristic's experimental status; mathematical density controls
do not calibrate physical solvation. No published external detection method or
new attribution resource is introduced.

The User Guide tutorial, Cookbook, course, generated native client help and
maintained addon guides describe the same return/selection/unit contract. The
13-cell tutorial executes, showing mixed, repeated, scalar, deliberate all/any
and empty outputs. Course/Cookbook executable cells, outputs and metadata are
unchanged. Source/test/notebook hashes, failed attempts, final commands and
bounded results are retained in
`devtools/data/solvation_predicate_receiving_504_20261105.json`.
