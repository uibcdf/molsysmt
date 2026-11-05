---
summary: Alternate-location occupancy selection can choose a lower-occupancy site
issue: uibcdf/molsysmt#569
status: open
opened: 2026-11-05
closed:
severity: high
verification: reproduced
area: [build, alternate_locations]
guard:
normative:
blocked_by: []
supersedes: []
---

# Alternate-location occupancy selection can choose a lower-occupancy site

**Reported:** 2026-11-05 during expert-addon receiving; standalone native reproduction, explicitly authorized by the principal maintainer.
**Status:** Open; scientific correction/contract decision belongs to MolSysMT.

## What

The documented highest-occupancy policy chooses A=0.2 instead of B=0.5. This is not a tie.

## How

```python
import numpy as np
import molsysmt as msm

puw = msm.pyunitwizard
builder = msm.MolSysBuilder()
builder.add_atom(atom_name="C", atom_type="C", atom_id="10")
builder.set_coordinates(puw.quantity([[[0., 0., 0.]]], "nm"))
system = builder.build()
system.structures.b_factor = puw.quantity([[0.1]], "nm**2")
system.structures.occupancy = np.array([[0.2]])
system.structures.alternate_location = [{
    0: {
        "location_id": np.array(["A", "B"]),
        "occupancy": np.array([0.2, 0.5]),
        "atom_id": np.array(["10", "11"]),
        "coordinates": puw.quantity([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], "nm"),
        "b_factor": puw.quantity([0.12, 0.24], "nm**2"),
    }
}]
msm.build.solve_atoms_with_alternate_location(system)
print(msm.get(system, element="atom", atom_id=True))  # ['10'] (A), expected ['11'] (B)
print(puw.get_value(system.structures.coordinates, to_unit="nm"))
# [[[0.1, 0.2, 0.3]]] -- the lower-occupancy A coordinates
```

_location_position first finds the maximum, then replaces its index by A whenever that maximum is close to 0.5 and A exists. It does not verify that A shares the maximum. The public help/tutorial promise maximum occupancy and preference for A on a 0.5 tie.

## Why

The default scientific policy can select a different crystallographic conformer from the documented one, affecting coordinates, labels and downstream analysis. No addon normalization is proposed.

## Acceptance

Protect maximum selection, true ties with/without A, unequal occupancies including maximum 0.5, metadata order, missing/NaN policies as explicitly decided by the owner, selected atoms and nonconsecutive structures. Keep the tie-tolerance policy explicit; do not renormalize occupancies in the consumer.

## Provenance

Reproduced without MolSysViewer, in the explicit molsyssuite@uibcdf_3.14 source environment, Python 3.14.7. Contribution input a1dbe0fb67373c32b0ca3276aa40f52250ff9554, native owner basis 5f3af9374f2bf4ce9c3598450e22d43ca14509ae. Native solve_atoms_with_alternate_location.py SHA-256: 91028f58c53cf0424f585b6d6e3333e14e8edf1841b2f7dddeee2503ec006af7; the current owner checkout has identical function bytes. No new package/installation or universal scientific qualification is claimed.

This was found while receiving the expert addon under #421 / PR #543 and uibcdf/molsysviewer#264. The addon must preserve native science rather than repair selection/metadata downstream. The maintainer explicitly authorized these reports. Duplicate search included open/closed alternate-location, occupancy and partial-write reports; #88/#175 describe different work.

## What is measured and what is assumed

The native call chooses A=0.2 despite B=0.5, verified from stored coordinates and an atom-level ID query. The exact tolerance desired for ties remains an owner policy decision; this example is not a tie.

## What was refuted

The standalone native call reproduces the mismatch without Viewer. No normalization of occupancy sums or reconstruction algorithm is proposed.

## Scope and exclusions

Native solve_atoms_with_alternate_location only. No consumer scientific repair, implicit conformer generation or automatic recovery from arbitrary raw edits. Existing identity, units and data-preservation contracts remain applicable.
