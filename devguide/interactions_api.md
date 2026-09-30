# Interaction Analysis API

`molsysmt.interactions` owns chemically interpreted analyses over molecular
systems. Distance-only proximity remains a geometric primitive in `structure`;
it is not by itself an interaction classification. The first public families
are `interactions.hbonds`, `interactions.disulfides`, and the experimental
`interactions.ionic`. Other families need
separate scientific contracts and decisions.

## Hydrogen bonds

`interactions.hbonds` is the canonical path for the existing donor and acceptor
helpers and the named Buch and Luzard–Chandler methods. The implementations and
their return conventions were moved without changing their geometric criteria:

| Method | Current default criterion | Result |
| --- | --- | --- |
| `get_buch_hbonds` | Hydrogen–acceptor separation at most 0.23 nm | Per-structure donor, hydrogen, acceptor triples and aligned distances. |
| `get_luzard_chandler_hbonds` | Donor–acceptor separation at most 0.35 nm and the H–D–A angle below 30 degrees | Per-structure triples, distances, and angles. |

The donor helper sorts intact covalent donor-H pairs by donor and then hydrogen
index. Independently sorting the columns would change chemical membership;
the interleaved-index guard under `uibcdf/molsysmt#258` protects this invariant.

Both methods support one molecular system with one or two atom selections.
Passing `molecular_system_2` raises `NotImplementedMethodError`; cross-system
atom and structure alignment has no defined contract yet. Their current array
layout is a legacy method-specific contract, not a common interaction result
schema. The root `molsysmt.hbonds` namespace and direct historical module paths
remain available for compatibility. There is no deprecation decision for them
in 1.0.

For a single selection with no eligible donor or acceptor, each method returns
an empty result for every requested structure rather than attempting a
covalent-path lookup on an empty atom set.

Both hydrogen-bond tuple results support evaluated frames with eligible atoms but
no accepted bonds. Equal counts retain the rectangular legacy arrays; varying
counts return aligned lists of integer `(n_hbonds, 3)` arrays and nanometer
`(n_hbonds,)` distance quantities, including shaped empty entries.
Luzard–Chandler also returns aligned radian angle quantities. Neither path
pads frames with fabricated observations. The corrections are tracked by
`uibcdf/molsysmt#253` and `uibcdf/molsysmt#259`.

`get_buch_hbonds(..., output_type="molsysmt.Interactions")` returns a sparse
analysis with donor, hydrogen, acceptor roles, evaluated-empty coverage,
nanometer H-A distances, automatic role-selection rules, and the eligible
participant universe actually searched. The donor helper can include attached
hydrogens outside the user's atom selection; these belong to that universe.
One selection declares an internal scope. Two disjoint participant universes
declare a between scope and search both donor/acceptor directions. Identical
role selections collapse to an internal scope without duplicated observations.
Repeated requested frames are also deduplicated in this result.

The optional result currently rejects supplied donor/acceptor arrays, a second
structure axis, and partially overlapping participant universes. Those cases
need explicit eligibility and alignment contracts. It uses eager execution;
the result adapter is not a streaming trajectory detector. The existing tuple
API remains available for its established supported combinations.

The migration is guarded by regression tests using bundled systems. Those tests
show continuity of the existing implementation, not independent scientific
validation of either hydrogen-bond definition. Callers must choose and report
the named criterion and parameters used.

## Disulfide candidates

`interactions.disulfides.get_disulfide_candidates` identifies sulfur atoms in
eligible groups (by default `CYS`) and returns candidate pairs when atoms in
different groups lie within the maximum S–S distance (by default 0.205 nm).
The detector accepts an atom selection, an ordered set of structure indices,
and periodic boundary conditions. It returns two aligned lists: one array of
global atom-index pairs and one nanometer distance quantity per requested
structure. An evaluated structure with no candidates has an empty `(0, 2)`
pair array and an empty `(0,)` distance array. The detector does not mutate the
system and reports a geometric candidate even if the pair is already recorded
as a bond.
With `output_type="molsysmt.Interactions"`, it instead returns one full sparse
analysis in the original system's atom and structure index spaces. The result
declares its eligible sulfur atoms as the evaluated scope, retains evaluated
empty frames, stores nanometer distances and geometric evidence, and records
the observed lattice image when a periodic box was used. Repeated requested
structure indices do not duplicate observations in this result. The default
tuple output remains unchanged. The caller attaches the analysis to `MolSys`
under a chosen name when persistence with the system is wanted.

The topology remains authoritative for recorded covalent bonds.
`build.get_disulfide_bonds` delegates to this detector and retains its
single-structure list-of-pairs result for build workflows;
`build.get_missing_bonds` continues to consume that entry point. The detector
has synthetic tests for geometry, selection, group filters, periodicity, frame
order, and already-recorded bonds. These tests validate the implementation of
the stated threshold rule; they do not independently establish chemical bond
identity. The disulfide API is Experimental in the public stability registry.

## Reusable ring participants

`topology.get_rings` and `physchem.get_aromatic_rings` are experimental chemical
preparation tools. They are form-agnostic: external inputs use the registered
native chemistry conversion routes, not detector-specific package branches.
ChemicalStates, ChemicalStatesDict and topology-free MolSys can supply the
necessary atom domain and chemistry directly. H5MSM 0.5 reads chemistry and
association metadata without coordinates or saved analyses, and requires
declared identity atom links where domains are combined. Rich selections also
need the attributes and geometry used by their expressions.

Both tools use `@arg_digest()` and expose `skip_digestion=False`. Private graph,
state and packing helpers are undecorated. Trusted delegation skips digestion
only when the complete target argument contract is already satisfied.

The topology operation computes an unweighted minimum cycle basis of the complete
covalent graph, excluding dative edges. It does not classify aromaticity. The
physchem operation computes a basis of the covalent subgraph explicitly marked
aromatic in the chosen ChemicalStates state. Unknown atom or bond aromatic flags
fail rather than becoming False. Aromatic bond endpoints must be declared
aromatic, and aromatic atoms/bonds must belong to cycles in that subgraph.
A nonaromatic fusion bond can leave an aromatic perimeter, so filtering the full
covalent basis would not be equivalent. No planarity, residue-name, or bond-order
fallback is used. Legacy TopologyDict/MolSysDict do not preserve these aromatic
fields; their covalent graphs can still be used with an explicit completeness
assumption when needed. Typed ChemicalStatesDict preserves the relevant chemistry.

Results contain int64 `atom_indices`/`atom_offsets`, source, selected and examined
atom axes, state index, method, connectivity evidence and producer versions.
Aromatic results also record the declared-bond definition and rule version.
Memberships are sorted atom sets, not traversal order. Recognition precedes
selection and rejects cuts through any perceived ring, including shared fused
atoms. Empty memberships have `(0,)` and offsets `[0]`. These dictionaries are
chemical features, not InteractionsDict or observed pi-pi interactions.

A minimum basis is not all cycles or SymmSSSR. Tied bases need not be unique or
symmetry-preserving; fixed atom indices and NetworkX version establish the
reproducibility boundary. Perception uses cyclic biconnected blocks and an
explicit default maximum of 256 atoms per cyclic block. Larger blocks fail
before basis calculation; the caller may raise the limit after assessing cost.
The limit does not bound process RSS, total graph memory or execution time.

Analytical graph tests and optional independent RDKit fixtures cover the stated
simple/fused memberships. This evidence does not establish universal aromaticity
or favorable pi-pi geometry. The plane tool and pi-pi detector remain under
uibcdf/molsysmt#265. Reproducible chemical preparation measurements are described
in [benchmarking/rings.md](benchmarking/rings.md).

## Ionic contacts

`interactions.ionic.get_ionic_interactions` calculates minimum-distance
observations between opposite formal-charge centers in one declared chemical
state. The required `distance_threshold` is a finite positive length quantity;
there is no universal default. The criterion is inclusive, with one float64
ULP for unit-conversion roundoff. Proximity is geometric evidence, not an
electrostatic energy, favorable binding, or a recorded covalent bond.

General chemistry belongs to `physchem.get_charge_centers`. Its bounded
definition groups carboxylate and guanidinium motifs, directly covalently
connected charged atoms, and other literal charged atoms; net-neutral groups
are omitted. Carboxylate geometry uses oxygen references, guanidinium nitrogen
references. Whole-center membership is retained even when a reference subset
defines the distance. Source elements, formal charges, connectivity, and bond
orders must be explicit. An explicit completeness assumption is recorded
without repairing the source. No protonation, residue descriptor, partial
charge model, or force-field parameterization substitutes for missing chemistry.
Phosphate, sulfate, and aromatic delocalization remain separately scoped under
`uibcdf/molsysmt#262`.

Recognition examines source chemistry once before selection. Atom selections
must contain complete centers. Calculation scopes are internal, incident, or
between two disjoint selections. Frames are source structure indices; repeats
are deduplicated and sorted, and evaluated-empty frames remain in coverage.
Intramolecular contacts are included; direct covalent center links are excluded,
while dative links do not impose this exclusion. There is no residue/component
exclusion. MIC uses the available box when requested. A periodic observation
anchors the positive participant at image zero and shifts the whole negative
participant by the recorded row-box lattice vector. Split participants needing
individual atom images fail explicitly.

The default result is `molsysmt.Interactions`, optionally
`molsysmt.InteractionsDict`. Relations have positive/negative roles; measures
contain distances in nm and center charges in elementary charge units.
Parameters preserve threshold, charge source, selected state, definition/rule
version, evidence, scope, exclusions, periodic policy, execution mode, block
count, and numerical memory policy. Producer versions are captured at
calculation time. Attachment to `MolSys.interactions` is an explicit named
assignment; public H5MSM 0.5 preserves the complete result.

Keyword-only `heavy_mode` supports native MolSys and H5MSM 0.5 paths with
index selections or `all`. Rich string selections retain eager execution.
The [scalability contract](SCALABILITY.md) defines chemistry projection,
coordinate/candidate/result working estimates, and unsupported combinations.
The result remains resident; the detector has no incremental writer.

Scientific controls use analytical fixtures and real bundled Trp-cage/HP35
coordinates under explicitly declared states. Fixed membership, independent
RDKit SMARTS, exhaustive Cartesian distances, and controlled periodic image
representations protect the bounded claim. They do not establish experimental
protonation or validate arbitrary chemical motifs. Guards are
`tests/scientific_truth/curated/test_ionic_interactions.py` and
`tests/interactions/ionic/`; source hashes and state assumptions are in
`devtools/data/ionic_validation_systems.json`. The API remains Experimental;
scientific correctness for this declared rule does not establish stability.
See the [ionic benchmark guide](benchmarking/ionic.md) for measured tradeoffs.

## Current result behavior and 1.0 target

The experimental `molsysmt.Interactions` class stores one method's typed observations,
relation participants and roles, explicit evaluated-structure coverage,
declared atom search scope, measurement units, evidence labels, and optional
periodic image vectors. Its `software` dictionary maps software names to the
versions that produced the observations. Both hydrogen-bond and disulfide adapters capture
`{"molsysmt": molsysmt.__version__}` during calculation. Views, remapping,
invalidation, InteractionsDict, standalone HDF5, selective HDF5 projections,
and H5MSM 0.5 preserve this metadata. The optional field is stored once per
analysis in schema-1 metadata, without a per-occurrence column. Readers of
older payloads with no field return `{}`: unknown producer versions are never
filled from the installed reader version. External producers may supply their
own name/version entries through `from_records(software=...)`. Its
`query` method supports local-index structure lists and atom-set `incident`,
`internal`, and `cross` semantics; `between` supports disjoint atom sets.
`from_records`, `to_dict`, `relation`, `remap`, `invalidate_structures`, `save`, and
`load` provide construction,
inspection, and standalone HDF5 round trips. The current file schema version
is 1 and is distinct from H5MSM 0.4. `load` materializes the result in memory.
`to_dict()` exposes `occurrence_indices`, the `int64` row positions in the
complete analysis. They distinguish parallel observations with the same
structure and relation, remain unchanged in filtered views and H5MSM round
trips, and are scoped to one named analysis version. Remapping or editing
creates a new version and can reassign positions. The row position is derived
from stored order, so it adds no per-occurrence file column.
Input records and source indices are validated by the class. Disulfide
candidates and both hydrogen-bond detectors have opt-in result routes.
The analysis-level evaluation scope has modes `internal(A)`, `incident(A)`,
and `between(A, B)` with a declared participant universe. It applies uniformly
to evaluated structures. An evaluated-empty frame claims no detections only
inside that scope. A constructor defaults to an internal search over all local
atoms; detector adapters must supply their actual search scope. Relations
outside the scope are rejected. Scope and source maps survive remapping,
InteractionsDict, and standalone HDF5 round trips. Distinct per-frame scopes
or merged analyses with different scopes are not yet representable as one
result.
Periodic-image vectors are all-or-none across an analysis: the constructor
rejects mixed explicit and absent image data rather than substituting zero
vectors for unknown images.
For occurrence `o`, `image_offsets[o]:image_offsets[o+1]` selects one integer
vector per participant, in the relation's participant order. The three rows
of a structure's box are its lattice vectors in nanometers. The observed
position of each atom in participant `p` is its stored coordinate plus
`image_vectors[p] @ box`. Thus a positive `[1, 0, 0]` adds the first box
vector. Relative geometry is anchored to the first participant: subtract its
image vector from each other participant's vector before applying the box.
All atoms in one compound participant receive the same lattice shift; this
encoding does not describe internal unwrapping of a split ring. Without image
columns, the observed periodic copy is unknown, even if PBC was used by a
detector. Detector adapters must emit the actual image chosen by their
geometry calculation. The disulfide result route recovers this image from
the same MIC algorithm for its observed S–S pairs and verifies the aligned
distance. Buch anchors the donor at image zero, applies the D-H MIC shift to
the hydrogen, and adds the H-A MIC shift to obtain the acceptor image. The
H-A distance is checked against the detector output. The D-H shift supplies
a deterministic display image for the covalently attached hydrogen; it is
not an additional Buch detection criterion. Luzard–Chandler anchors the
donor at zero and independently applies the D-H and D-A MIC shifts to the
hydrogen and acceptor. These are the vectors used for its H-D-A angle;
the adapter checks reconstructed D-A distance and H-D-A angle against the
detector output. Its measurements are `distance` in nm and `angle` in rad.
The acos detector loses precision near collinearity, so the image check uses
a 1e-7 rad absolute angular tolerance. Both optional results currently require
automatic roles, one selection or disjoint participant universes, or identical
role selections; supplied roles, a second structure axis, and partially
overlapping universes raise explicit unsupported-method errors.

The experimental class has no lazy file-backed query, streaming writer, or
incremental add/remove editor. `invalidate_structures()` returns an independent
snapshot with the selected frames unevaluated and their occurrences removed;
it copies packed arrays and does not replace an incremental editor. It represents one
molecular-system index space and one method per instance. `MolSys.interactions`
holds a mapping of named full results with matching atom and structure axes.
Each result retains local-to-source atom and structure index arrays plus the
sizes of both source axes. Extraction composes those maps; an appended
structure has source index `-1` and is unevaluated. The caller-supplied source
label stays with the mapped result. These are positional indices, never
element IDs.
Native copy, extraction, and removal preserve or remap attached results;
newly appended structures remain unevaluated. Adding atoms to a target with
analyses preserves the target's previous atom search scope: new
atoms are outside the evaluated universe and have source index `-1`. Adding
from a source that carries analyses, or appending its structures, requires an
explicit merge policy and currently fails. H5MSM 0.4 and
MolSysDict 0.1 exports reject a system with attached analyses because those
formats cannot store them. The design and remaining gates are
tracked by [`uibcdf/molsysmt#251`](pending_proposals/design_a_sparse_public_interactions_result_and_serialization_contract.md).
The required H5MSM and MolSysViewer integrations are tracked
in the [1.0 execution plan](pending_proposals/release_1_0_execution_plan.md)
and the design proposal [#251](pending_proposals/design_a_sparse_public_interactions_result_and_serialization_contract.md).
Implementation progress is tracked by
[`uibcdf/molsysmt#252`](pending_proposals/implement_experimental_sparse_interactions_results_and_queries.md).

H5MSM 0.5 has an optional interaction layer. Public `molsysmt.h5msm.write`
and `read` preserve named analyses attached to `MolSys`; `write_layers` and
`read_layers` also handle interaction-only files. The public readers currently
materialize each selected analysis. An indexed selective HDF5 reader exists
internally, but it is not yet a supported public file-backed query API.
The native/H5MSM parity workflow is guarded by
`tests/interactions/test_public_molsys_h5msm_workflow.py`. No generic contact
classifier is implied by these family methods. Client
libraries can call the family-specific APIs and should preserve method
identity and units in any presentation or derived analysis. A stable
cross-system result contract requires a separate decision.

## Associating analyses with a system

Attaching a full analysis to `MolSys.interactions` declares that its local
atom and structure indices refer to that system's local index spaces.
MolSysMT validates the result's typed columns, index bounds, source maps,
coverage, and participant scope. Native attachment also validates analysis
names, full-result types, and matching atom and structure axis sizes. These
checks establish structural consistency; equal axis sizes do not prove that
two independently supplied systems have the same atom or structure ordering.

The H5MSM writer is responsible for the scientific correspondence of layers
and their declared associations. The 0.5 reader validates those associations;
it does not independently authenticate the molecular origin of the layers.
When loading an analysis from a separate file, the caller is responsible for
choosing the matching system and aligning both local axes before attachment.
If ordering differs, supply that correspondence explicitly through a supported
remap or extraction. `Interactions.remap()` takes the old analysis indices in
the desired new order; it is not an arbitrary embedding into a larger target.
Source maps record provenance and are not automatically joined to target axes.

`source_id` is an optional caller-supplied provenance label, not a verified
fingerprint. Missing source identity does not prevent attachment of an
otherwise valid result. Content fingerprints and automatic cross-file origin
verification are optional future capabilities, not a MolSysMT 1.0 gate. A
consumer may require an explicit user declaration or impose stricter checks.
This does not waive existing validation: malformed results, out-of-range
indices, incompatible axes, and contradictory declared H5MSM associations
remain errors. The caller must also provide coordinates and, for periodic
observations, box vectors compatible with the stored geometry and images.
