(user-tools-interactions-result)=
# Querying interaction results

Build an experimental `molsysmt.Interactions` result from observations that
have local atom and structure indices. By default these equal the source
system's indices; explicit source maps support a selected or reordered domain.
This class stores the
observations; it does not detect interactions or declare covalent bonds.

Construction and queries validate their arguments through ArgDigest. Counts and
indices must be integers: booleans and fractional values are rejected before
they can become different atom or structure indices. Integer lists, NumPy
arrays, empty selections and record generators remain supported. Existing
positional calls keep their argument order. The keyword-only
`skip_digestion=False` defaults to validation; use `True` only inside a pipeline
that has already checked the complete input contract. Stored cross-column
invariants and file/schema checks remain active on that route.

```python
import molsysmt as msm

records = [
    {
        "structure_index": 0,
        "interaction_type": "hbond",
        "participants": [
            {"role": "donor", "atom_indices": [0]},
            {"role": "hydrogen", "atom_indices": [1]},
            {"role": "acceptor", "atom_indices": [2]},
        ],
        "measurements": {"distance": 0.20},
    },
]
interactions = msm.Interactions.from_records(
    records, n_atoms=3, n_structures=3,
    evaluated_structure_indices=[0, 2],
    method="example", measure_units={"distance": "nm"},
)
```

The distance is in nanometers. Structure 2 was evaluated and has no observed
interactions; structure 1 was not evaluated. The result keeps that difference.
By default, the declared atom search scope is `internal` over all local atoms.
The caller must declare the actual search scope; the class cannot infer from
observed records whether a detector examined all possible participants.

For a search involving one selection and its surroundings, declare the
selection and the complete atom universe examined:

```python
scoped = msm.Interactions.from_records(
    records, n_atoms=4, n_structures=3,
    evaluated_structure_indices=[0, 2], method="example",
    measure_units={"distance": "nm"},
    evaluation_mode="incident", evaluation_atom_indices=[0],
    evaluation_universe_indices=[0, 1, 2],
)
assert scoped.evaluation_scope["universe_indices"].tolist() == [0, 1, 2]
```

`internal(A)` covers relations whose participant atoms all belong to `A`;
`incident(A)` covers relations with at least one participant atom in `A`;
`between(A, B)` covers relations touching each of two disjoint sets. In every
mode, all participants must belong to the declared universe. The declaration
applies uniformly to the listed evaluated structures. Analyses with distinct
scopes belong in separate named results. A structure marked evaluated and
empty is empty only within this declared search scope.

```python
interactions.query(structure_indices=[2, 0, 2]).to_dict()
interactions.query(atom_indices=[0], mode="involving_selection")
interactions.query(atom_indices=[0, 1, 2], mode="within_selection")
interactions.query(atom_indices=[0], mode="across_selection_boundary")
interactions.between_selections([0, 1], [2], exclusive=True)
```

`involving_selection` (the default) means at least one participating atom belongs
to the selection; `within_selection` requires every participating atom;
`across_selection_boundary` requires atoms inside and outside the selection.
These names describe the atom-selection boundary, not a molecular boundary.
For a ring, every constituent atom participates in these tests; a hydrogen bond
includes its donor, hydrogen and acceptor. Empty atom selections return no
observations in all three modes.
`between_selections(A, B)` requires at least one atom from each disjoint set. With
`exclusive=True`, every participant atom must belong to `A` or `B`.

Only these explicit query names are supported. `between_selections` is a separate
method, not a fourth value for `query(mode=...)`, because it needs two selections.
Queries preserve the scientific search that produced the analysis:
detector `selection_mode` and stored `evaluation_mode` still use `internal`,
`incident` and `between`. Existing H5MSM 0.5 and InteractionsDict files retain
those scientific values without migration or a schema change.

Each query returns a lightweight view. `to_dict()` provides typed occurrence
columns, explicit evaluated-structure indices, measurement units, and optional
periodic-image vectors. Use `relation(index)` to inspect the type and roles
referenced by a result's `relation_indices` column.

(user-tools-interactions-pages)=
## Inspecting bounded pages

Keep a query and project a small page instead of copying all its occurrences:

```python
view = interactions.query(structure_indices=[2, 0])
page = view.to_page(offset=0, limit=50, max_participant_atoms=10000)
assert page["total_count"] == view.n_interactions
assert page["occurrence_indices"].tolist() == [0]
assert page["participant_roles"] == ("donor", "hydrogen", "acceptor")
assert page["next_offset"] is None
```

`offset` refers to rows in this query's order, rather than complete-analysis
occurrence indices. Use `next_offset` to request the next page; it is `None`
when the current page is empty or reaches the end. A zero `limit` gives an empty
page with count and coverage. Negative, boolean and noninteger bounds raise.

The experimental schema `molsysmt.interactions.page@1` contains the occurrence
columns provided by `to_dict()`, plus a compact catalog of the page's relations.
`relation_catalog_indices` contains complete-analysis relation indices;
`relation_types` and `relation_participant_offsets` use positions in that compact
catalog. `participant_roles`, `participant_atom_offsets` and `participant_atoms`
encode its participant groups. Occurrence `relation_indices` remain in the
complete analysis's space; find their catalog positions with
`numpy.searchsorted(page["relation_catalog_indices"], page["relation_indices"])`.
Parallel observations retain distinct `occurrence_indices`. Measurements,
units, evidence and periodic images follow the page's occurrence order.

`max_participant_atoms` bounds the sum of constituent atoms over page occurrences,
counting a reused relation once per occurrence. An oversized page raises before
copying its participant definitions or images; reduce `limit` or explicitly
increase that budget. Empty arrays retain their dtypes and offsets start at zero.
Source maps and evaluated coverage share read-only arrays with the analysis.

Paging bounds additional occurrence and participant copies. Constructing the
query retains its own row-index array; optional query indexes and frame metadata
have separate costs. Edited analyses can page without packing all surviving
columns. `to_dict()` continues to copy every selected occurrence. A page is for
inspection; use `InteractionsDict` or H5MSM for complete persistence. Evaluated
coverage still refers to the analysis's declared `evaluation_scope`.

The aligned `occurrence_indices` column identifies each observation within
this named analysis, even when two observations share a structure and relation.
Filtering and an H5MSM round trip preserve these indices. Extracting or editing
the analysis creates a new set of indices; rebuild saved selections against
the new result. The current API does not expose a persistent revision token.
If any input observation supplies periodic-image vectors, every observation
in that result must supply them; missing vectors are not interpreted as zero
images.
Each vector applies to one participant in relation order. With the three box
vectors as rows in nanometers, add `image_vector @ box` to each constituent
atom's stored coordinate. A positive `[1, 0, 0]` adds the first box vector;
relative geometry uses the first participant as reference. All atoms in a
compound participant receive the same shift. These vectors do not unwrap a
ring split across a periodic boundary.

To transfer the **complete** result through MolSysMT's conversion system,
convert it to `molsysmt.InteractionsDict`:

```python
columns = msm.convert(interactions, to_form="molsysmt.InteractionsDict")
assert msm.get_form(columns) == "molsysmt.InteractionsDict"
restored = msm.convert(columns, to_form="molsysmt.Interactions")
assert restored.query(structure_indices=[2]).n_interactions == 0
```

`InteractionsDict.data` contains versioned NumPy columns for relations,
participants, occurrences, evaluated coverage, evidence, and measurements.
It avoids one Python dictionary per occurrence. It is a typed Python payload,
not JSON data. A query view's `to_dict()` has a different purpose: it reports
selected occurrences and cannot reconstruct the full result.

`interactions.software` maps producer software names to the versions used
when calculating the observations. Both hydrogen-bond and disulfide adapters record
`{"molsysmt": msm.__version__}` at calculation time. The dictionary also
appears in query projections and survives conversion, remapping, invalidation,
and H5MSM persistence. Saving or loading with another MolSysMT version does
not replace the producer version. Older results without this metadata expose
`{}`, meaning unknown. When constructing an analysis from an external
detector, you can declare its versions with `software={"detector_name": "1.2"}`.

## Inspecting execution provenance

`parameters` contains scientific criteria. `execution_records` describes how each
set of evaluated structures was calculated. Each record has a `structure_indices`
integer array and a `details` dictionary. Projected detectors record execution
mode, coordinate block count and memory policy. Unknown details appear as `{}`.

```python
runs = interactions.execution_records
assert runs[0]["structure_indices"].tolist() == sorted(
    interactions.evaluated_structure_indices.tolist())
assert runs[0]["details"] == {}  # This example declares no execution details.
```

A frame query restricts these records even when it has zero occurrences. After
partial recalculation, an analysis can contain records from several executions.
Changing a returned record does not modify the analysis. A stored block count
continues to describe the original execution after extraction or invalidation;
it is not a count of frames still present. H5MSM preserves these records.

New interaction payloads use codec version 2 inside H5MSM 0.5. Current readers
also load version 1 and move its recorded execution keys out of `parameters`.
Older MolSysMT builds supporting only codec 1 must be updated to read new files.

```python
interactions.save("observations.h5i")
restored = msm.Interactions.load("observations.h5i")
```

The standalone HDF5 file is versioned and separate from H5MSM. `load` reads
the complete result into memory. Saving writes active observations in small
numeric windows, including analyses with invalidated or recalculated structures.
It does not create or change a cache of complete occurrence columns. Existing
observations, frame metadata and HDF5 caches still occupy memory. Detectors
continue to return resident results; direct detector-to-file output,
append/resume and public lazy file-backed queries remain unavailable. The disulfide
candidate and both hydrogen-bond detectors have optional `Interactions`
outputs.

Use `remap()` to extract a complete result into new index spaces. A relation
survives only if all atoms in its participants survive. Repeated structure
indices make distinct output structures, and evaluated structures with no
occurrences stay marked as evaluated.

If a structure changes and its prior observations are stale, use
`invalidate_structures()` to remove its occurrences and mark it unevaluated
while keeping its positional structure index:

```python
invalidated = interactions.invalidate_structures([0])
assert invalidated.query(structure_indices=[0]).to_dict()[
    "evaluated_structure_indices"
].size == 0
```

This returns a result with independent validity and leaves existing query
views unchanged. It shares read-only columns instead of copying surviving
observations. Re-evaluate the affected structures before claiming that they
have no interactions.

Numeric storage, including the measurement mapping and its arrays, is read-only
and independent of the input buffers used to construct the result. To change
observations, construct another result; an `InteractionsDict` provides editable
interchange columns that can be converted back into a validated result.

Invalidating frames allocates coverage information rather than a new copy of
every observation. Partial invalidation keeps the underlying shared columns in
memory, including excluded rows. Queries do not return those rows. If no
observations survive, the new result drops its reference to the occurrence
storage; old results and views can still retain it.

Reading complete attributes such as `occurrence_structures`, `image_vectors`
or `measurements` after invalidation can pack and cache all surviving columns.
Use `query(...).to_dict()` for selected frames or atoms when you need only a
small result. Remapping and typed/pickle serialization can also pack the active data;
temporary packing for those operations is released afterward. This is not yet
an incremental writer or an editor for individual observations.

(user-tools-interactions-compaction)=
## Reclaiming retired observations

After invalidation or repeated recalculation, use `compact()` when you want to
release excluded observation storage:

```python
compacted = invalidated.compact()
assert compacted.evaluated_structure_indices.tolist() == [2]
assert compacted.n_interactions == 0
assert interactions.n_interactions == 1  # The original analysis is unchanged.
```

The returned full analysis preserves occurrence and relation indices, source
maps, coverage and provenance. Unused relation definitions stay in its catalog.
Queries and H5MSM saving work as before. Query views cannot be compacted.

Attach it explicitly if you want to replace a named analysis:
`molsys.interactions = {**molsys.interactions, "example": analysis.compact()}`.
Release references to the previous analysis and its query views to reclaim their
storage. Those snapshots otherwise remain valid and keep their old buffers.
Compacting builds new observation columns and needs memory for that output plus
a temporary copy of one column. It neither recalculates observations nor makes
unevaluated structures evaluated. Saving to H5MSM already writes active blocks
directly, so you do not need to compact before saving.

(user-tools-interactions-coordinate-edits)=
## Changing coordinates

When you call `msm.set(molsys, coordinates=..., structure_indices=...)` on a
native `MolSys`, every attached named analysis becomes **unevaluated in the
selected structures**. This applies even if you move just one atom, the atom
had no earlier interactions, or the frame previously had zero observations.
Other structures remain evaluated. Periodic box changes use the same rule.

MolSysMT does not run detectors automatically. A moved atom can form a new
interaction, and a moved ring member can change the geometry of its entire
ring. Checking only previous participants would miss these changes. Recalculate
the affected frame, considering the detector's complete declared atom scope.

| Operation on native `MolSys` | Effect on named analyses |
| --- | --- |
| Coordinates or box through `msm.set` | Selected frames become unevaluated. |
| Empty atom/frame selection, time or identifier edit | Results remain valid. |
| Scientific chemical-state edits through `msm.set`, or replacing `chemical_states` | All covered frames become unevaluated. |
| Changing `structure_chemical_state_index` | Selected frames become unevaluated. |
| Direct writes through arrays or separate domain objects | You must invalidate the owning analyses explicitly. |

For example, attach a synthetic result to matching coordinates, then move one
atom in a previously evaluated-empty frame:

```python
import numpy as np
from molsysmt.native import MolSys, Structures

molsys = MolSys(n_atoms=3)
molsys.structures = Structures(
    coordinates=msm.pyunitwizard.quantity(np.zeros((3, 3, 3)), "nm")
)
molsys.interactions = {"example": interactions}
previous_view = interactions.query(structure_indices=[0])

msm.set(molsys, selection=[2], structure_indices=[2],
        coordinates=msm.pyunitwizard.quantity([[[0.3, 0.0, 0.0]]], "nm"))

current = molsys.interactions["example"]
assert current.evaluated_structure_indices.tolist() == [0]
assert current.query(structure_indices=[2]).n_interactions == 0
assert current.query(structure_indices=[2]).to_dict()[
    "evaluated_structure_indices"
].size == 0  # Pending calculation, not an evaluated absence of interactions.
assert current.query(structure_indices=[0]).n_interactions == 1
assert previous_view.n_interactions == 1  # A snapshot of the earlier analysis.
```

For explicit coordinate writes outside that owner boundary, invalidate the
named analyses yourself:

```python
molsys.interactions = {
    name: analysis.invalidate_structures([0])
    for name, analysis in molsys.interactions.items()
}
```

### Recalculating selected frames

Calculate new observations for the changed frames with the appropriate detector,
using the same molecular system axes and the complete original atom search scope.
Then call `current.replace_structures(fresh)` and attach the returned analysis
under its original name. Every frame evaluated by `fresh` replaces all its old
observations. A recalculated frame with zero observations remains **evaluated**.
Other frames and previously held snapshots remain unchanged. Nothing is detected
or attached automatically.

For the synthetic example above, declare a new evaluated-empty result for frame 2:

```python
fresh = msm.Interactions.from_records(
    [], n_atoms=3, n_structures=3, evaluated_structure_indices=[2],
    method=interactions.method, parameters=interactions.parameters,
    software=interactions.software, source_id=interactions.source_id,
    measure_units=interactions.measure_units,
)
updated = current.replace_structures(fresh)
molsys.interactions = {"example": updated}
assert updated.query(structure_indices=[2]).n_interactions == 0
assert updated.query(structure_indices=[2]).to_dict()[
    "evaluated_structure_indices"
].tolist() == [2]  # Evaluated absence, unlike the earlier pending frame.
assert updated.query(structure_indices=[0]).n_interactions == 1
```

For a real Buch analysis, the equivalent workflow is:

```python
# Given a MolSys whose named "buch" analysis used this same scope and pbc=False:
# fresh = msm.interactions.hbonds.get_buch_hbonds(
#     molsys, structure_indices=[2], pbc=False,
#     output_type="molsysmt.Interactions")
# updated = molsys.interactions["buch"].replace_structures(fresh)
# molsys.interactions = {**molsys.interactions, "buch": updated}
```

Both operands must be full analyses with the same local/source axes and maps,
source label, method, parameters, producer versions, measurement names/units,
and effective atom evaluation scope. A query view or an extracted subsystem
is not a replacement operand. Differences raise an error; use a separate name
for a different scientific calculation. Parameter equality is strict, including
scientific attribution. Execution mode and block counts may differ: they are
preserved per set of evaluated frames in `updated.execution_records`.
Populated frames cannot mix known periodic images with unknown images. Empty
frames do not invent images or impose missing observations.

Replacement shares immutable source blocks and indexes the owner of each frame.
When the relation catalog is unchanged, its buffers and existing block maps are
shared too. Identity maps require no stored vector. Recognizing incoming relations
can build a compact lazy index with 16 numeric bytes per registered relation;
subsequent edits reuse it. Full participant/role equality is always checked,
including hash collisions. This process-local cache is not serialized or used as
an interaction identifier. New definitions extend the catalog and may allocate
new catalog buffers. Frame bookkeeping still requires memory proportional to the
number of structures. Typed dictionary/pickle export and remapping can allocate
all active rows. HDF5 export instead writes directly from the active blocks,
including a structure with many observations. Selecting or converting a system
before writing can still materialize data through those separate operations.
A selected-frame query visits its owners and copies only the selected occurrence
columns, while sharing the relation registry. Atom queries reuse each active
source block's lazy inverse indexes. These selected projections differ from
views of an ordinary packed analysis, which share its occurrence columns too.
Repeated replacement drops fully superseded block references; it does not retain
a chain of analysis versions. A partly active block retains its original rows,
and unused relation definitions may remain in the registry. Many small edits can
therefore accumulate blocks; automatic compaction is still pending.

New occurrence indices belong to the updated analysis version and survive its
H5MSM/typed round trip. Replacing a frame does not preserve its old canvas handles.
Reading complete columns, remapping, pickle and typed dictionary export can
materialize all active data. HDF5 saving avoids that packing step; it does not
provide editing of individual rows or resumable output.
Assigning `fresh` directly under an existing name still replaces the **whole**
analysis: use `replace_structures` to preserve other frames.

```python
subset = interactions.remap(atom_indices=[0, 1, 2], structure_indices=[2, 0])
assert subset.n_structures == 2
assert subset.query(structure_indices=[0]).n_interactions == 0
assert subset.structure_source_indices.tolist() == [2, 0]
```

`atom_source_indices` and `structure_source_indices` map each local positional
index to its original source index; `source_n_atoms` and
`source_n_structures` define the original index spaces. These are indices, not
element IDs. `remap()` composes the maps and preserves `source_id`. An
appended structure or atom with no counterpart in the original source has map
value `-1`. Query projections do not copy the complete maps on every call; read
them from the result when needed. The typed dictionary and standalone HDF5
file omit identity-map vectors; their readers reconstruct those maps from
the declared axis sizes.

A native `MolSys` can hold several named, full interaction analyses. Their
atom and structure counts must match the system. Its `copy()`, `extract()`,
and `remove()` methods preserve or remap the analyses.

(user-tools-interactions-attribution)=
## Methods and attribution

Calculation methods use an author's name when a scientific definition is
established, or describe the geometric criterion. A `profile` selects the
recognition and geometry conventions within a method. These names do not claim
that the reference program originated the criterion:

| Calculation | Method | Profile | Reference implementation |
| --- | --- | --- | --- |
| Hydrogen bonds | `baker_hubbard`, `wernet_nilsson` | `nitrogen_oxygen` | MDTraj |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `elemental_fon` | CPPTRAJ |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `smarts_donor_acceptor` | ProLIF |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `explicit_sites` | MDAnalysis geometry |
| Cation–π | `centroid_distance_angle` | `smarts_5_6` | ProLIF |
| Cation–π | `centroid_distance_offset` | `three_atom_plane` | Mol* geometry |
| Cation–π | `centroid_angle_offset` | `least_squares` | MolSysMT proposal |
| π–π | `plane_angle_intersection` | `smarts_5_6` | ProLIF |
| π–π | `plane_angle_intersection` | `aromatic_cycles` | MDTraj geometry |
| π–π | `centroid_angle_offset` | `three_atom_plane` | Mol* geometry |
| π–π | `centroid_angle_offset` | `least_squares` | MolSysMT proposal |

For example, `method="donor_acceptor_distance_angle", profile="elemental_fon"`
selects the existing CPPTRAJ-compatible definition. The old selectors `prolif`,
`cpptraj`, `mdanalysis_geometry`, `mdtraj_geometry`, and `molstar_geometry`
remain supported aliases in their respective functions. Changing the name
does not change participants, cutoffs, inclusivity, periodic images or defaults.
Explicit incompatible method/profile combinations raise an error.
The site recognizer has descriptive methods `elemental_nitrogen_oxygen`,
`elemental_fluorine_oxygen_nitrogen`, and `smarts_donor_acceptor`;
its previous software selectors remain aliases too.

Detector-produced analyses include `method`, `profile`, `method_definition`,
and `attribution` in `analysis.parameters`. The attribution payload uses
`schema="molsysmt.scientific_attribution@1"`, a calculation target and a compact
list of bibliographic records. Each record declares its contextual roles:
`scientific_criterion`, `reference_implementation`, or `executed_software`.
A reference to ProLIF does not mean ProLIF was executed. Actual producer
versions remain in `analysis.software`; a reached RDKit branch records RDKit.
The versioned method definition identifies a contract, not a scientific DOI.
The original reference for the historical Buch selector has not been verified;
its recorded criterion is `hydrogen_acceptor_distance`, without a guessed paper.
The existing Luzard–Chandler entry point records the established
`luzar_chandler` criterion and its paper while retaining its public spelling.

The complete typed dictionary, standalone file and H5MSM 0.5 preserve these
records, including the bibliography and producer versions recorded at calculation
time. Query views expose `.parameters`; their occurrence-only `to_dict()` does
not carry the complete analysis parameters. Loading, querying and remapping do
not register a new scientific calculation. Manually constructed and older
analyses may have no attribution; missing records mean unknown provenance.

When Ackredit is installed, completed calculations also register their used
references in the current Ackredit session. An evaluated structure with no
observations still belongs to that calculation. MolSysMT imports Ackredit lazily
and enables no import hooks, DOI enrichment, persistent journal or reminders.
Without Ackredit, the same result-level metadata is produced. A broken optional
provider emits a diagnostic while preserving the scientific result.
This also applies when warnings are promoted to errors. If creating or emitting
that diagnostic fails, a fallback log retains `MSM-WARN-ATTR-001`, the operation
and both failures. Scientific errors and unrelated warnings still propagate.
The caller owns workflow sessions and report destinations:

```python
# Optional workflow reporting; requires Ackredit.
import ackredit

with ackredit.session("interaction-workflow"):
    analysis = msm.interactions.hbonds.get_hbonds(molecular_system, pbc=False)
    print(ackredit.report(format="bibtex"))
```

Here `molecular_system` must supply the detector's required chemistry and
coordinates; this sketch does not assign chemistry or download a system.
Bibliography is stored once per analysis, never once per observation. Portable
workflow capture and contextual report roles are being coordinated with
[Ackredit #75](https://github.com/uibcdf/ackredit/issues/75).

(user-tools-interactions-association)=
## Associating an analysis

Attaching an analysis declares that its local atom and structure indices
correspond to the system's local indices. You are responsible for choosing
the matching system. MolSysMT checks index bounds, result consistency, and
matching axis sizes; equal counts alone do not establish molecular identity.
The writer of an H5MSM containing both system and analyses is responsible
for their correspondence and declared associations.

When loading an analysis from another file, align it with the target before
attachment if either axis has a different order. `remap()` accepts old
analysis indices in the desired new order. It can extract or reorder the
analysis; it does not embed a smaller analysis into a larger target domain.
Source maps are provenance and are not automatically matched to the target.
`source_id` is an optional label supplied by the caller, not a verified
fingerprint. Attachment requires no automatic origin authentication. Use
coordinates and periodic boxes compatible with the calculation; the stored
image vectors refer to that geometry.

```python
import numpy as np
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=3)
molsys.structures.append(coordinates=np.zeros((3, 3, 3)))
molsys.interactions = {"example": interactions}
selected = molsys.extract(atom_indices=[0, 1, 2], structure_indices=[2, 0])
assert selected.interactions["example"].n_structures == 2
```

You can also attach an analysis returned directly by the disulfide candidate
detector. This synthetic example identifies a geometric candidate; it does
not declare a covalent bond:

```python
builder = msm.MolSysBuilder()
first = builder.add_atom(atom_name="SG", atom_type="S")
second = builder.add_atom(atom_name="SG", atom_type="S")
builder.add_group([first], group_name="CYS")
builder.add_group([second], group_name="CYS")
builder.set_coordinates(
    msm.pyunitwizard.quantity([[0, 0, 0], [0.20, 0, 0]], "nm")
)
molsys = builder.build()
analysis = msm.interactions.disulfides.get_disulfide_candidates(
    molsys, pbc=False, output_type="molsysmt.Interactions"
)
molsys.interactions = {"disulfide_candidates": analysis}
assert molsys.interactions["disulfide_candidates"].n_interactions == 1
```

For a system with covalently attached donor hydrogens, use the Buch detector
to construct an analysis of H-A distances (in nm):

```python
analysis = msm.interactions.hbonds.get_buch_hbonds(
    molsys, output_type="molsysmt.Interactions"
)
molsys.interactions = {**molsys.interactions, "buch": analysis}
visible = analysis.query(structure_indices=[0]).to_dict()
```

The result declares the automatically eligible participants, including
donor hydrogens attached outside an atom selection. Two selections must have
disjoint participant universes or identical roles for this optional output.
Supplied role arrays and a second structure axis are currently unsupported.
With PBC, the donor is the image anchor, the hydrogen uses its D-H minimum
image, and the acceptor continues from that hydrogen using the observed H-A
image. The stored distance checks the H-A segment; D-H unwrapping supplies
consistent drawing geometry and does not add a detection criterion. These
detectors use eager execution; requesting `Interactions` does not make them
stream coordinates or write observations incrementally.

For the joint distance-and-angle criterion, use
`msm.interactions.hbonds.get_luzard_chandler_hbonds(...,
output_type="molsysmt.Interactions")`. It measures donor-to-acceptor distance
in nm and the H-D-A angle in rad, with the donor as vertex. The defaults are
0.35 nm and a strict angular cutoff of 30 degrees (pi/6 rad). Its periodic
images independently unwrap D-H and D-A from the donor; they reproduce the
two vectors used for the angle. It has the same optional-result scope limits
as Buch and preserves evaluated-empty frames and producer versions.

Appended structures remain unevaluated by existing analyses, including a
coordinate-only source passed to `msm.append_structures`. Adding atoms to a
system with analyses keeps their previous search universe fixed; the added
atoms are outside it and are not claimed as evaluated. Adding atoms from a
source `MolSys` that already has analyses, or appending structures from such a
source, requires an explicit analysis merge policy and currently raises an
error. H5MSM 0.4 and MolSysDict 0.1 cannot store attached analyses and
reject that export. H5MSM 0.5 writes and reads the named analyses with the
system; `Interactions.save()` remains available for standalone results.

## Directional halogen observations

The experimental {func}`molsysmt.interactions.halogen_bonds.get_halogen_bonds`
returns four singleton roles: donor, halogen, acceptor and acceptor reference.
Every role participates in atom-set queries; an acceptor with two eligible
reference neighbors can yield two separately identifiable directional relations.
The descriptive `distance_two_angles` method with `smarts_donor_acceptor` profile
reproduces the ProLIF 2.2.2 core adapted from Auffinger et al. (2004), not that
paper's original element-specific distance thresholds. Producer versions and
the adapted paper/reference bibliography persist with each named analysis. See
{ref}`Tutorial_Get_halogen_bonds` and {ref}`Cookbook_Saving_halogen_bonds`.

## Hydrophobic atom-pair observations

The experimental {func}`molsysmt.interactions.hydrophobic.get_hydrophobic_interactions`
uses `atom_pair_distance` with `smarts_hydrophobic_atoms`, reproducing the pinned
ProLIF 2.2.2 core. Two distinct atoms form an unordered relation, with ascending
source indices and roles `hydrophobic_1`/`hydrophobic_2`; roles do not encode the
selected interface sides. Self records and reverse duplicates are excluded.
Additional covalent/intramolecular exclusions are not inferred. Use disjoint
selections for interfacial observations. This typed proximity is not a residue
scale value or interaction energy. Scope, known-empty coverage, canonical MIC
images, original producers and reference bibliography remain part of the named
analysis. See {ref}`Tutorial_Get_hydrophobic_interactions` and
{ref}`Cookbook_Saving_hydrophobic_interactions`.

## Coordination and solvent paths

{func}`molsysmt.interactions.metal_coordination.get_metal_coordination` stores
directed metal/ligand candidates; it does not declare bonds in ChemicalStates.
{func}`molsysmt.interactions.water_bridges.get_water_bridges` stores two or three
D-H-A legs with six or nine singleton roles and one or two mediator waters.
`order=1` is the default; `order=2` means exactly two distinct waters, not up to two. Repeated atoms
retain their separate chemical roles; `involving_selection` queries return an occurrence
once. Internal queries require all actual branch atoms, including mediator
O and the participating H. An unused water H is not an extra participant.
Both analyses retain evaluated-empty frames, original references/producer
versions, units and observed images through named H5MSM 0.5 conversion.
