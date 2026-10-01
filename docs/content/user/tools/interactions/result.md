(user-tools-interactions-result)=
# Querying interaction results

Build an experimental `molsysmt.Interactions` result from observations that
have local atom and structure indices. By default these equal the source
system's indices; explicit source maps support a selected or reordered domain.
This class stores the
observations; it does not detect interactions or declare covalent bonds.

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
interactions.query(atom_indices=[0], mode="incident")
interactions.query(atom_indices=[0, 1, 2], mode="internal")
interactions.query(atom_indices=[0], mode="cross")
interactions.between([0, 1], [2], exclusive=True)
```

`incident` means at least one participating atom belongs to the selection;
`internal` requires all participating atoms; `cross` means incident but not
internal. For a ring, every constituent atom participates in these tests.
`between(A, B)` requires at least one atom from each disjoint set. With
`exclusive=True`, every participant atom must belong to `A` or `B`.

Each query returns a lightweight view. `to_dict()` provides typed occurrence
columns, explicit evaluated-structure indices, measurement units, and optional
periodic-image vectors. Use `relation(index)` to inspect the type and roles
referenced by a result's `relation_indices` column.
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

```python
interactions.save("observations.h5i")
restored = msm.Interactions.load("observations.h5i")
```

The standalone HDF5 file is versioned and separate from H5MSM. `load` reads
the complete result into memory. The current version has no streaming writer,
lazy file-backed queries, or incremental add/remove editor. The disulfide
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

This returns an independent result and leaves existing query views unchanged.
It copies the packed occurrence arrays, so repeated local edits still need
the planned incremental editor. Re-evaluate the affected structures before
claiming that they have no interactions.

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
retain their separate chemical roles; incident queries return an occurrence
once. Internal queries require all actual branch atoms, including mediator
O and the participating H. An unused water H is not an extra participant.
Both analyses retain evaluated-empty frames, original references/producer
versions, units and observed images through named H5MSM 0.5 conversion.
