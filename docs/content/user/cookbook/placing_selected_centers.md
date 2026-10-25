(Cookbook_Placing_Selected_Centers)=
# Placing selected centers

*Moving a population rigidly between explicitly chosen centers.*

Use a common translation to position a molecule or selected atoms without
changing their internal geometry. A source-center population defines what you
place; a target point or an initial target-center population defines where.

:::{versionadded} 1.0.0
:::

## Moving a molecule to another population

This small coordinate-only system represents two destination atoms A and B at
2 and 4 nm, and two moving atoms C and D at 10 and 12 nm. Moving C and D to the
center of A and B puts their center at 3 nm and preserves their 2 nm separation.
Only explicit atom indices are needed, so a topology is unnecessary.

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures

puw = msm.pyunitwizard
molsys = Structures(coordinates=puw.quantity(
    [[[2, 0, 0], [4, 0, 0], [10, 0, 0], [12, 0, 0]]], 'nm'))
molsys_centered = msm.structure.center(
    molsys, selection=[2, 3], target_center_selection=[0, 1])
xyz = puw.get_value(msm.get(molsys_centered, element='atom', coordinates=True),
                    to_unit='nm')
np.testing.assert_allclose(xyz[0, :, 0], [2, 4, 2, 4], atol=1e-12)
```

To move C alone to 3 nm, use `selection=[2]` with the same target selection.
By default the source center belongs to `selection`, not the entire system.
The input remains unchanged unless you request `in_place=True`.

## Using one atom as the source center

Move C and D together while placing C itself at 1 nm. D remains 2 nm from C.
The source-center population must be contained in the moving selection.

```python
molsys_centered = msm.structure.center(
    molsys, selection=[2, 3], source_center_selection=[2],
    target_coordinates='[10, 0, 0] angstrom')
xyz = puw.get_value(msm.get(molsys_centered, element='atom', coordinates=True),
                    to_unit='nm')
np.testing.assert_allclose(xyz[0, :, 0], [2, 4, 1, 3], atol=1e-12)
```

Use either `target_center_selection` or `target_coordinates`. With neither,
the destination is the origin. The target selection is always measured before
translation, including when it overlaps the moving population. `weights`
affects only the source center; use `get_center` to prepare a weighted target
and pass that quantity through `target_coordinates`.

For several structures, use `structure_indices` and either one shared target
or a quantity shaped `(n_selected_structures, 1, 3)`. Target rows follow the
requested index order. Repeated indices must have identical targets. Native
coordinate edits invalidate interaction coverage for the edited structures.
This operation uses stored Cartesian coordinates; periodic reconstruction is
a separate preparation step.

:::{seealso}
:class: dropdown

- {ref}`Center <Tutorial_Center>`
- {ref}`Get center <Tutorial_Get_center>`
- {ref}`The molecular system <user-foundations-molecular-system-definition>`
- {func}`molsysmt.structure.center`
:::
