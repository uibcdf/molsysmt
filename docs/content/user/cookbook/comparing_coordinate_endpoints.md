(Cookbook_Comparing_Coordinate_Endpoints)=
# Comparing coordinate endpoints

*Checking distances and neighbors across independent coordinate sets.*

Use independent source objects when the coordinates describe different systems.
Use structure indices to address observations within each system. Keep both
index spaces explicit when interpreting the results.

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
puw = msm.pyunitwizard
xyz = np.array([[[0., 0., 0.], [1., 0., 0.], [4., 0., 0.]],
                [[1., 0., 0.], [2., 0., 0.], [5., 0., 0.]]])
molsys = Structures(coordinates=puw.quantity(xyz, 'nm'))
molsys_2 = Structures(coordinates=puw.quantity(xyz + [10., 0., 0.], 'nm'))
```

Pair the selected structures positionally. A repeated structure index reuses that
observation; it does not identify a different system.

```python
matrix = msm.structure.get_distances(molsys, selection=[0],
    molecular_system_2=molsys_2, selection_2=[1, 2],
    structure_indices=[1, 0, 1], structure_indices_2=[1, 0, 1], pbc=False)
np.testing.assert_allclose(puw.get_value(matrix, to_unit='nm')[:, 0],
                           [[11., 14.]] * 3)
neighbors, distances = msm.structure.get_neighbors(molsys, selection=[0],
    molecular_system_2=molsys_2, selection_2=[0, 1], n_neighbors=1, pbc=False)
np.testing.assert_array_equal(neighbors, np.zeros((2, 1, 1), dtype=int))
np.testing.assert_allclose(puw.get_value(distances, to_unit='nm'), 10.)
```

The first returned neighbor index is local target position zero, even though it
has the same number as a primary atom index. The target remains a separate source.
For contacts within one source, choose its second structure list explicitly:

```python
contacts = msm.structure.get_contacts(molsys, selection=[0], selection_2=[1, 2],
    threshold='1 nm', pbc=False, cell_list=False, use_gpu=False)
np.testing.assert_array_equal(contacts, [[[True, False]], [[True, False]]])
```

With PBC, the primary source supplies the box. Compound centers use the supplied
positions; reconstruct participants before taking a center when they span periodic
images. For large distance outputs, consume disk-backed handles in blocks and
clean them up. Contacts require a resident map and coordinate workspace.
See {ref}`user-tools-distance-family` for output, empty-input and error contracts.
