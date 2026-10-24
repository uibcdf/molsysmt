(user-tools-molsysviewer)=
# MolSysViewer tools addon

Use MolSysMT tools on the molecular system already loaded in your view. The
expert API follows MolSysMT's module/function hierarchy, with `view.molsys`
supplied as the primary input.

## Availability

The experimental source implementation provides six queries under
`view.addons.molsysmt.basic`: `get`, `select`, `info`, `get_attributes`,
`has_attribute` and `get_label`, plus independent extraction with `extract`,
managed native removal with `remove`, the coordinates/box routes of `set`,
and native `copy`, `convert` and `get_conversion_report`. Presence/composition
checks `contains`, `is_composed_of` and the read-only `compare` route are also
received; the topology-rebuilding comparison mode remains pending. Identification
helpers `get_form`, `is_a_molecular_system`, `where_is_attribute` and the explicit
collection utility `are_multiple_molecular_systems` are also available in source.
Their root aliases are also available, such as `view.addons.molsysmt.get`.

The current `view.addons.molsysmt.topology` namespace wraps all eleven native
exports at the reviewed baseline: bond graphs, covalent blocks/paths, dihedral
quartets, rings, rigid fragments, rotatable bonds, SMARTS matches, atom
correspondences, sequence alignment and sequence identity. Native scientific
limitations remain applicable, including the sequence/group mapping limitation
below. This receiving is not a certification of every possible input or engine.
Topology functions keep their module path; they do not gain invented root aliases.
The current `view.addons.molsysmt.structure` slice adds `get_distances`,
`get_vectors`, `get_center`, `get_radius_of_gyration`, `get_angles`,
`get_dihedral_angles`, `get_rmsd`, `get_least_rmsd`, `get_principal_axes` and
`get_least_squares_plane`, `get_maximum_distances`, `get_contacts` and `get_rmsf`.
Results retain native quantities, arrays and metadata;
coordinate-changing operations remain outside this received slice.

Other scientific modules, editing families and graphical task panels
are still being implemented. This is not a complete MolSysMT mirror
or a claim that the currently published package pair contains these tools.

Install compatible versions of both components. MolSysMT supplies the
integration; MolSysViewer discovers its declared entry point automatically.
Source checkouts need current generated distribution metadata as well as an
editable installation after an entry-point change. No manual registration is needed in a correctly installed compatible
environment. Ordinary MolSysMT import and the core visualization backend work
independently of this optional interface.

## Querying the current system

```python
import molsysviewer as msv

with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    count = tools.basic.get(n_atoms=True)
    atoms = tools.basic.select(selection="atom_type=='N'")
    coordinates = tools.basic.get(
        element="atom", selection=atoms,
        structure_indices=[2, 0], coordinates=True,
    )
    summary = tools.basic.info(output_type="dictionary")
```

Coordinates retain the native physical quantity and structure order; the
standard MolSysMT length unit is nm. Scientific choices, defaults, result types,
errors and mutable-result ownership follow the native function. These wrappers
add no whole-trajectory copy or scene update. Native calculation/cache behavior
is unchanged; for example, `get_missing_bonds` retains its documented meaning.

| Bound tool | Native parameter and result reference |
| --- | --- |
| `tools.basic.get(...)` | {doc}`basic/get` |
| `tools.basic.select(...)` | {doc}`basic/select` |
| `tools.basic.info(...)` | {doc}`basic/info` |
| `tools.basic.get_attributes(...)` | {doc}`basic/get_attributes` |
| `tools.basic.has_attribute(...)` | {doc}`basic/has_attribute` |
| `tools.basic.get_label(...)` | {doc}`basic/get_label` |

The bound methods omit the primary `molecular_system` argument. You cannot
override it with another system. Inspect a signature or call `help` on the
method for the remaining native parameters. `skip_digestion` keeps the native
trusted-call contract; it does not bypass view lifetime checks.

## Identifying systems and locating attributes

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    resident_form = tools.basic.get_form()
    valid_single = tools.basic.is_a_molecular_system()
    molsys, owning_form = tools.basic.where_is_attribute("coordinates")
    with msv.MolSysView() as empty:
        valid_container = empty.addons.molsysmt.basic.are_multiple_molecular_systems(
            [molsys],
        )
```

{doc}`basic/get_form` identifies the current resident system, usually
`molsysmt.MolSys`, rather than the filename or original format passed to loading.
{doc}`basic/is_a_molecular_system` retains native input classification and
consistency checks; it is not a claim that the system is chemically complete or
ready for simulation.

{doc}`basic/where_is_attribute` returns the native item/form pair with its actual
`include_none` and fallback semantics. The item can be the current `view.molsys`
itself; it is a live reference, not a copied snapshot. Locating a possible owner
is not proof that an attribute currently has a non-None value. Use `has_attribute`
for the corresponding availability query. Later direct edits through the returned
item retain explicit reconciliation responsibilities.

{doc}`basic/are_multiple_molecular_systems` is an explicit-input utility: its
`molecular_systems` collection remains required. The addon never prefixes that
collection with the current system and does not merge items or load a result
into the view. Native inspection may still read the supplied inputs. It may
run on an empty view, but the owning view must remain open. Inputs are
caller-owned and must remain stable; this utility takes no managed-edit locks.
Native True for a one-item valid container does not mean there are at least two
systems, nor decide how sources should be composed or loaded.

Native `get_form`, `is_a_molecular_system` and `are_multiple_molecular_systems`
deliberately have no digestion escape-hatch parameter. Their addon wrappers add
keyword-only `skip_digestion=False` for the addon boundary only; they never pass
it to or redecorate the native helper. View lifetime checks still run. The
ordinary native `skip_digestion` parameter of `where_is_attribute` remains native.

## Checking composition and comparing systems

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    count = tools.basic.get(n_atoms=True)
    contains_minimum = tools.basic.contains(n_atoms=count - 1)
    matches_exact_count = tools.basic.is_composed_of(n_atoms=count)
    reference = tools.basic.copy()
    differences = tools.basic.compare(
        reference, output_type="dictionary", n_atoms=True, atom_name=True,
    )
```

{doc}`basic/contains` and {doc}`basic/is_composed_of` keep their native condition
semantics. For an integer `n_atoms` condition, the former checks a minimum count,
while the latter checks an exact count. Empty conditions, selections and attribute
synonyms retain native behavior; the addon adds no new interpretation of chemistry.

{doc}`basic/compare` binds only the first system. Pass `molecular_system_2`
explicitly, including when it is another view's molecular system. Keep the two
systems' selections and structure indices separate through `selection`,
`structure_indices`, `selection_2` and `structure_indices_2`. Dictionary output
and `attributes_type`'s native alias for `attribute_type` remain available.
An alias and its canonical argument are alternatives; supplying both is rejected,
even when the explicit canonical value equals its default.

The received comparison route uses `redefine_indices=False`. Native
`redefine_indices=True` forces topology rebuilding in **both** inputs, so it is
an editing operation that still needs separate receiving. The addon rejects it
before either system is changed, including with `skip_digestion=True`.
Use native MolSysMT and explicit reconciliation of affected views when you need
that mode. Other provider limitations and errors, such as the unimplemented
`rule="in"`, are preserved rather than replaced with fallback results.

These tools do not request a scene update or attach analyses. They may read a
pending molecular edit without synchronizing its scene. Native derived caches
retain their own behavior. Keep an explicitly supplied reference stable while
the call runs; this interface does not lock or transact across two views.

## Extracting a molecular subset

```python
with msv.demo["pentalanine"] as view:
    subset = view.addons.molsysmt.basic.extract(
        selection=[0, 2, 4], structure_indices=[2, 0, 2],
        to_form="molsysmt.MolSys",
    )
```

This returns the native molecular result and leaves the view unchanged. Structure
order and repetitions follow {doc}`basic/extract`, as do output formats/files,
units, attached-analysis projection and the `copy_if_all` ownership policy.
An unrestricted `copy_if_all=False` call may retain native shared/live-reference
behavior; the addon does not add a defensive copy or observe later direct writes.
`view.extract(...)` is a separate operation that returns a new view with migrated
scene state. Neither method implicitly adopts its result into the source view.

## Copying and converting the current system

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    snapshot = tools.basic.copy()
    subset = tools.basic.convert(
        selection=[0, 1, 2, 3], structure_indices=[2, 0],
    )
    reports = tools.basic.get_conversion_report(
        to_form=["molsysmt.MolSys", "molsysmt.Structures"],
        structure_indices=[2, 0],
    )
```

{doc}`basic/copy` returns the native independent copy. {doc}`basic/convert`
returns the requested molecular form, collection or file result, with native
selection, structure order and converter options. Neither replaces `view.molsys`
or copies the visual scene. With `return_report=True`, conversion returns its
native result/report pair. Target lists retain their requested order.
`copy_if_all=False` keeps the converter's sharing policy: a full native conversion
may return the current system itself. Later edits through that live reference
are outside automatic synchronization.

{doc}`basic/get_conversion_report` inspects potential losses without creating or
overwriting the destination. An existing destination may be inspected to identify
its form and can produce a native format error. Check each report's `outcome`,
`issues`, `audited_scopes` and `is_exhaustive`; a report is not an unconditional
guarantee that a format preserves every property. `strict=True` on conversion
rejects losses detected by the provider's preflight. It adds no rollback or atomic
publication guarantee across multiple files. Optional converters retain their
own dependencies and scientific limitations.

## Saving molecular data

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with msv.demo["pentalanine"] as view:
    with TemporaryDirectory() as directory:
        destination = Path(directory) / "system.h5msm"
        filename, report = view.addons.molsysmt.basic.convert(
            to_form=destination, structure_indices=[2, 0],
            return_report=True,
        )
        # Use the saved molecular file with ordinary MolSysMT tools.
        import molsysmt as msm
        restored = msm.convert(filename)
```

H5MSM 0.5 preserves the supported molecular domains and named Interactions.
Other formats are selected through native `to_form` and may retain fewer
properties; use a preflight report and the format reference before exporting.
Only native forms and H5MSM have addon-specific receiving in this delivery;
optional-format qualification remains with its converter owner.

A filename addresses the filesystem of the Python process. In a remote Jupyter
session it is a server path, not an automatic browser download. This operation
saves molecular data; use Viewer session/export tools to preserve the scene or
produce an interactive HTML view. No output is automatically adopted or displayed.
`copy(output_filename=...)` keeps native behavior: file-copy destinations are for
file-based inputs, so use `convert` to serialize the view's native MolSys.

## Removing atoms or structures

`remove` preserves {doc}`basic/remove`: `in_place=False` is the native default
and returns an independent molecular system. It does not replace `view.molsys`.
To edit the actual bound system and update its scene:

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    tools.basic.remove(selection=[0], in_place=True)
    tools.basic.remove(structure_indices=[1], in_place=True, update_view=False)
    status = tools.get_sync_status()  # pending: science is already complete
    tools.sync_view()                # update the scene, not the science
```

Successful in-place removal returns native `None`. The keyword-only
`update_view=True` default synchronizes immediately; False defers only visual
reconciliation. Compatible deferred removals compose their atom/structure maps.
Queries read the current edited MolSys, while scene actions using old indices
are blocked until synchronization. Live windows display an Update view action.

The initial receiver supports retained nonempty atom/structure axes. Removing
every atom or structure in place is rejected before scientific execution; use
`in_place=False` for independent empty outputs. Surviving analyses follow native
extraction/projection semantics and retain their original evaluated scope: they
are not new calculations. Regions, saved/active atom selections, shapes and
structure-bound scene data follow the receiving host's map policies. Textual
region/selection queries are reevaluated; explicit atom lists are remapped.

### A completed edit whose display update fails

A scene synchronization error does not mean the removal failed. The host raises
`molsysviewer.system_edits.SystemEditSyncError` with `science_completed=True`,
`operation_id` and `scientific_result` (native None for this removal). Its cause
identifies the projection failure. Call `tools.sync_view()` to retry; do not
repeat the removal. The facade does not permanently retain large results.

If a scientific exception may have left partial writes, status is `uncertain`;
unchanged counts do not certify correspondence. Explicit recovery through
`view.addons.manager.system_edits.replace(molecular_system)` discards pending
scene reconciliation and loads a replacement. This is not scientific Undo and
does not revert caller-held references to the old edited system. Ordinary
`view.load` cannot silently discard unresolved managed edits.

## Setting coordinates and periodic boxes

The source receiver admits `basic.set` for **coordinates** and **box**, with
the current atom and structure axes retained. Its native parameters/defaults
remain visible; `update_view=True` is the additional keyword-only integration
control. Native setting edits the bound system and returns None; it does not
need or invent an `in_place` flag.

```python
import numpy as np
from molsysmt import pyunitwizard as puw

with msv.demo["pentalanine"] as source:
    with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
        tools = view.addons.molsysmt
        coordinates = tools.basic.get(
            element="atom", selection=[2, 0],
            structure_indices=[2, 0], coordinates=True,
        )
        tools.basic.set(
            selection=[2, 0], structure_indices=[2, 0],
            coordinates=coordinates + puw.quantity(0.1, "nm"),
        )
        boxes = puw.quantity(np.tile(np.diag([3, 4, 5]), (3, 1, 1)), "nm")
        tools.basic.set(box=boxes, update_view=False)
        tools.sync_view()
```

Units, selection order and repeated-index writes follow {doc}`basic/set`.
Supply one coordinate block or box matrix per selected structure; no broadcast
is added. Coordinates use atom-level selection with element=None or atom;
element=system keeps native whole-system semantics and ignores atom selection.
Boxes require element=None or system. Initialize a missing box with all
structures before partial replacement; `tools.basic.set(box=None)` clears the
complete series. Coordinate-axis initialization/resizing/clearing and other
attributes are not received yet and fail before writing through this wrapper.

MolSysMT invalidates named interaction analyses only on edited structures,
including previously evaluated-empty ones. Unedited structures and earlier
snapshots remain available; setting geometry never recalculates a detector.
Valid empty selections are native no-ops. Geometry and removal edits can be
deferred together and reconciled once. The existing synchronization-failure and
uncertain-state recovery rules above also apply to this setter.

Multiple attributes are validated before delegation, but an unexpected error
after a native write may leave partial data. This route therefore requires a
host that checks nested geometry/analysis state on rejection; an older receiver
rejects the request before scientific execution. It does not promise scientific
rollback. To use other native attributes, first synchronize pending work, then
use MolSysMT with explicit Viewer reconciliation until their effects are received.

Native geometry storage replaces affected blocks. The current visual receiver
still rebuilds the scene when synchronizing, so a small setter request is not a
promise of incremental or bounded trajectory transfer to the browser.

## Exploring stored topology

```python
with msv.demo["pentalanine"] as view:
    topology = view.addons.molsysmt.topology
    graph = topology.get_bondgraph(structure_indices=[2, 0])
    blocks = topology.get_covalent_blocks()
    paths = topology.get_covalent_paths(path=[
        'atom_name=="C"', 'atom_name=="N"',
        'atom_name=="CA"', 'atom_name=="C"',
    ])
    phi_quartets, phi_blocks = topology.get_dihedral_quartets(
        phi=True, with_blocks=True,
    )
    hypothetical_blocks = topology.get_covalent_blocks(
        remove_bonds=phi_quartets[0][1:3],
    )
```

{doc}`topology/get_bondgraph` returns the native NetworkX graph with source atom
indices as nodes. The graph is an independent result; changing it does not change
the system's bonds. {doc}`topology/get_covalent_blocks` returns native sets or
source-index label arrays. `remove_bonds` cuts the analysis graph only: it neither
removes molecular bonds nor defines scene regions.

{doc}`topology/get_covalent_paths` takes an explicit ordered selection pattern.
{doc}`topology/get_dihedral_quartets` takes native dihedral flags such as `phi`
and `psi`. Request the intended type explicitly. Its `with_blocks=True` result
keeps the native lists of sets with different sizes; the addon does not coerce
that ragged data into a rectangular array.

Selection, output, chemical-state and structure options remain those declared by
each native function. A reference-state graph is one connectivity graph, not an
automatically calculated graph per displayed structure. Paths/quartets do not
acquire new state or structure parameters absent from their native interfaces.
No topology is prepared, connectivity certified complete, analysis attached or
scene updated by these wrappers. Native derived/cache behavior remains native.
The additional received graph and sequence tools are described below.

`get_bondgraph` and `get_covalent_blocks` forward native `skip_digestion`.
The native path/quartet signatures do not declare it, so their addon-only keyword
controls the wrapper boundary and is never inserted into scientific **kwargs.
Their native public validation remains active. The same view-lifetime and
pending-read rules apply to these calls as to the received `basic` readers.

## Reading chemical graphs and sequences

With sufficient declared chemistry, native graph tools also return ring
memberships, source-bond torsion classifications, explicit-cut fragments,
SMARTS matches and atom correspondences. They never fill missing chemical
metadata or apply their outputs to the scene. RDKit remains optional and is
required by SMARTS/correspondence matching; Biopython supplies sequence alignment.
The example below explicitly chooses the RDKit input-conversion route. That
choice belongs to the caller, not an implicit addon preparation step.

```python
import molsysmt as msm

molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol')
with msv.new_view(molsys) as view:
    topology = view.addons.molsysmt.topology
    rings = topology.get_rings()
    torsions = topology.get_rotatable_bonds(method='conjugation_restricted')
    fragments = topology.get_rigid_fragments(
        bond_indices=torsions['rotatable_bond_indices'],
    )
    matches = topology.get_substructure_matches(['[#8]', '[#9]'])
    n_atoms = view.addons.molsysmt.basic.get(n_atoms=True)
    identity_map = [[index, index] for index in range(n_atoms)]
    correspondence = topology.get_atom_correspondences(
        fixed_atom_correspondence=identity_map, max_matches=1,
    )
```

{doc}`topology/get_rings` returns sparse sorted memberships of a minimum cycle
basis, not every cycle or an aromaticity assignment. A partial-ring selection
can be rejected. Its block-size limit is not a universal RAM/runtime bound.
{doc}`topology/get_rotatable_bonds` retains explicit experimental graph criteria
and exclusions. {doc}`topology/get_rigid_fragments` cuts chosen source bond
indices analytically: it does not remove bonds or rotate coordinates. Packed
memberships and source-index arrays remain native, without becoming regions.

{doc}`topology/get_substructure_matches` keeps pattern order, query-column
order, empty matrix shapes and its pre-selection match bound.
{doc}`topology/get_atom_correspondences` preserves full chemical context,
independent reference selectors/states, source-index pairs, anchors, supplied
candidates, evidence and search limits. Its default None reference uses the
current system, as native MolSysMT does. It does not infer a visual alignment or
authorize adopting a different atom order. Caller-owned references must remain
stable; the addon does not lock another view. No truncated result is substituted
when a scientific search bound is exceeded.

```python
with msv.demo['pentalanine'] as view:
    reference = view.addons.molsysmt.basic.copy()
    topology = view.addons.molsysmt.topology
    amino_acids = "group_type=='amino acid'"
    aligned = topology.get_sequence_alignment(
        selection=amino_acids, reference_molecular_system=reference,
        reference_selection=amino_acids,
    )
    identity, groups, reference_groups = topology.get_sequence_identity(
        selection=amino_acids, reference_molecular_system=reference,
        reference_selection=amino_acids,
    )
```

{doc}`topology/get_sequence_alignment` preserves the native strings, engine,
alignment index and prettyprint branch, which prints and returns None.
{doc}`topology/get_sequence_identity` returns the native percentage and matched
source group lists. Current source resolves groups that actually contribute
sequence letters, so capped pentalanine self-comparison is 100 percent and
returns source groups [1, 2, 3, 4, 5]. Native empty/pre-gapped selection errors
remain explicit. The repaired native helper declares keyword-only skip_digestion;
the bound method forwards it, preserving all six historical native positional
slots. This is native receiving of
[#439](https://github.com/uibcdf/molsysmt/issues/439), not an addon identity formula.
No sequence result edits topology, fits coordinates or selects scene objects.

## Reusing tool references

A cached `tools` object or method resolves the current `view.molsys` when each
call begins. After `view.load(..., mode="replace")`, later queries use the
replacement system. The facade does not keep a second authoritative MolSys.
Each view has its own binding. Disabling the addon's graphical activation does
not disable expert Python queries. Closing the view makes bound queries fail;
an empty view must first load a molecular system.

Results are native scientific values. These queries do not create scene objects
or attach every result automatically. Use the visual owners in MolSysViewer for
regions, selections, measurements or Interactions. General direct edits made
with MolSysMT or through returned live references retain explicit reconciliation
responsibilities. Only admitted addon writers coordinate their edits; there is
no observer for arbitrary external writes.

## Host and author documentation

MolSysViewer documents discovery, activation, configuration, lifecycle, its
addon catalogue and how to create an addon in its
[addon guide](https://www.uibcdf.org/molsysviewer/content/user/introduction/addons.html).
This MolSysMT guide owns the capabilities and use of the MolSysMT tools addon.

## Computing geometry on the current system

The structure wrappers keep atom/structure selections, endpoint order, weights,
periodic choices, native output formats and execution controls explicit. They
return native results without attaching a measurement, selecting atoms or
changing coordinates. The additional `molecular_system_2` of distances/vectors
is an ordinary caller-owned input with its own selectors; it is not implicitly
the displayed system or another locked view.

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    distances = structure.get_distances(
        selection=[0, 2, 4], selection_2=[1, 3],
        structure_indices=[2, 0, 2], pbc=False, heavy_mode='off',
    )
    directed = structure.get_vectors(
        selection=[0, 2, 4], selection_2=[1, 3],
        structure_indices=[2, 0, 2], pbc=False, output_type='dictionary',
    )
```

{doc}`structure/get_distances` keeps native Cartesian/pair and array/dictionary
choices, including their supported index conventions and exceptions.
{doc}`structure/get_vectors` points from the first endpoint to the second,
retaining sparse endpoint memberships, both structure axes, periodic images,
distances and directions in dictionary output. Zero-length vectors retain
undefined NaN directions. Indices are source positions, not scene object IDs.
Repeated/nonconsecutive structure choices and auxiliary selectors stay native.

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    centers = structure.get_center(
        selection=[[0, 2], [4, 5]], structure_indices=[2, 0],
        weights='masses', heavy_mode='off',
    )
    radii = structure.get_radius_of_gyration(
        selection="atom_type!='H'", structure_indices=[2, 0],
        weights='masses', heavy_mode='off', use_gpu=False,
    )
```

{doc}`structure/get_center` returns geometric or weighted centers; it does not
center the molecule. Nested atom selections retain separate centers and native
weight interpretation. {doc}`structure/get_radius_of_gyration` returns one
length quantity per selected structure. Neither aligns, unwraps or prepares
coordinates. Inspect or explicitly convert physical units with PyUnitWizard;
the addon does not convert quantities to bare arrays or impose display units.

The current source repairs native heavy endpoint populations and physical-unit
attribution for distances, radius of gyration and RMSF
([#441](https://github.com/uibcdf/molsysmt/issues/441),
[#440](https://github.com/uibcdf/molsysmt/issues/440),
[#442](https://github.com/uibcdf/molsysmt/issues/442)). These repairs are checked
from the addon against independent geometry and fluctuation references across
nm/angstrom/pm contexts and repeated structure scopes. No hidden mode or unit
correction is added by the addon. Native output/resource limits still apply;
source receiving does not qualify older published packages.

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    angles = structure.get_angles(
        triplets=[[0, 1, 2]], structure_indices=[2, 0, 2],
        pbc=False, use_gpu=False,
    )
    dihedrals = structure.get_dihedral_angles(
        phi=True, psi=True, structure_indices=[2, 0, 2],
        pbc=False, use_gpu=False,
    )
```

{doc}`structure/get_angles` retains explicit source atom triplets and
{doc}`structure/get_dihedral_angles` retains explicit quartets or named dihedral
flags. Multiple named types retain their native list and order. Angular
quantities follow the active standard-angle policy, including a PyUnitWizard
context; explicitly request radians or degrees when extracting numeric values.
The native dihedral function has no declared skip_digestion parameter: the
addon-only keyword controls addon validation and is never injected into named
scientific flags. Native public validation and view-lifetime checks remain active.

Backend, periodic and streaming behavior stays native; optional GPU routes were
not qualified by these CPU receiving examples. Chunked input processing does
not guarantee constant memory, and returned outputs can still scale with the
requested atom pairs and structures. These are calculations, not automatic
scene measurements or coordinate edits. Fitting transformations and other
unlisted structure tools still need individual addon receiving.


## Comparing structures without modifying their coordinates

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    reference = view.addons.molsysmt.basic.copy()
    raw_rmsd = structure.get_rmsd(
        selection='backbone', structure_indices=[2, 0, 2],
        reference_molecular_system=reference, reference_structure_index=0,
        heavy_mode='force', use_gpu=False,
    )
    minimum_rmsd = structure.get_least_rmsd(
        selection='backbone', structure_indices=[2, 0, 2],
        reference_molecular_system=reference, reference_structure_index=0,
        use_gpu=False,
    )
```

{doc}`structure/get_rmsd` measures deviations in the supplied coordinate frame;
no fit is performed. {doc}`structure/get_least_rmsd` computes the minimum after
an optimal superposition internally, returning a length quantity without
changing either system. It does not call a scene alignment or move the displayed
molecule. Explicit reference inputs, their atom selection and reference structure
index stay native and caller-owned; None retains native self-reference behavior.
Matching counts do not infer chemical atom correspondence. Both inputs must have
the intended order and coordinate conventions. No implicit PBC reconstruction,
preparation or alignment is added.

The native `get_rmsd` signature has no skip_digestion parameter. Its addon-only
keyword governs addon digestion and is never forwarded. Scientific validation
still runs. Quantities retain the actual native units; explicitly convert values
when a numeric consumer requires nm or another unit. Supported native streaming
and optional-engine limits remain native, not a universal RAM/GPU guarantee.

## Inspecting axes and fitting planes

```python
with msv.demo['pentalanine'] as view:
    axes, moments = view.addons.molsysmt.structure.get_principal_axes(
        selection='backbone', structure_indices=[2, 0, 2],
        principal_axes_type='geometric', use_gpu=False,
    )
```

{doc}`structure/get_principal_axes` returns native numeric arrays, including the
moment convention and numeric scale of the selected native coordinate/weight
route. The addon does not invent physical unit labels for bare moment arrays.
Axes are rows ordered by ascending eigenvalue, with a right-handed orthonormal
basis. Individual signs are arbitrary; repeated eigenvalues determine a subspace
rather than unique individual directions. Inspecting axes does not align coordinates.

```python
with msv.demo['pentalanine'] as view:
    planes = view.addons.molsysmt.structure.get_least_squares_plane(
        selection=[[0, 10, 25, 40], [4, 14, 27, 45]],
        structure_indices=[2, 0, 2], pbc=False, heavy_mode='force',
    )
```

{doc}`structure/get_least_squares_plane` returns native sparse source memberships,
structure indices, length-quantity centers/deviations and numeric normals. It
fits coordinates without inferring aromaticity, creating rings or adding a plane
shape to the scene. Degenerate groups, missing boxes and split periodic groups
retain their native rejection; no hidden unwrapping or fabricated normal follows.
An explicit empty structure scope retains native typed empty outputs. Plane
normals describe unoriented planes; a deterministic sign is not temporal continuity.

These metric/fitting queries preserve native selection/backend dependencies;
their numeric/property-selection receiving is not a blanket certification of
every selector or optional engine. Additional scientific calculations remain
separate from coordinate fitting, scene measurements and molecular preparation.


## Receiving maxima, contacts and fluctuations

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    farthest_positions, farthest_distances = structure.get_maximum_distances(
        selection=[25, 10, 0], selection_2=[0, 25],
        structure_indices=[2, 0, 2], as_entity=True, as_entity_2=False, pbc=False,
    )
    contact_map = structure.get_contacts(
        selection=[0, 10, 25], selection_2=[1, 14, 27],
        structure_indices=[2, 0, 2], threshold='0.6 nm',
        pbc=False, cell_list=True, use_gpu=False,
    )
    fluctuations = structure.get_rmsf(
        selection='backbone', structure_indices=[2, 0, 2], heavy_mode='force',
    )
```

{doc}`structure/get_maximum_distances` returns native endpoint positions and a
length quantity. Its positions are local to the selected populations or pair
list, not automatically global atom indices. `as_entity` and `as_entity_2`
retain native reduction semantics. The extra keyword-only skip_digestion on
this wrapper controls addon digestion only; the native helper has no declared
flag and still validates scientific arguments.

{doc}`structure/get_contacts` retains threshold quantities, native dense/cell-list
choices, pairs/maps and supported source-index mapping. It returns scientific
booleans or pair lists without drawing contacts. Optional GPU execution has not
been qualified by these CPU examples. Native errors and memory limits remain
native; a dense contact map can still scale with both endpoint populations.

{doc}`structure/get_rmsf` returns one length per selected atom. It does not align
structures, unwrap coordinates, create a color scale or attach a scientific
analysis. Prepare the intended common coordinate frame explicitly when that is
the scientific question. Current heavy-mode physical units are received against
independent variance calculations; no alternate formula is implemented here.

`get_minimum_distances` and `get_neighbors` remain pending new scientific-owner
repairs: independent second-center weights
([#444](https://github.com/uibcdf/molsysmt/issues/444)) and explicit second-system
neighbor inputs ([#445](https://github.com/uibcdf/molsysmt/issues/445)). The
maintainer requests a native pytest contract matrix across the four distance/
neighbor/extrema tools before consolidating that family. Existing fixed issues
are retained as history; these two new defects are not repaired by addon-side
parameter substitutions. Other unlisted structure operations remain unreceived.
