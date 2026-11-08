(cookbook-delivering-coordinates)=
# Delivering declared coordinate values

*Assigning an existing coordinate quantity to selected structures.*

A pose can already be a length quantity with known atom correspondence. Pass it
directly to {func}`molsysmt.basic.set` on your mutable molecular system. Choose
the destination structure explicitly. MolSysMT checks axis compatibility; you
remain responsible for declaring that the atom positions refer to the same
atoms in the same order.

```python
import numpy as np
import molsysmt as msm

puw = msm.pyunitwizard
pose = puw.quantity([[1., 2., 3.], [4., 5., 6.]], 'angstrom')
molsys = msm.convert(
    puw.quantity(np.zeros((2, 2, 3)), 'nm'), to_form='molsysmt.MolSys')
msm.set(molsys, structure_indices=1, coordinates=pose)
actual = msm.get(molsys, element='atom', coordinates=True)
np.testing.assert_allclose(puw.get_value(actual, to_unit='angstrom')[0], 0.)
np.testing.assert_allclose(
    puw.get_value(actual, to_unit='angstrom')[1], [[1., 2., 3.], [4., 5., 6.]])
```

This synthetic coordinate-only example supplies no chemical identity. In an
application, use your independently copied, prepared system with its declared
atom map. A coordinate value does not create that correspondence or assign a
chemical model. Changing coordinates follows the system's ordinary interaction
invalidation contract.

## Querying a coordinate quantity

If you need a query first, XYZ provides coordinates at the **atom** level:

```python
selected = msm.get(pose, element='atom', selection=[1, 0], coordinates=True)
assert selected.shape == (1, 2, 3)
np.testing.assert_allclose(
    puw.get_value(selected, to_unit='angstrom')[0], [[4., 5., 6.], [1., 2., 3.]])
```

`msm.get(pose, coordinates=True)` defaults to `element='system'`. XYZ does not
implement that coordinate getter and raises `NotWithThisFormError`; use the
explicit atom-level query above. A numeric selection retains its requested
order and repetitions on both axes. Reordering coordinates alone does not
reorder a target molecular inventory.

XYZ accepts length quantities with shapes `(3,)`, `(n_atoms, 3)` and
`(n_structures, n_atoms, 3)`. Queries return rank-three quantities; they preserve
physical values under another application unit policy. Bare arrays without
length units and arrays with other ranks or a final dimension other than three
are not XYZ. A query result is not an independent mutable copy of its input;
use supported copy operations when you need independent editing.

:::{seealso}
:class: dropdown

{ref}`Tutorial_Form_XYZ` describes the coordinate-only form.
{func}`molsysmt.basic.get` queries attributes and
{func}`molsysmt.basic.set` assigns them to mutable systems.
:::
