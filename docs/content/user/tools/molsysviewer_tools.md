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
prerequisites and engine limitations remain applicable. The contributing
source-group mapping repair is received below. This receiving is not a certification of every possible input or engine.
Topology functions keep their module path; they do not gain invented root aliases.
The current `view.addons.molsysmt.structure` slice adds `get_distances`,
`get_vectors`, `get_center`, `get_radius_of_gyration`, `get_angles`,
`get_dihedral_angles`, `get_rmsd`, `get_least_rmsd`, `get_principal_axes` and
`get_least_squares_plane`, `get_maximum_distances`, `get_contacts`, `get_rmsf`,
`get_minimum_distances`, `get_neighbors`, `get_symmetry_corrected_rmsd`,
`get_secondary_structure` and `principal_component_analysis`.
Results retain native quantities, arrays and metadata. The separate
`structure.translate`, `structure.rotate`, `structure.flip`, `structure.least_rmsd_fit`,
`structure.least_rmsd_align`, `structure.center`, `structure.move_away` and
`structure.align_principal_axes`, `structure.set_dihedral_angles` and
`structure.shift_dihedral_angles` wrappers receive independent outputs and managed
in-place coordinate changes. Sequence alignment receives the native self-reference and atom-index/mask
repairs documented below. Reflection receiving includes the default z normal and finite nonzero scaled normals,
with native pre-write rejection of invalid planes. Displacement receiving covers single-structure, finite nonzero directions; undefined directions and unsupported axes reject before native coordinate writes. The reviewed structure namespace now has explicit wrappers for all 28 native function exports; torsion input/block limitations below remain unqualified. This is source exposure and bounded receiving, not unconditional scientific or package compatibility.

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

## Querying minima and neighborhoods

```python
with msv.demo['pentalanine'] as view:
    structure = view.addons.molsysmt.structure
    nearest_positions, minimum_distances = structure.get_minimum_distances(
        selection=[25, 10, 0], selection_2=[4, 2],
        structure_indices=[2, 0, 2], pbc=False,
    )
    nearest_neighbors, neighbor_distances = structure.get_neighbors(
        selection=[25, 10, 0], selection_2=[4, 2],
        structure_indices=[2, 0, 2], n_neighbors=1, pbc=False,
    )
    within_cutoff, cutoff_distances = structure.get_neighbors(
        selection=[25, 10, 0], selection_2=[4, 2],
        structure_indices=[2, 0, 2], threshold='0.6 nm', pbc=False,
    )
```

{doc}`structure/get_minimum_distances` returns positions local to the selected
populations or explicit pair list, plus length quantities. The entity flags
choose which population axes are reduced. Independent `weights` and `weights_2`
retain their native meaning when computing centers. No endpoint indices are
silently converted into global atom indices.

{doc}`structure/get_neighbors` accepts exactly one search criterion: `threshold`
or `n_neighbors`. Its ordinary array output gives target positions relative to
the second selected population, with fixed-size count results or ragged cutoff
results. Native supported pairs/atom-index and CSR outputs remain available;
unsupported combinations retain native errors. Self-exclusion applies according
to the native source/selection identity contract, not simply to every zero
distance. An explicit `molecular_system_2` remains caller-owned and can use its
own selection and matching structure-index list. Matching index values do not
make two different sources the same system.

The wrappers reuse the native criterion-admission contract before forwarding
defaults, so an omitted search criterion stays omitted. They do not choose a
cutoff, count, engine or alternative scientific route. Both tools read the
current primary MolSys, including pending managed edits, without synchronizing
the scene, adopting data or attaching an analysis.

The fixes tracked by [#444](https://github.com/uibcdf/molsysmt/issues/444) and
[#445](https://github.com/uibcdf/molsysmt/issues/445) are committed in the native
owner and have source receiving in the addon. This is not a published-package
compatibility claim. The original working-tree evidence and follow-up are retained
in the receiving record. Other unlisted
structure operations remain unreceived.


## Assigning secondary structure

```python
with msv.demo['pentalanine'] as view:
    codes = view.addons.molsysmt.structure.get_secondary_structure(
        selection=[3, 1, 3], structure_indices=[2, 0, 2],
        simplified=True, engine='MDTraj',
    )
```

{doc}`structure/get_secondary_structure` uses MDTraj's DSSP implementation.
MDTraj must be available for this explicitly selected route. Codes belong to
groups, with structures on the first output axis. Unlike atom-population metric
queries, numeric selections here address group indices. The native selected
groups are unique and ordered by group index; the example returns groups 1 and
3. Simplified codes are H, E, C and NA; full codes retain DSSP distinctions and
nonprotein groups retain NA. The wrapper does not color or annotate the scene.
Its extra keyword-only skip_digestion controls addon digestion only; native
scientific validation still runs. No second engine is silently selected.

## Comparing chemically equivalent poses

```python
import molsysmt as msm

# You explicitly provide chemistry suitable for the declared matching method.
molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol')
with msv.new_view(molsys) as view:
    matches = view.addons.molsysmt.topology.get_atom_correspondences()
    pose = view.addons.molsysmt.structure.get_symmetry_corrected_rmsd(
        selection='all', correspondences=matches, structure_indices=[0], heavy_mode='off',
    )
```

{doc}`structure/get_symmetry_corrected_rmsd` returns the native result dictionary:
length-valued RMSD, selected structures, winning correspondence indices,
near-optimal counts, search scope, method/software and scientific attribution.
The correspondence table is shared across observations rather than copied for
every structure. The dictionary retains detached native result ownership.
RDKit and sufficient declared chemical context are prerequisites; the addon
does not infer missing chemistry or add hydrogens.

Keep reference systems, populations and reference structure indices explicit
when needed. Cached correspondences must still match the current chemistry.
Anchors and supplied candidate maps restrict the scientific search scope; the
result need not be the unrestricted chemical minimum. A raw baseline is computed
only when its correspondence is explicitly provided. No fitting, centering,
rotation or periodic imaging occurs: compare poses in the intended common
coordinate frame. Native bounds and experimental method classification remain
visible; this wrapper does not promote the method's scientific stability.

## Computing principal components

```python
import numpy as np

with msv.demo['pentalanine'] as view:
    eigenvectors, eigenvalues = view.addons.molsysmt.structure.principal_component_analysis(
        selection=[0, 2, 4], structure_indices=[2, 0, 2],
        weights=np.array([1., 3., 2.]), use_gpu=False,
    )
```

{doc}`structure/principal_component_analysis` returns one eigenvector per row,
ordered by descending eigenvalue. Features contain all selected x coordinates,
then y, then z. Eigenvalues retain squared-length units, normally nm**2.
Numeric weights scale the centered covariance as defined by the native method;
they are not normalized or reinterpreted by the wrapper. Eigenvector signs and
bases within degenerate subspaces are not unique. Use covariance reconstruction
or subspace comparisons instead of requiring identical degenerate vectors.

PCA centers features over the requested structures; it does not align molecular
structures, edit coordinates, project the trajectory or draw modes. Prepare the
scientifically intended coordinate frame explicitly. The native covariance is
dense in 3*n_atoms features, so this is not a general bounded-memory trajectory
API. CPU use_gpu=False is qualified here; optional GPU execution has separate
requirements.

The native repair of [#448](https://github.com/uibcdf/molsysmt/issues/448) is
received. Numerical lists, tuples and supported array dtypes, including strided
or read-only arrays, are normalized by MolSysMT. Dimensionless quantity weights
retain their physical numerical factors. Invalid lengths, nonfinite/negative or
all-zero weights and dimensioned quantities reject before native computation.
The addon forwards inputs unchanged; it adds no scientific normalization rule.
This receiving qualifies the CPU route, with squared-unit and covariance checks.



## Translating coordinates

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    shifted = tools.structure.translate(translation='[1, 0, 0] nm')
    # The independent result is returned to Python; view.molsys stays in the view.
    tools.structure.translate(
        translation='[0, 1, 0] angstrom', selection='backbone',
        structure_indices=[2, 0], in_place=True, update_view=False,
    )
    pending = tools.get_sync_status()
    tools.sync_view()
```

{doc}`structure/translate` preserves the native in_place=False default and result
ownership. Independent results are never adopted by update_view. To edit the
bound system, request in_place=True; successful translation returns native None.
The default update_view=True reconciles geometry immediately. False leaves
completed scientific edits pending until sync_view(), which never repeats the
translation. Reads use pending coordinates; stale scene/index actions are blocked.

Translation quantities, shape broadcasting, atom selections and structure order
remain native. Supported shapes describe one vector, one vector per selected
structure, or one vector per selected atom and structure. Repeated indices use
the native last supplied value, without added accumulation or deduplication.
The box and atom/structure identities stay fixed. Regions, selections, anchored
shapes, navigation and source accounting survive reconciliation. Native coordinate
setters invalidate named interaction coverage only on edited structures; no
detector runs automatically. Independent output may copy the system according
to the native contract; in-place integration adds no full trajectory copy.

A display failure after successful science raises SystemEditSyncError with
science_completed=True and scientific_result, which is None here. Retry
tools.sync_view() instead of the translation. A possible partial scientific write
enters uncertain state and requires explicit recovery, without an implied rollback.
The skip_digestion flag cannot bypass integration ownership or branch controls.

Native centering is resolved in [#451](https://github.com/uibcdf/molsysmt/issues/451)
with explicit source/destination centers and a consistent in-place None return.
See {ref}`Tutorial_Center` for the new pre-1.0 argument names and containment rules.
The bound structure.center wrapper now receives that exact native contract,
with source containment, initial destinations, weights and native return ownership.
The addon supplies no alternate formula, legacy keyword alias or hidden selection.


## Rotating and reflecting coordinates

Use a proper rotation to change orientation while preserving distances and
handedness. Reflection across a plane is a different operation: it preserves
distances for a unit plane normal but can invert molecular chirality. Neither
operation rotates the periodic box or updates chemical-state assignments.

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    rotated = tools.structure.rotate(
        rotation=[[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        rotation_center='[0.1, 0.2, 0.3] nm',
    )
    # An independent reflected system is returned; the current view stays loaded.
    reflected = tools.structure.flip(vector=[1, 0, 0], point='[0, 0, 0] nm')
    tools.structure.rotate(
        rotation=[[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        selection='backbone', structure_indices=[2, 0],
        in_place=True, update_view=False,
    )
    tools.sync_view()
```

{doc}`structure/rotate` retains native proper-matrix validation, active row-vector
conventions, matrix broadcasting and rotation-like objects with apply(). The
rotation center carries length units. Repeated and nonconsecutive selections keep
native ordering and last supplied coordinate assignments. No matrix conversion,
normalization or alternate algorithm is introduced by the addon.

{doc}`structure/flip` retains native arguments and scientific results. The None
default uses [0, 0, 1]. Native validation normalizes finite nonzero normals, so
[2, 0, 0] and [-1, 0, 0] describe the same plane as [1, 0, 0]. Zero/nonfinite
normals and invalid plane points reject before coordinate publication, preserving
coordinates, boxes and interaction coverage. The native repair is tracked in
[#460](https://github.com/uibcdf/molsysmt/issues/460); the addon forwards its
inputs and does not implement a reflection formula. One finite length-bearing
point defines the plane for all requested structures. Reflection reverses
handedness and leaves stored chemical assignments unchanged. The native flip
signature has no declared skip_digestion: the addon's keyword-only flag controls
addon digestion only and never disables the native boundary.

Both wrappers preserve in_place=False by default. update_view does not adopt an
independent result. In-place edits return None; update_view=True synchronizes the
scene, and False leaves pending work for sync_view(). The same retained identity,
selective interaction invalidation, deferred composition and failure-recovery
contract as translation applies. A synchronization-only retry must not repeat a
rotation or reflection: doing so would execute the science a second time.


## Fitting and sequence-based alignment

Use {doc}`structure/least_rmsd_fit` when you can specify corresponding atoms.
selection_fit and reference_selection_fit are the ordered fit anchors; selection
is the population moved by the resulting rigid transform. Those populations can
be different. Native rank and correspondence checks remain applicable.

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    reference = tools.basic.extract(structure_indices=[0])
    fitted = tools.structure.least_rmsd_fit(
        selection='all', selection_fit='backbone',
        reference_molecular_system=reference, reference_structure_index=0,
        use_gpu=False,
    )
    # The independent result stays in Python; the current view is not replaced.
    tools.structure.least_rmsd_align(
        selection="atom_name=='CA'", reference_molecular_system=reference,
        reference_structure_index=0, in_place=True, update_view=False,
        use_gpu=False,
    )
    tools.sync_view()
```

{doc}`structure/least_rmsd_align` derives correspondence through the declared
sequence-alignment engine. Its selection and reference_selection identify fit
anchors; **complete selected components move**, including their non-anchor atoms.
Other components remain unchanged. Biopython is the native sequence-engine
prerequisite, not an implicit preparation step performed by the addon.

Both tools preserve native in_place=False, native returns, structure ordering,
reference choices and configuration controls. Only independent least_rmsd_fit
output uses to_form; requesting conversion never adopts the result into the
view. An in-place call returns None. update_view=False defers projection only;
sync_view() reconciles the completed science without fitting again. Other view
state, retained object identity, native selected-structure interaction invalidation
and uncertain/synchronization-failure recovery follow the geometry contract above.
The native fit may publish through more than one coordinate setter; a scientific
interruption does not imply rollback.

The reference is caller-owned and must remain stable during the call. The addon
serializes its primary view only: it neither locks nor synchronizes another view
whose molecular system you pass as reference. An independent fit can read pending
primary coordinates; it does not project them or adopt its output. Explicit
coordinate-only native references and independent output forms retain native
units and ownership. No periodic reimaging, atom-correspondence heuristic, box
transformation or chemical preparation is added.

Native least_rmsd_align now preserves omitted/None self-reference using the
original reference_structure_index, including in-place fits. Atomic index lists,
tuples, arrays and full-axis Boolean masks use the query and reference atom axes;
they are projected to original sequence groups and paired atom names by MolSysMT.
The addon forwards these inputs unchanged and does not calculate correspondence
or replace a reference. Repairs and their native guards are tracked in
[#452](https://github.com/uibcdf/molsysmt/issues/452) and
[#453](https://github.com/uibcdf/molsysmt/issues/453). The same semantics are
received in the bound addon with actual scene and selected-structure checks.
This qualification covers CPU calls with explicit precision where tested; forwarding GPU/backend choices is not GPU qualification.


## Centering the current molecular system

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    centered = tools.structure.center(
        selection='backbone', source_center_selection="atom_name=='CA'",
    )
    # The independent centered MolSys stays in Python; the view is unchanged.
    tools.structure.center(
        selection='all', source_center_selection="atom_name=='CA'",
        target_coordinates='[1, 2, 3] angstrom',
        in_place=True, update_view=False,
    )
    tools.sync_view()
```

The three populations in {doc}`structure/center` all address the current
view.molsys. selection is the population moved by one rigid translation per
selected structure. source_center_selection defines the source center; None
uses the moving population, including repeated source indices and their weights.
Every source atom must belong to the moving population. Weights apply only to
that source: None gives its geometric center and 'masses' requests native masses.

Choose either a physical target_coordinates point (possibly one per selected
structure) or target_center_selection. The latter supplies its **initial geometric
center**, captured before any movement. A target population can be disjoint from
or overlap the atoms that move; its final center is not constrained to stay at
that initial position. To use a weighted destination, compute it explicitly with
get_center and pass its coordinates. Both destination modes together reject;
with neither, the destination is the origin.

Defaults and results remain native: in_place=False returns an independent system
without adoption, even when update_view=False. With in_place=True, science edits
the current system and returns None. update_view=True reconciles immediately;
False defers projection until sync_view(). Retained scene handles, sources and
structure navigation follow the managed geometry contract. Native coordinate
setters invalidate interaction coverage only for edited structures; no detector
runs. A failed projection is retried without a second centering calculation.
Potential scientific publication before an exception requires explicit recovery.

The native pre-1.0 redesign retired center_of_selection and center_coordinates;
the addon does not recreate those aliases. Source containment, destination/unit
validation, repeated-structure targets and residual refinement remain native.
No implicit periodic reconstruction or box transformation is added. See the
[placement recipe](../cookbook/placing_selected_centers.md) for the same native
population contract outside a view. The technical fix behind
[#451](https://github.com/uibcdf/molsysmt/issues/451) remains accepted; the requested
administrative closure comment is now restored.


## Moving away from a reference center

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    displaced = tools.structure.move_away(
        selection='all', center_of_selection="atom_name=='CA'",
        direction=[1, 0, 0], distance='2 angstroms', structure_indices=0,
    )
    # The independent result stays in Python; the view is unchanged.
    tools.structure.move_away(
        selection='all', center_of_selection="atom_name=='CA'",
        direction=[1, 0, 0], distance='2 angstroms', structure_indices=0,
        in_place=True, update_view=False,
    )
    tools.sync_view()
```

The bound `structure.move_away` mirrors {func}`molsysmt.structure.move_away`.
Its native default is one structure, index 0, and an independent output.
`selection` determines what moves. `center_of_selection` and its `weights`
determine the source center. These are this function's current native argument
names, distinct from the redesigned arguments of `structure.center`.
`reference_molecular_system=None` uses the current bound system;
`reference_center_of_selection`, `reference_weights` and
`reference_structure_indices` remain independent scientific inputs. A None
reference structure scope uses the moving structure scope. An external reference
remains caller-owned: keep it stable during the call; this addon does not lock or
synchronize another view.

The two direction modes have different meanings. Automatic direction adds the
requested distance along the existing reference-to-source vector; distance is
an **additional displacement**, not the final center separation. With an explicit
finite nonzero direction, native digestion normalizes it and places the source
at the **initial** reference center plus the requested offset. There is no
intermediate centering publication. The explicit
mode requires the source-center atoms to be contained in the moving population.
An overlapping reference is an initial snapshot, not a final constraint. No
periodic reconstruction, reference preparation or box transformation is added.

The addon receives single-structure nondegenerate calls with units and weights,
independent results and native None in-place returns. Native selected-structure
interaction invalidation is retained. Deferred projection, scene identity/maps
and retry after a display failure use the same controls as translation. Retry
`tools.sync_view()` after a projection failure; do not repeat completed science.

:::{warning}
Both modes require one structure and one center in each system. Multiple or
repeated structure requests reject before centering or displacement. Automatic
centers must be distinct and finite, even when distance is zero; explicit
vectors must be finite and nonzero. These rejections preserve coordinates,
boxes and stored interaction coverage and leave the managed scene synchronized.
The native NaN and partial-write defects tracked by
[#456](https://github.com/uibcdf/molsysmt/issues/456) and
[#457](https://github.com/uibcdf/molsysmt/issues/457) are repaired. The addon
forwards the native validation and supplies no substitute geometry. An unrelated
backend failure after actual publication still needs explicit recovery; display
retry must not repeat successful science.
:::


## Aligning principal axes

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    aligned = tools.structure.align_principal_axes(
        selection='all', principal_axes_of_selection="atom_name=='CA'",
        principal_axes_type='inertia', weights='masses', center=False,
    )
    # The independent native result does not replace view.molsys.
    tools.structure.align_principal_axes(
        selection='all', principal_axes_of_selection="atom_name=='CA'",
        principal_axes_type='geometric', structure_indices=[2, 0],
        axes=[[0, 1, 0], [0, 0, 1], [1, 0, 0]],
        center=True, in_place=True, update_view=False,
    )
    tools.sync_view()
```

{func}`molsysmt.structure.align_principal_axes` rotates the atoms in `selection`
using the axes of `principal_axes_of_selection`. None uses the moving population;
an explicit fitting population may overlap or be disjoint from the atoms moved.
All populations address the current bound system. A disjoint fitting population
stays unchanged: its **initial** geometry determines the transformation, rather
than defining a final constraint on atoms that do not move.

The native `principal_axes_type` selects inertia or geometric axes. Eigenvalues
are ordered increasingly within that definition. Individual eigenvector signs
are mathematically arbitrary; repeated principal moments do not define unique
individual axes and reject. The target `axes` are three **row vectors** forming
a right-handed orthonormal basis; None requests the Cartesian basis. The native
operation owns weights, axis signs, degeneracy tolerance and basis validation.
`weights` apply to the fitting population, including native mass weighting.
No eigenvalue correction or eigensolver is supplied by this addon.

By default `center=False`, the rotation uses and restores the initial weighted
fitting center. With `center=True`, that center is subtracted without restoration.
When fitting atoms move along with the selection this places their weighted
center at the origin; it does not promise to center a fitting population that
was deliberately excluded from movement. Both modes preserve relative distances
and handedness within the moved population. They do not rotate the periodic
box, wrap components or prepare periodic coordinates.

Native `in_place=False` returns an independent result; `in_place=True` edits the
bound system and returns None. Nonconsecutive/repeated structures retain native
ordering and selected-structure interaction invalidation. `update_view` controls
only projection. A deferred sequence preserves scene correspondence and is
finished with `sync_view()`; synchronization retry does not repeat the alignment.

The native function currently has no `skip_digestion` argument. The addon's
keyword-only flag controls its own digestion only: native validation always
runs, including when that flag is True. Invalid target bases, degenerate moments
and rejected inputs keep their native exceptions; a possible scientific partial
write and a failed display projection retain their separate recovery contracts.


## Editing dihedral angles

```python
with msv.demo['pentalanine'] as view:
    tools = view.addons.molsysmt
    quartets = tools.topology.get_dihedral_quartets(phi=True)
    # Keep this one quartet explicit; input angles carry physical angular units.
    edited = tools.structure.set_dihedral_angles(
        dihedral_quartets=quartets[0], angles='60 degrees',
        structure_indices=[0], pbc=False,
    )
    # Independent outputs are returned without replacing the view's system.
    tools.structure.shift_dihedral_angles(
        dihedral_quartets=quartets[0], shifts='15 degrees',
        structure_indices=[0], pbc=False, in_place=True, update_view=False,
    )
    tools.sync_view()
```

{func}`molsysmt.structure.set_dihedral_angles` sets absolute targets;
{func}`molsysmt.structure.shift_dihedral_angles` adds signed angular increments
to the current torsions. Supply ordered atom-index quartets and unit-bearing
angles/shifts. Missing required scientific inputs retain native rejection; the
addon does not infer phi/psi or a preparation workflow. Native `pbc=True` is the
default; use the same periodic convention when measuring and editing. With no
box the native editor falls back to nonperiodic geometry. No box is created,
rotated or changed by the addon.

Automatic blocks come from the native connectivity owner after cutting each
central bond; atoms on the fourth atom's side are rotated. This is a coordinate
edit, not bond deletion or force-field minimization. The receiving layer only
declares retained atom/structure identities and possible coordinate publication;
it does not recompute graph cuts, rewrite quartets or guess a moving selection.
Changes to bond lengths across a deliberately limited explicit block are the
caller's scientific choice, not automatically repaired geometry.

The setter receives its native angle broadcasting, including size-one axes,
and explicit atom-index block collections as understood by that tool. Other
structures and boxes stay unchanged. Native structure ordering/repetitions and
last publication semantics remain intact. Shifts are added by the native tool
before delegation to the setter; no extra accumulation is introduced for repeated
structure indices. General block objects from another tool must match the
editor's actual native input contract; the addon does not reshape ragged data.

Both editors retain native `in_place=False`: return the independent MolSys
without adoption. `in_place=True` returns None and reconciles admitted geometry
by default; `update_view=False` defers only projection. Native coordinate setters
invalidate stored interactions on edited structures. Regions, selections,
anchored shapes, sources and current-structure navigation use the same managed
correspondence as other coordinate edits. Retry `sync_view()` after a display
failure, without repeating the already completed torsion operation. Possible
partial scientific writes still require explicit recovery.

The setter has no native `skip_digestion` parameter: its addon-only keyword
controls local digestion while native public validation still runs. The shifter
retains its native declared flag. Neither flag bypasses integration controls.

:::{warning}
At this receiving source, native nonfinite angle values can generate nonfinite
coordinates. Supply finite valid torsions; those invalid-input routes are not
qualified. Native `shift_dihedral_angles` also ignores explicit `blocks` when
calling its setter, so that explicit-block shifter route is not qualified.
`set_dihedral_angles` with explicit blocks is separately tested. The addon
forwards native behavior and supplies no silent replacement calculation.
These findings are tracked in
[#461](https://github.com/uibcdf/molsysmt/issues/461) and
[#462](https://github.com/uibcdf/molsysmt/issues/462). They prevent declaring unconditional completion of the
scientific family despite complete function exposure.
:::
