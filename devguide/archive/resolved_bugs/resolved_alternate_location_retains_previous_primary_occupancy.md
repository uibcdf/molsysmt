---
summary: Resolving an alternate location retains the previous primary occupancy
issue: uibcdf/molsysmt#570
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [build, alternate_locations]
guard: tests/build/solve_atoms_with_alternate_location/test_alternate_location_contract.py::test_selected_primary_observation_includes_its_occupancy
normative:
blocked_by: []
supersedes: []
---

# Resolving an alternate location retains the previous primary occupancy

**Reported:** 2026-11-05 during expert-addon receiving; standalone native reproduction, explicitly authorized by the principal maintainer.
**Status:** Open; scientific correction/contract decision belongs to MolSysMT.

## What

Choosing B updates coordinates, available B factor and the atom-ID label, but the primary structural occupancy remains A's old value. Please confirm whether this is a defect or an intended separately documented data contract; the numerical mismatch itself is reproduced.

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
system.structures.occupancy = np.array([[0.4]])
system.structures.alternate_location[0][0]["occupancy"] = np.array([0.4, 0.6])
msm.build.solve_atoms_with_alternate_location(system, location_id="B")
print(msm.get(system, element="atom", atom_id=True))  # ['11']
print(system.structures.occupancy)  # [[0.4]], chosen B has 0.6
print(puw.get_value(system.structures.b_factor, to_unit="nm**2"))  # [[0.24]]
```

The writer builds a values dict containing coordinates and, when available, b_factor; it does not publish the chosen occupancy. Retaining the full alternate-site records is a distinct, already documented behavior.

## Why

Readers/exports may associate B's position and ID with A's occupancy. Viewer needs a precise native contract and must not invent a correction. This is different from #556, which concerns occupancy acquisition during CIF conversion; this reproduction constructs native data directly.

## Acceptance

Decide and document primary-occupancy semantics, then protect explicit site and occupancy-policy selection, selected/unselected atoms and structures, missing occupancy, alternate-record preservation and unit-free occupancy values. If primary occupancy follows the selected site, test consistency with coordinates/B factors/ID and persistence.

## Provenance

Reproduced without MolSysViewer, in the explicit molsyssuite@uibcdf_3.14 source environment, Python 3.14.7. Contribution input a1dbe0fb67373c32b0ca3276aa40f52250ff9554, native owner basis 5f3af9374f2bf4ce9c3598450e22d43ca14509ae. Native solve_atoms_with_alternate_location.py SHA-256: 91028f58c53cf0424f585b6d6e3333e14e8edf1841b2f7dddeee2503ec006af7; the current owner checkout has identical function bytes. No new package/installation or universal scientific qualification is claimed.

This was found while receiving the expert addon under #421 / PR #543 and uibcdf/molsysviewer#264. The addon must preserve native science rather than repair selection/metadata downstream. The maintainer explicitly authorized these reports. Duplicate search included open/closed alternate-location, occupancy and partial-write reports; #88/#175 describe different work.

## What is measured and what is assumed

The chosen B site has occupancy 0.6; stored primary occupancy remains 0.4 while coordinates, ID and B factor move. Whether retaining that occupancy is intentional remains an explicit owner contract question.

## What was refuted

This is independent of CIF acquisition (#556): the fixture declares native occupancy directly. Keeping alternate-site records does not require retaining a primary value for a different chosen site.

## Scope and exclusions

Native solve_atoms_with_alternate_location only. No consumer scientific repair, implicit conformer generation or automatic recovery from arbitrary raw edits. Existing identity, units and data-preservation contracts remain applicable.

## Consumer receiving — 2026-11-05

Published owner correction `532d03622` resolves this report. The
[canonical owner resolution](alternate_location_resolution_retains_the_previous_primary_occupancy.md)
records the scientific contract and specific regression named above. This
original contribution report is retained as historical reproduction evidence;
its earlier outcomes apply to the old producer, not to the corrected source.
The expert addon delegates the repaired native operation and verifies primary
measurements, stable-label conflicts and clean late rejection separately.
