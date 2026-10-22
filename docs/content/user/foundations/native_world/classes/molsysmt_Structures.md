(user-foundations-native-world-classes-molsysmt-structures)=
# Structures

`molsysmt.native.Structures` stores atomic coordinates, periodic boxes, structure times and physical observables.

---

## Overview and Role

`Structures` holds spatial data and aligned observables for a single structure,
an ensemble or a molecular dynamics trajectory. It does not require topology.

---

## Internal Attributes

Coordinates and boxes use protected internal numeric blocks. Public quantities
retain the shapes below; other series use numeric arrays or metadata lists:

| Attribute | Data Type | Physical Units | Dimensions / Shape | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`coordinates`** | `float64` numeric blocks | `nanometer` (`nm`) | `(n_structures, n_atoms, 3)` | Cartesian coordinates per structure and atom. |
| **`velocities`** | Numeric array | `nm / ps` | `(n_structures, n_atoms, 3)` | Atomic velocities; dtype follows the supplied values. |
| **`box`** | `float64` numeric blocks | `nanometer` (`nm`) | `(n_structures, 3, 3)` | Periodic box vectors as rows. |
| **`time`** | Numeric array | `picosecond` (`ps`) | `(n_structures,)` | Time associated with each structure, when supplied. |
| **`structure_id`** | Array-like labels | N/A | `(n_structures,)` | Structure labels, distinct from positional indices. |
| **`b_factor`** | Numeric array | `nm²` | `(n_structures, n_atoms)` | Isotropic temperature factors (B-factors). |
| **`occupancy`** | Numeric array | Dimensionless | `(n_structures, n_atoms)` | Crystallographic atom occupancy values. |
| **`alternate_location`** | List of Dicts | N/A | `(n_structures,)` | Alternate location indicators mapping atom indices to location keys. |
| **`temperature`** | NumPy `float64` array | `kelvin` (`K`) | `(n_structures,)` | System temperature per structure. |
| **`potential_energy`** | NumPy `float64` array | `kJ / mol` | `(n_structures,)` | Potential energy per structure. |
| **`kinetic_energy`** | NumPy `float64` array | `kJ / mol` | `(n_structures,)` | Kinetic energy per structure. |

---

A missing periodic box series can be initialized with
`msm.set(molsys, box=...)` or `molsys.structures.set_box(value=...)` using the full
structure axis. Partial box updates require an existing series; they do not
invent periodic boxes for unspecified structures. Box quantities carry length
units and are stored internally in nm. See {ref}`Tutorial_Set`.

## Aligned Observables

Temperature, potential energy and kinetic energy can be supplied directly to
native `Structures` construction and `append()` as unit-bearing series of shape
`(n_structures,)`. Each value belongs to one structure. A scalar becomes a
length-one series; it is not broadcast across a longer coordinate block.
Missing observables remain `None`, and an empty series represents zero structures.

Compatible units are converted on storage (K and kJ/mol); `get()` applies your
active output unit policy. Bare values, Boolean/complex values, matrices and
incompatible units are rejected. Series lengths must match the same coordinate
or metadata structure axis. Invalid append units, ranks or lengths leave the
object unchanged. Existing append policies apply: `intersection` keeps shared
attributes, while `strict` refuses one-sided attributes.

These observables survive supported `StructuresDict` and H5MSM 0.5 round trips.
MolSysDict 0.1 and the current structures YAML codec do not store these three
thermodynamic series. Converting to those formats does not extend their schema.
Scalar temperatures in simulation settings keep their existing contract.
See the {ref}`native input reference <API Native Structure Inputs>`.

## Assembly Operations

`bioassembly` maps assembly names to dictionaries with `chain_indices`,
`rotations` and `translations`. Rotations have shape `(n_operations, 3, 3)`
and must be finite, orthonormal matrices with determinant +1. Translations are
length quantities of shape `(n_operations, 3)`, or a list of unit-bearing
three-component vectors. Compatible length units follow your output unit policy.
These axes count operations, not structures or atoms.

Use a flat nonnegative integer sequence for a chain set shared by every operation,
or one sequence per operation. Operation counts must match. Normal construction
creates independent normalized containers without modifying your input mapping;
constructing again from those containers retains the same shapes. H5MSM 0.5
preserves both chain scopes and stores translations in nm. See
{ref}`the assembly recipe <cookbook-h5msm-assembly-operations>`.

Building an assembly applies each operation to every selected source structure.
Operations expand the atom axis, while structure indices keep their requested
order and repetitions. Structure IDs and times follow that selected structure
axis; IDs remain labels rather than positional selectors. See
{ref}`Make bioassembly <Tutorial_Make_bioassembly>`.

## Invariants and Performance

`repr(structures)` reads stored shape metadata without array conversion, unit
conversion, alignment validation or payload rendering. No atom-aligned series
means `n_atoms=None`; an explicit `(n_structures, 0, 3)` coordinate array means
`n_atoms=0`. This is a brief human summary, not a validity check or interchange
format. `repr(molsys)` can report these dimensions even when topology is absent.

Selected `get()` calls and specialized coordinate/box getters return independent,
editable arrays with quantities. They preserve repeated and nonconsecutive
structure/atom selections. Native iterators use those selected reads rather than
assembling the complete coordinate series. Full `coordinates` and `box`
properties are protected read snapshots; assembling several blocks needs an
output array. A full editable getter likewise needs its complete output memory.

An attached domain's `set_coordinates()` and `set_box()`, and full assignments
to its `coordinates`/`box` properties, notify its owning `MolSys`. Every named
analysis loses occurrences and evaluated coverage on the affected structures;
this includes previously empty results and edits to nonparticipating atoms.
Other structures and earlier snapshots survive. No interactions are recalculated.
Invalid units, selections, shapes or invalidation-allocation failures leave a
direct native edit unpublished. Geometry setters cannot resize axes with attached
analyses; use the owning system's extraction/append tools. ID/time edits do not
invalidate. Raw/private storage writes, whole-domain replacement and direct
domain append/add operations are outside this notification boundary. See
{ref}`Changing coordinates <user-tools-interactions-coordinate-edits>`.

(user-foundations-structures-copying)=
## Independent Copies

`structures.copy()` and `copy.deepcopy(structures)` eagerly copy coordinate and
box bytes. `structures.copy(deep=False)` and `copy.copy(structures)` share
protected blocks and replace affected blocks before editing. Both modes own
independent mutable metadata and other series. Copying invokes no constructor,
legacy restoration or form discovery, and preserves the concrete supported type.
Standalone copies drop their weak owner link; complete `MolSys` copies rebind
their copied structure domain to the copied system. Holding a structure domain
does not keep its former owner alive.

Blocks are dimensioned by an internal byte budget with at least one complete
structure per block. A small edit copies its affected blocks rather than every
coordinate; that may still include several small structures or one large
structure. Block size is an implementation detail, not a fixed public guarantee.
Copies do not retain a hidden complete base array after local replacements.
Initial storage captures caller values independently without changing the
caller's array flags. Owned query outputs can be edited without changing either
the source or its copy.

The H5MSM 0.5 coordinate/box reader, writer and append path transfer bounded
numeric blocks. Loading a resident object still requires memory for its complete
requested data, but avoids an additional complete coordinate staging array.
File schemas and canonical nm units are unchanged. This is resident storage,
not an object that queries coordinates lazily from disk.

This protocol also underlies {ref}`MolSys copies <user-foundations-molsys-copying>`
and complements {ref}`interaction analyses <user-tools-interactions-copying>`.
Editing an attached `molsys.structures` directly still requires explicit invalidation of
the owner's analyses; the automatic boundary is `msm.set(molsys, ...)`. See
{ref}`Changing coordinates <user-tools-interactions-coordinate-edits>`.

---

## API Documentation

Geometry can be evaluated from Structures without topology or chemical-state
metadata. For example, plane fitting produces centroids, unoriented normals and
orthogonal deviations for whole atom selections. Planarity alone does not
establish aromaticity. Coordinate streaming and resident calculated output are
separate memory costs; explicit source atom and structure indices preserve their
meaning in a Structures-only H5MSM 0.5 file. See {ref}`Tutorial_Get_least_squares_plane` for
executed examples and PBC requirements.

See {ref}`API Native Queries` for resident-object queries and
{func}`molsysmt.basic.convert` for form-agnostic conversion.

## Native Queries

Use `structures.get(element="atom", selection=[...], structure_indices=[...], coordinates=True)` for selected quantities. Existing `get_coordinates()`, `get_box()` and `get_time()` remain available. General get/info options and output units follow the basic query contract. Native `info()` supports Styler, DataFrame and dictionary records. See {ref}`Tutorial_Get` and {ref}`Tutorial_Info`.
