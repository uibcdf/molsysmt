# Interaction Analysis API

`molsysmt.interactions` owns chemically interpreted analyses over molecular
systems. Distance-only proximity remains a geometric primitive in `structure`;
it is not by itself an interaction classification. The first public families
are `interactions.hbonds` and `interactions.disulfides`. Other families need
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

The Buch tuple result also supports evaluated frames with eligible atoms but
no accepted bonds. Equal counts retain the rectangular legacy arrays; varying
counts return aligned lists of integer `(n_hbonds, 3)` arrays and nanometer
`(n_hbonds,)` quantities, including shaped empty entries. Neither path pads
frames with fabricated observations. This behavior resolves
`uibcdf/molsysmt#253`.

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

## Current result behavior and 1.0 target

The experimental `molsysmt.Interactions` class stores one method's typed observations,
relation participants and roles, explicit evaluated-structure coverage,
declared atom search scope, measurement units, evidence labels, and optional
periodic image vectors. Its
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
candidates and Buch hydrogen bonds have opt-in result routes;
Luzard–Chandler still has only its method-specific output.
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
not an additional Buch detection criterion. Luzard–Chandler still needs a
result adapter whose images agree with its angle calculation.

The experimental class has no lazy file-backed query, streaming writer, or
incremental add/remove editor. `invalidate_structures()` returns an independent
snapshot with the selected frames unevaluated and their occurrences removed;
it copies packed arrays and does not replace an incremental editor. It represents one
molecular-system index space and one method per instance. `MolSys.interactions`
holds a mapping of named full results with matching atom and structure axes.
Each result retains local-to-source atom and structure index arrays plus the
sizes of both source axes. Extraction composes those maps; an appended
structure has source index `-1` and is unevaluated. The source identity stays
with the mapped result. These are positional indices, never element IDs.
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
classifier or other interaction family is implemented in this slice. Client
libraries can call the family-specific APIs and should preserve method
identity and units in any presentation or derived analysis. A stable
cross-system result contract requires a separate decision.
