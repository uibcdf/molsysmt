---
summary: Invalid alternate-location requests can leave earlier structures modified
issue: uibcdf/molsysmt#571
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

# Invalid alternate-location requests can leave earlier structures modified

**Reported:** 2026-11-05 during expert-addon receiving; standalone native reproduction, explicitly authorized by the principal maintainer.
**Status:** Open; scientific correction/contract decision belongs to MolSysMT.

## What

A requested location missing from a later structure raises a malformed ArgumentChoiceError construction as TypeError after modifying an earlier structure. Coordinates/B factors can therefore change while the final global atom-ID write never happens.

## How

```python
from copy import deepcopy
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
site = deepcopy(system.structures.alternate_location[0][0])
site["occupancy"] = np.array([0.4, 0.6])
system.structures.alternate_location = None
system.structures.append(coordinates=puw.quantity([[[0., 0., 0.]]], "nm"))
system.structures.b_factor = puw.quantity([[0.1], [0.1]], "nm**2")
system.structures.occupancy = np.array([[0.4], [0.4]])
system.structures.alternate_location = [{0: deepcopy(site)}, {0: deepcopy(site)}]
system.structures.alternate_location[1][0]["location_id"] = np.array(["A", "C"])
msm.build.solve_atoms_with_alternate_location(
    system, structure_indices=[0, 1], location_id="B"
)
# TypeError: ArgumentChoiceError.__init__() missing 1 required positional argument: 'choices'
# After catching the exception:
# coordinates in nm = [[[0.4,0.5,0.6]], [[0.,0.,0.]]]
# atom_id is still ['10']; the first coordinate now belongs to B/'11'.
```

Each structure publishes coordinates/B factors as the loop progresses. The later missing location raises before the final atom-ID publication; _location_position also omits the required choices argument when constructing its exception. Independent per-structure alternate dictionaries are necessary in the reproduction.

## Why

A failed request leaves partially resolved data and can invalidate only some analysis coverage. Managed Viewer integration must classify this as uncertain and require explicit recovery, rather than retrying science or silently declaring synchronization.

## Acceptance

Prefer full request validation before any publication, with a proper public choice error. Protect a valid first/invalid later structure, a failing first structure, several selected atoms/sites, nonconsecutive/repeated structures, coordinates/B factors/IDs/occupancy/analysis coverage preservation on rejected requests and input alternate-record ownership. If partial publication is intentionally retained, document that guarantee and a reliable recovery contract explicitly.

## Provenance

Reproduced without MolSysViewer, in the explicit molsyssuite@uibcdf_3.14 source environment, Python 3.14.7. Contribution input a1dbe0fb67373c32b0ca3276aa40f52250ff9554, native owner basis 5f3af9374f2bf4ce9c3598450e22d43ca14509ae. Native solve_atoms_with_alternate_location.py SHA-256: 91028f58c53cf0424f585b6d6e3333e14e8edf1841b2f7dddeee2503ec006af7; the current owner checkout has identical function bytes. No new package/installation or universal scientific qualification is claimed.

This was found while receiving the expert addon under #421 / PR #543 and uibcdf/molsysviewer#264. The addon must preserve native science rather than repair selection/metadata downstream. The maintainer explicitly authorized these reports. Duplicate search included open/closed alternate-location, occupancy and partial-write reports; #88/#175 describe different work.

## What is measured and what is assumed

The valid first structure changes to B coordinates and B factor; the later rejection is TypeError and the final global atom label remains old. No atomic guarantee or rollback mechanism is assumed.

## What was refuted

Separate per-structure alternate dictionaries eliminate the initial shared-dictionary fixture alias. The observed partial write is a native multi-structure call, not a failed Viewer projection.

## Scope and exclusions

Native solve_atoms_with_alternate_location only. No consumer scientific repair, implicit conformer generation or automatic recovery from arbitrary raw edits. Existing identity, units and data-preservation contracts remain applicable.
