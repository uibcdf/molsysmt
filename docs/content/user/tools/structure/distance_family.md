(user-tools-distance-family)=
# Distances and neighborhoods

*Keeping endpoint coordinates, weights and indices aligned.*

These tools share an endpoint model. Every atom index addresses its own source;
every selected structure in the first list pairs with the structure at the same
position in the second list. Repeated and nonconsecutive indices retain that
order. There is no implicit broadcast: repeat a structure index explicitly to
reuse it. A supplied second molecular system remains independent even when its
selection and structure arguments are omitted.

| Tool | Observable | Index convention |
| :--- | :--- | :--- |
| {func}`molsysmt.structure.get_distances` | Cartesian matrix or corresponding pair distances | Requested atom/selection labels and both structure axes |
| {func}`molsysmt.structure.get_minimum_distances` | Minimum over the selected reduction axes | Local positions in the reduced population(s) |
| {func}`molsysmt.structure.get_maximum_distances` | Maximum over the selected reduction axes | Local positions in the reduced population(s) |
| {func}`molsysmt.structure.get_neighbors` | Nearest count or inclusive distance cutoff | Local target positions; optional labeled pairs or flat CSR |
| {func}`molsysmt.structure.get_contacts` | Inclusive boolean distance cutoff | Matrix positions or labeled contacting pairs |

## Independent endpoints

`weights` and `weights_2` belong to their respective centers. Numeric weights are
finite nonnegative vectors with a positive sum for every group; zero individual
weights are valid. `weights='masses'` reads masses through the chemical-property
owner. Nested selections define multiple centers, with per-group weights also
accepted. Weights on raw atom endpoints reject rather than being ignored.

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
puw = msm.pyunitwizard
xyz = np.array([[[0., 0., 0.], [1., 0., 0.], [4., 0., 0.]]])
molsys = Structures(coordinates=puw.quantity(xyz, 'nm'))
indices, values = msm.structure.get_minimum_distances(molsys,
    selection=[0, 1], selection_2=[1, 2], center_of_atoms=True,
    center_of_atoms_2=True, weights=[1., 1.], weights_2=[1., 3.], pbc=False)
np.testing.assert_allclose(puw.get_value(values, to_unit='nm'), [2.75])
```

Entity flags on extrema choose reduction axes; they do not define groups.
Both flags reduce globally, returning a local index pair per structure. Keeping
one population returns one extremum per member of that population and the local
index into the reduced population. Paired distances require both flags. Extrema
choose the first tied local occurrence in row-major order and reject empty
populations. Empty distance matrices retain their declared shape and dtype.

## Neighbor identity and contacts

An implicit self-neighbor search without a second endpoint definition excludes physical self identity. Distinct atoms
at identical coordinates remain neighbors. Repeated self-selection entries do
not turn the same physical atom into its own neighbor. Explicit second selections, center definitions
or structure lists are independent endpoints; their zero-distance entries remain
eligible. An explicitly supplied second system is always independent.

Neighbors sort by distance, breaking ties by local target position. Counts can
be zero and must fit every query's available targets. Cutoffs are finite,
nonnegative scalar lengths and include equality. Empty query/target populations
have defined empty outputs. Pair filters need compatible identities within one
source. `sorted=True` sorts pair rows without exchanging query and target roles.

Contact matrices include the diagonal in an implicit same-structure self map;
its pair output retains the strict upper triangle. When endpoint structures are
explicitly different, pair output retains all directed entries. Resolved atom
indices are used even when selections are expressions. `get_contacts` has no
second-system argument; do not treat another structure index as another system.

## Units and periodicity

Lengths use PyUnitWizard's active presentation policy; nm, angstrom and pm inputs
are compared by physical magnitude. The primary system supplies the periodic
box. Missing boxes use the existing vacuum fallback. Supplied periodic boxes must
be finite and nonsingular; orthogonal and supported triclinic geometry use MIC.
Centers are calculated from the supplied positions. Make a compound participant
whole through the periodic tools when its wrapped coordinates span images.
See {ref}`user-foundations-governance-quantities-and-units`.

## Formats and memory

Dictionary distances retain positional structure pairs, including repeated primary
indices with different secondary indices. Center dictionaries require selection
keys; group/atom-label combinations without a meaningful representation reject.
Paired ndarray metadata and neighbor structure-label output remain unsupported.
CSR neighbors cover flat-atom threshold searches using the cell-list route;
unsupported combinations raise explicitly.

Flat single-system distances support eager, automatic and forced chunked
execution. Centers, explicit atom pairs and two-system calculations retain their
eager route even with a force request. Oversized distance matrices can return a
`PersistentResultHandle` magnitude: read it by blocks and call `cleanup()`.
Dictionary output does not support this disk-backed result. Extrema, neighbors
and CPU contacts retire their internally created disk distance intermediates.

Contacts return a resident boolean map, including when pair lists are requested.
Their coordinate preparation for accelerated dispatch also uses RAM; the map
budget is not a process-RSS cap or an out-of-core guarantee. The cell-list and
scalar routes are tested independently against numerical references. Actual GPU
kernels require separate device qualification; a GPU-selector fallback to CPU
does not qualify GPU computation.

See {doc}`../../cookbook/comparing_coordinate_endpoints` for a complete workflow.
