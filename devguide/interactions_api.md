# Interaction Analysis API

`molsysmt.interactions` owns chemically interpreted analyses over molecular
systems. Distance-only proximity remains a geometric primitive in `structure`;
it is not by itself an interaction classification. The first public families
are `interactions.hbonds`, `interactions.disulfides`, and the experimental
`interactions.ionic`, `interactions.pi_pi`, `interactions.cation_pi` and
`interactions.halogen_bonds`, `interactions.hydrophobic`,
`interactions.metal_coordination` and `interactions.water_bridges`. Other families need
separate scientific contracts and decisions.

## Scientific method names and attribution

Public method selectors name a scientific criterion or its geometric operations,
not a reference software package. A keyword-only `profile` specifies participant
recognition, plane construction and numerical conventions when the criterion
has multiple supported definitions. The following pairs are implemented:

| Family | `method` | `profile` | Reference definition |
| --- | --- | --- | --- |
| Hydrogen bonds | `baker_hubbard` | `nitrogen_oxygen` | Baker–Hubbard criterion, MDTraj implementation reference |
| Hydrogen bonds | `wernet_nilsson` | `nitrogen_oxygen` | Wernet–Nilsson criterion, MDTraj implementation reference |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `elemental_fon` | CPPTRAJ elemental sites and geometric rule |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `smarts_donor_acceptor` | ProLIF SMARTS sites and geometric rule |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `explicit_sites` | MDAnalysis geometric rule with caller-supplied sites |
| Pi-pi | `plane_angle_intersection` | `smarts_5_6` | ProLIF ring and plane definition |
| Pi-pi | `plane_angle_intersection` | `aromatic_cycles` | MDTraj geometric definition on declared aromatic cycles |
| Pi-pi | `centroid_angle_offset` | `three_atom_plane` | Mol* geometric definition |
| Pi-pi | `centroid_angle_offset` | `least_squares` | Explicit-cutoff MolSysMT proposal |
| Cation-pi | `centroid_distance_angle` | `smarts_5_6` | ProLIF ring/cation and plane definition |
| Cation-pi | `centroid_distance_offset` | `three_atom_plane` | Mol* geometric definition |
| Cation-pi | `centroid_angle_offset` | `least_squares` | Explicit-cutoff MolSysMT proposal |
| Halogen bonds | `distance_two_angles` | `smarts_donor_acceptor` | ProLIF 2.2.2 core adapting Auffinger et al.; not original-paper distance thresholds |
| Metal coordination | `metal_ligand_distance` | `smarts_metal_ligand` | ProLIF 2.2.2 MetalDonor/Distance chemical sites and inclusive 0.28 nm criterion |
| Water bridges | `hbond_water_path` | `indexed_water` | Exact one- or two-water path; independently chosen attributed hydrogen-bond criteria. Previous `two_hbonds_one_water` remains supported for order one. |
| Hydrophobic | `atom_pair_distance` | `smarts_hydrophobic_atoms` | ProLIF 2.2.2 atomic SMARTS incorporating RDKit feature patterns and distance criterion |

The descriptive names do not establish who first introduced a formula. Reference
implementations and verified papers are retained separately. Historical software
selectors such as `prolif`, `cpptraj`, `mdtraj_geometry` and `molstar_geometry`
remain compatibility aliases for their exact profiles; a conflicting profile
raises an argument error. Defaults and numerical observations are unchanged by
renaming. Public detector docstrings define the exact cutoffs, inequality signs,
site rules and reference limitations. Reproducing a geometric definition does
not promise the reference program's complete feature discovery or refinement.

`Interactions.method` identifies the producer function. The scientific selector
is `parameters["method"]`, accompanied by `profile`, `method_definition` and the
selected rule's parameters. `method_definition` is a versioned definition label,
not a DOI. Producer versions belong in `Interactions.software`; the reader's
installed version must never replace them.

The optional Ackredit pilot credits completed calculations, including evaluated
empty results, to the application's current session. A detached bibliography in
`parameters["attribution"]` has schema `molsysmt.scientific_attribution@1`, a
producer target and typed bibliographic items with contextual roles
`scientific_criterion`, `reference_implementation`, and `executed_software`.
Referencing ProLIF does not claim that ProLIF executed. Verified declarations are
offline; missing original attribution is left unknown rather than invented.
This metadata is constructed once per analysis, independently of workflow-session
deduplication, and survives views, typed conversion and H5MSM persistence.

Ackredit is loaded lazily and remains optional. Import hooks, reminders, journals
and network enrichment are not enabled by MolSysMT. Missing Ackredit preserves
the result bibliography; a broken optional provider emits `MSM-WARN-ATTR-001`
without discarding a completed calculation. Reading, querying or remapping a
saved analysis does not credit a new calculation. Portable provider capture and
suite adoption remain tracked by `uibcdf/ackredit#75` and
`uibcdf/molsyssuite#68`; this is not whole-library instrumentation. The guard is
`tests/interactions/test_scientific_attribution.py`.

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

The newer `interactions.hbonds.get_hbonds` defaults to Baker–Hubbard and returns
`molsysmt.Interactions` (or `molsysmt.InteractionsDict` when requested). It supports
the five method/profile pairs above. Its public defaults differ from the legacy
tuple functions by design; the legacy functions retain their default outputs.
The result includes all donor/hydrogen/acceptor roles, three pair distances in
nm, D-H-A and H-D-A angles in rad, actual evaluated scope and empty-frame
coverage. Method-specific geometric and chemical rules are recorded explicitly.

General site recognition belongs to `physchem.get_hbond_sites`; its public
methods are `elemental_nitrogen_oxygen`, `elemental_fluorine_oxygen_nitrogen`
and `smarts_donor_acceptor`. Explicit-site calculations require intact supplied
donor-H pairs and acceptor indices, not partial-charge guessing. Selection
eligibility is distinct from the complete chemical graph examined during
recognition. Modern detection supports projected coordinate blocks on native
MolSys and H5MSM 0.5, with a resident sparse result. The legacy Buch and
Luzard–Chandler adapters remain eager. All paths must retain the actual images
used by geometry; inconsistent periodic triangles are rejected.

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

`ChemicalStates` owns recorded covalent bonds; `Topology.bonds` remains a
compatibility facade for the selected state.
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
or favorable pi-pi geometry. These general tools now supply both pi-pi and
cation-pi detection. Reproducible chemical preparation measurements are described
in [benchmarking/rings.md](benchmarking/rings.md).

## Reusable plane geometry

`msm.structure.get_least_squares_plane` fits unweighted orthogonal least-squares planes to
one atom selection or overlapping groups. It requires coordinates, not topology
or aromaticity. Its geometric dictionary is not an InteractionsDict. Packed
source atom memberships and requested source structure indices accompany centers,
unoriented unit normals and orthogonal RMS/maximum deviations. Structure traversal
preserves order and repetitions; explicit empty frame lists have typed shapes.

The implementation uses a bundled Rust/Faer rectangular SVD on scaled, centered
coordinates, without forming covariance matrices or computing left vectors.
Independent frames follow the session parallel policy; each worker fits groups
sequentially with bounded workspace. Units, selection and PBC validation remain
in Python. The normal is
unique only when the middle/smallest singular-value gap exceeds 1e-12 times the
largest singular value. Collinear, coincident and degenerate clouds fail; regular
planar rings with equal in-plane singular values are permitted. The normal's
largest absolute component is positive, with the first component breaking an
exact tie. This is not a temporal sign-continuity promise. Future detectors must
compare unoriented planes using the absolute dot product.

With `pbc=True`, boxes must be finite and numerically nonsingular: determinant
magnitude after dividing by each box's largest absolute component must exceed
1e-12, independently of uniform length scaling. All group atoms
must already be in their anchor's MIC neighborhood. Shared PBC validation rejects
groups requiring internal image shifts. The tool does not reconstruct molecules,
change coordinates or infer aromaticity. Ring recognition, plane fitting and
observation criteria remain distinct tools in their owning modules.

Native Structures/MolSys and modular H5MSM use ChunkedExecutor with projected
coordinate blocks. Explicit H5MSM indices avoid topology and saved-analysis
materialization, including Structures-only files. Other forms providing a real
coordinate getter use the eager route; placeholder iterators do not establish
streaming capability. Missing forced streaming fails explicitly.

Dense results are preallocated in RAM. Numerical budget estimates include output
standardization and group-wise SVD workspace; an operation-specific chunk cap
applies after optimization. They do not bound process RSS or supply a disk-backed
output. See [benchmarking/planes.md](benchmarking/planes.md) for a bounded
projection/geometry measurement. The implemented ring detectors call the general
plane and plane-pair tools; their scientific criteria remain in `interactions`.

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

## Aromatic ring observations

`interactions.pi_pi.get_pi_pi_interactions` is an experimental geometric detector.
Its default `centroid_angle_offset`/`least_squares` profile uses the general
declared-aromatic minimum-basis participants, packed Rust
least-squares planes, bounded compiled spatial candidates and shared whole-group
PBC validation. General plane-pair angle/offset geometry belongs to `structure`;
chemical rules belong to `physchem`; the detector owns acceptance and sparse
observation assembly. Compound selection membership is shared with ionic and
ring tools. No additional dependency or detector-specific Rust kernel is added.

For this default profile, four explicit unitful cutoffs define the rule: positive centroid distance,
angular deviation, lateral offset and maximum orthogonal plane deviation. The
acute unoriented angle lies in [0, pi/2]; the angular cutoff must be below pi/4.
Parallel geometry requires the angle near zero and both lateral offsets within
cutoff. Edge-to-face requires the angle near pi/2 and at least one offset within
cutoff. Both rings must satisfy planarity. A pair has positive distance within
cutoff. Inclusive comparisons permit one float64 ULP without an absolute
geometric tolerance. Angular roundoff remains strictly below pi/4 to preserve
disjoint classes. Zero cutoffs therefore require numerical exactness.
This is `centroid_angle_offset@1`, not an energy, attraction or Mol* parity claim.

The other supported profiles preserve their reference geometry. ProLIF uses
ordered 5/6-member SMARTS rings; MDTraj geometry uses declared aromatic cycles.
Their centroid-to-first-two-member normals support parallel and edge-to-face
criteria with plane-intersection tests for the latter. The Mol* profile uses
three-atom planes, centroid distance, parallel/perpendicular angular classes
and lateral offset. These profiles have their own defaults and exact boundary
rules; they do not inherit the proposal's planarity or covalent exclusions.
Mol* feature discovery/refinement is outside the geometric reproduction. Common
MolSysMT whole-participant MIC geometry is an explicit extension, not a claim of
identical historical reference PBC behavior.

The following planarity and exclusion rules describe the default proposal:

Self, overlapping/fused and directly covalently linked rings are excluded.
Other intramolecular geometries are included; dative bonds do not impose an
exclusion. There is no clash or residue/component filter. A minimum basis is
not every cycle or a universal aromaticity model. Degenerate rings fail rather
than silently claiming evaluated-empty observations; warped, nondegenerate
rings exceeding the explicit planarity cutoff are excluded.

Internal, incident and disjoint between searches operate on complete ring
participants. Candidate searches are planned only between relevant sets and
repeated for every requested structure. Partial compound calculation selections
fail. Completed-result queries can inspect individual atoms. Source indices,
not atom or structure IDs, define axes. Repeated frames evaluate once, sorted;
empty evaluated frames remain explicit. `chemical_state='structure'` requires
one known state across selected frames.

One sparse `pi_pi` relation has `ring_a`/`ring_b` groups ordered by source ring
membership. Occurrences store evidence for parallel or edge-to-face geometry,
centroid distance, acute angle, both offsets and both RMS/maximum deviations.
Lengths and angles carry explicit nm/radians units. Producer versions retain
MolSysMT and NetworkX versions at calculation time. Geometry/chemistry method
versions, cutoffs, state and full recognition versus eligible observation scope
are recorded. The default is Interactions; InteractionsDict is optional. Named
attachment is explicit. Both named and standalone H5MSM 0.5 round trips preserve
this contract and public occurrence indices.

MIC shifts are added to all atoms of ring_b using row box vectors; ring_a is
zero. Every ring must already be whole in its anchor-relative image. Split
rings fail, and general unwrapping/reconstruction remains a separate future
PBC operation. Only the selected MIC image is reported. With pbc=True and no
box, geometry is nonperiodic under the explicit mic_when_box_available policy.

Rich H5MSM selections require eager materialization within the full source-coordinate
estimate; forced file streaming requires index selections or all.

All supported forms with sufficient chemistry and coordinates can use their
normal getters/conversion routes. Real heavy coordinate delivery, rather than
an iterator name, permits streaming. H5MSM index selections prepare native
chemistry and association metadata once without materializing structural series
or named analyses. Selected coordinates and fitted planes are block bounded;
accepted occurrences remain resident. Numeric working estimates are not a
process-RSS guarantee or an incremental result writer.

Analytical contracts, fixed molecular memberships, an independent exhaustive
covariance-plane oracle on Trp-cage/villin and controlled periodic translations
are covered by `tests/interactions/pi_pi/` and
`tests/scientific_truth/curated/test_pi_pi_interactions.py`. These establish
bounded geometric evidence, not a universal physical interpretation. See
[the detector benchmark guide](benchmarking/pi_pi.md) for reproducible
calculation/query/memory/H5MSM controls. The API remains Experimental.

## Cation-pi observations

`interactions.cation_pi.get_cation_pi_interactions` defaults to
`centroid_distance_angle`/`smarts_5_6`. It reproduces the ProLIF 2.2.2 core
definition using RDKit SMARTS for cations and 5/6-member aromatic rings,
unweighted centers and a centroid-to-first-two-member normal. The default
centroid distance is at most 0.45 nm and the acute normal/center angle is in
[0, 30 degrees], inclusively. There is no added offset, planarity or covalent
exclusion. SMARTS cations can include resonance motifs whose individual atoms
have zero formal charge; this is not the formal-charge-center proposal.

`centroid_distance_offset`/`three_atom_plane` reproduces Mol* geometry on
declared positive charge centers and aromatic participants: distance at most
0.60 nm and lateral offset at most 0.20 nm by default. It does not reproduce
all Mol* valence-based feature discovery. `centroid_angle_offset`/`least_squares`
uses general formal-charge centers, declared aromatic cycles and fitted planes,
with four caller-supplied unitful cutoffs. It excludes overlapping or directly
covalently connected participants. It is a MolSysMT proposal, not a validated
improvement over either reference definition; comparison remains under
`uibcdf/molsysmt#271`.

Relations retain complete `cation` and `ring` participant groups. Sparse results
store centroid distance, acute normal angle, height, lateral offset and plane
deviations with explicit units, selected state, actual scope, rule parameters,
evidence, producer versions and reference attribution. Normal orientation is
recorded where the profile requires it. Repeated structure indices evaluate
once; evaluated-empty frames remain explicit. Individual-atom result queries
are supported even though calculation selections must contain whole groups.
Named attachment is explicit, with InteractionsDict and H5MSM round trips.

Shared whole-participant PBC validation anchors the cation and records the
ring image; split groups fail rather than guessing atom images. Native/H5MSM
coordinate execution can be chunked, but accepted observations remain in RAM.
Public inputs remain form-agnostic when the form supplies sufficient chemistry
and coordinates; soft RDKit imports are confined to the SMARTS profile.
Guards are `tests/interactions/cation_pi/` and
`tests/scientific_truth/curated/test_cation_pi_interactions.py`. See
[benchmarking/cation_pi.md](benchmarking/cation_pi.md) for bounded measurements.

## Halogen bonds

`interactions.halogen_bonds.get_halogen_bonds` is experimental. The descriptive
`distance_two_angles` method uses `smarts_donor_acceptor`, reproduced from
ProLIF 2.2.2 XBAcceptor/DoubleAngle. There is no new software-name method alias.
The independent `physchem.get_halogen_bond_sites` tool uses general declared-graph
SMARTS matching with lazy RDKit, ordered donor/halogen and acceptor/reference
pairs, full-source recognition before selection, explicit chemical-state choice
and checked match limits. Required assignments are not inferred or repaired.

The four singleton roles are donor D, halogen X, acceptor A and acceptor reference
R. Each eligible R is a distinct relation; occurrence identity therefore does
not collapse to the X-A pair. All four roles count for internal/incident/between
scope, including a selection touching only R. Default inclusive geometry is
X-A <=0.35 nm, D-X-A in [130,180] degrees and X-A-R in [80,140] degrees. Inputs
carry physical units; result columns declare nm/radians. Undefined angles are
skipped, and no numerical tolerance is added. Floating-point conversion and angle
evaluation can change membership exactly on a cutoff while geometry agrees to
roundoff. Curated guards separate exact-boundary characterization from interior
reference parity; they do not broaden the production criterion.

The source documents its geometry as adapted from Auffinger et al. (PNAS 2004,
DOI 10.1073/pnas.0407607101). That paper uses element-specific X-O van der Waals
limits, so this profile is not called `auffinger` or claimed to reproduce those
limits. Detached bibliography credits the paper as the adapted criterion and
ProLIF as the reference implementation. Actual producers are MolSysMT and RDKit;
ProLIF is not a runtime dependency. Recognition alone does not credit a geometric
paper. The source patterns exclude F as terminal donor and positive acceptors,
include eligible non-triple acceptor links, and preserve every reference neighbor.
No residue fingerprinting or additional covalent/intramolecular exclusion is added.

General chain MIC reconstructs adjacent D-X, X-A and A-R vectors in one image
anchored on D. Stored row-box shifts reproduce both angles and distances. This
is a MolSysMT extension, not reference PBC parity, ring closure or full-component
reconstruction. Native/H5MSM numeric selections project coordinate blocks through
the shared executor and compiled spatial candidates. Full chemistry and accepted
sparse output remain resident; numeric budgets exclude Python overhead and RSS.
Rich file selections need bounded eager loading or fail under forced streaming.
Known-empty coverage, exact source indices, scientific parameters, periodic images,
producer versions and optional Ackredit bibliography survive named/typed H5MSM 0.5
round trips. The detector does not attach results automatically.

Guards are `tests/interactions/halogen_bonds/`,
`tests/physchem/test_get_halogen_bond_sites.py` and
`tests/scientific_truth/curated/test_halogen_bonds.py`. The offline oracle contains
seven declared chemical controls and 56 structures, generated by unmodified
ProLIF 2.2.2 with recorded source hashes. It is not biological accuracy evidence
or qualification of the MolSysViewer renderer. The implementation record is
`uibcdf/molsysmt#277`.

## Hydrophobic observations

`interactions.hydrophobic.get_hydrophobic_interactions` is experimental. Its
`atom_pair_distance` method with `smarts_hydrophobic_atoms` profile reproduces
ProLIF 2.2.2 Hydrophobic/Distance SMARTS and the inclusive 0.45 nm default.
There is no new software-name selector or assumed original author. The independent
`physchem.get_hydrophobic_sites` tool uses general declared-graph SMARTS matching
with lazy RDKit, full-source recognition before selection, one selected chemical
state and checked match caps. These are atomic chemical features, not values from
`get_hydrophobicity` residue scales or evidence of solvent-mediated attraction.
The exact pattern includes selected neutral aromatic/carbon/sulfur environments
and Br/I, excludes charged atoms and carbon linked to N/O/F, and does not match
all terminal methyl carbons or F/Cl. Missing assignments are not repaired.

Relations contain two distinct singleton atoms in ascending source-index order,
with roles `hydrophobic_1` and `hydrophobic_2`. A symmetric observation is stored
once per frame. Roles do not encode ligand/protein direction. Same-atom records
and reverse duplicates are excluded, while distinct coincident atoms can have
zero distance. No covalent or intramolecular filter is added to the raw reference
core; callers should select disjoint ligand/environment sets for interfacial
analyses. Internal/incident/between semantics cover both atoms and retain the
actual typed search universe. Selected repeated structures are evaluated once;
known-empty scope and unevaluated coverage remain distinct.

Native/H5MSM numeric selections use the shared projected coordinate executor and
compiled bounded spatial candidates. Canonical pair MIC anchored on the lower
atom index preserves identical observed images even when a search originates
from the other selected side, including MIC ties. Integer row-box shifts
reconstruct the measured distance. It is a single winning MIC image, not an
all-images enumeration or reference residue-fingerprint pruning. Inputs carry
length units and result distances declare nm. Exact-cutoff comparisons have no
added geometric tolerance; roundoff can affect boundary membership.

Full chemistry and accepted sparse output remain resident; coordinate/candidate/
accumulator estimates reserve one quarter/one eighth/one half of the configured
numeric RAM, excluding Python overhead and process RSS. Rich H5MSM selections
need bounded eager loading or reject forced streaming. Calculation does not
attach automatically. Typed and named H5MSM 0.5 round trips preserve scope,
occurrence identity, original producers, evidence and reference bibliography.
Optional Ackredit credits completed computations, not subsequent reads.

Mol* carbon/C-H and fluorine rules, F-F exclusion and 0.40 nm default are a
separate alternative. This initial profile does not establish energetic accuracy,
universal chemical typing, complete Mol* parity or renderer qualification.
Guards are `tests/interactions/hydrophobic/`,
`tests/physchem/test_get_hydrophobic_sites.py` and
`tests/scientific_truth/curated/test_hydrophobic_interactions.py`. The unmodified
ProLIF oracle has seven controls, 21 synthetic structures and 119 unordered
observations; exact site/pair identities and geometry agree across three forms.
See `uibcdf/molsysmt#278` for the implementation record.

## Metal coordination candidates

`interactions.metal_coordination.get_metal_coordination` applies the descriptive
`metal_ligand_distance` criterion with profile `smarts_metal_ligand`: pinned
ProLIF 2.2.2 MetalDonor chemical sites and inclusive distance <=0.28 nm without
added tolerance. `physchem.get_metal_coordination_sites` owns graph recognition.
The supported metal set is Ca, Cd, Co, Cu, Fe, Mg, Mn, Ni and Zn; oxygen,
restricted nitrogen and negative nonpositive atoms can be candidate ligands.
This is not a universal all-metal chemical model. Dative assignments remain
independent of covalent graph matching and are never created or removed.

Relations are directed `metal_coordination_candidate` pairs with singleton
`metal`, `ligand` roles, measured distance in nm, explicit evaluated-frame
coverage, source indices, declared typed atom scope and original producer versions.
Self pairs are excluded; intramolecular/covalent neighbors remain included. An
atom matching both roles can produce two distinct reversed-role relations.
MIC images anchor on the metal and preserve actual pair geometry. Do not interpret
proximity as a certified bond, oxidation state, coordination number or energy.

The general pattern matching, projected executor, compiled bounded pair searches
and sparse accumulator are reused. Guards live under
`tests/interactions/metal_coordination/` and
`tests/physchem/test_get_metal_coordination_sites.py`; offline independent original
ProLIF evidence is in `tests/scientific_truth/curated/test_metal_coordination.py`.
See `uibcdf/molsysmt#280` for implementation evidence and limits.

## Indexed water-mediated hydrogen-bond paths

`interactions.water_bridges.get_water_bridges` implements `hbond_water_path`
with profile `indexed_water`. Keyword-only `order=1` (default) means exactly one
water and two simultaneous hydrogen bonds; `order=2` means exactly two distinct
waters and three simultaneous bonds. This is an exact order, not an upper bound.
Store separate named analyses when both orders are wanted. The previous method
`two_hbonds_one_water` retains its literal order-one meaning; it rejects order two.
Its single-water numerical behavior remains supported.

Recognize full-source neutral explicit O-H-H components through
`physchem.get_water_sites`, then reuse `hbonds.get_hbonds` for same-frame legs
incident on water oxygen. `hbond_method` and `hbond_profile` retain the exact leg
criterion; the default is Baker-Hubbard. ProLIF WaterBridge and MDAnalysis
WaterBridgeAnalysis are references for the path concept, separately attributed
from the executed leg criterion. Their pruning, residue aggregation and
maximum/minimum-order policies are not a promised pipeline equivalence.

Relations store six or nine singleton roles in two or three directed D-H-A
triples: `leg_1_donor`, `leg_1_hydrogen`, `leg_1_acceptor`, and similarly for legs
two and three. Each mediator oxygen repeats in adjacent legs; alternative and
bifurcated hydrogens remain identifiable. Unused water H is not an additional
participant. Distinct external heavy atoms and distinct mediator oxygens are
required. Order the traversal from the lower external heavy-atom index, while
preserving each leg's donor/acceptor orientation. Reversal is not a second path;
different observed leg triples are distinguishable paths. Repeated endpoint
cycles and observations from different frames are excluded.

`internal`, `incident` and `between` apply to all actual participating atoms,
including mediator atoms and observed H. Internal excludes endpoint-only
selections; use incident for those. Between requires all participants in the
union of two disjoint sets and at least one in each. Evaluated empty frames remain
distinguishable from unevaluated frames. Atom removal drops incomplete relations
without recalculating other interactions.

Measures retain `leg_1_`, `leg_2_` and (for order two) `leg_3_` prefixes and explicit
nm/radians units. Empty order-two output has all fifteen float64 measure columns.
The complete attributed leg parameters remain in `hbond_parameters`, with
`mediator_order` and the versioned path rule identifying the composition.
Translate each next leg onto its shared mediator oxygen image, then anchor at the
first role. Preserve all relative geometries; reject incompatible repeated-atom
images or int32 overflow. This reusable image join belongs to `pbc`, and handles
arbitrary role counts without reconstructing images from scalar distances.
Named and typed H5MSM 0.5 conversions preserve roles, images, occurrence indices
and original software/bibliographic provenance; no schema change is needed.

Accepted legs remain resident. Order one batches per-water pairs; order two
batches terminal fan-out only across observed water-water edges. No all-water
pair array or dense trajectory tensor is allocated. Numeric working estimates
include leg arrays and sparse packing, but not complete Python/graph RSS.
Higher orders, implicit H, endpoint-only scope modes, virtual-site recognition,
caller-explicit leg sites and an incremental writer remain outside this contract.
Guards: `tests/interactions/water_bridges/`,
`tests/physchem/test_get_water_sites.py` and
`tests/scientific_truth/curated/test_water_bridges.py`. The independent oracle
uses original ProLIF HBDonor observations and separate simple-path enumeration;
controlled geometries check all eight three-leg directions analytically.
Implementation records: `uibcdf/molsysmt#281` and `uibcdf/molsysmt#282`.

## Planned family coverage

All eight original families under `uibcdf/molsysmt#250` now have implemented
experimental detectors: hydrogen bonds, disulfide candidates, ionic observations,
pi-pi, cation-pi, halogen bonds, hydrophobic observations and metal candidates.
One- and two-water hydrogen-bond bridges extend this inventory as the ninth family
under the maintainer's 2026-10-01 decision. These additions are not mandatory
new 1.0 gates; metal-specific physical criteria, paths through more than two waters and
broader comparative validation remain refinements rather than implied support.
Phosphate/sulfate and aromatic charge-delocalization
extensions (`uibcdf/molsysmt#262`) and comparison of the proposed aromatic
criteria (`uibcdf/molsysmt#271`) are open refinements of existing tools, not
unimplemented detector families. See the [namespace roadmap](pending_proposals/organize_interaction_detection_by_family_before_1_0.md)
for the implementation inventory and release boundary.

## Current result behavior and 1.0 target

The experimental `molsysmt.Interactions` class stores one method's typed observations,
relation participants and roles, explicit evaluated-structure coverage,
declared atom search scope, measurement units, evidence labels, and optional
periodic image vectors. Its `software` dictionary maps software names to the
versions that produced the observations. Both hydrogen-bond and disulfide adapters capture
`{"molsysmt": molsysmt.__version__}` during calculation. Views, remapping,
invalidation, InteractionsDict, standalone HDF5, selective HDF5 projections,
and H5MSM 0.5 preserve this metadata. The optional field is stored once per
analysis in versioned metadata, without a per-occurrence column. Readers of
older payloads with no field return `{}`: unknown producer versions are never
filled from the installed reader version. External producers may supply their
own name/version entries through `from_records(software=...)`. Its
`query` method supports local-index structure lists and atom-set `incident`,
`internal`, and `cross` semantics; `between` supports disjoint atom sets.
`from_records`, `to_dict`, `relation`, `remap`, `invalidate_structures`,
`replace_structures`, `save`, and
`load` provide construction,
inspection, and standalone HDF5 round trips. The current file schema version
is 2; readers also accept schema 1. It is independent of H5MSM 0.5.
`load` materializes the result in memory.
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

The experimental class has no public lazy file-backed query, direct detector-to-file
stream or incremental add/remove editor. Saving an existing analysis uses bounded
HDF5 windows without packing edited occurrence columns. `invalidate_structures()` returns an independent
snapshot with the selected frames unevaluated and their occurrences removed;
it shares immutable numeric storage and does not replace an incremental editor. It represents one
molecular-system index space and one method per instance. `MolSys.interactions`
holds a mapping of named full results with matching atom and structure axes.
Each result retains local-to-source atom and structure index arrays plus the
sizes of both source axes. Extraction composes those maps; an appended
structure has source index `-1` and is unevaluated. The caller-supplied source
label stays with the mapped result. These are positional indices, never
element IDs.
Numeric columns are owned, read-only buffers, independent of writable inputs.
Storage fields cannot be reassigned and the measurement mapping is read-only.
Construction pays for ownership once. Local invalidation updates coverage and
compact removed-row intervals without allocating surviving occurrence columns.
Its allocations depend on covered structures and metadata, not trajectory row
count. Repeated invalidation references one immutable base rather than a chain
of earlier filtered snapshots. Atom/structure queries filter validity and reuse
the base's lazy inverse indexes. Occurrence handles are positions in the active
analysis and survive full typed/file round trips, including parallel observations.

Partially invalidated rows remain physically resident in shared storage but
cannot be returned as active observations. If no observations survive, the new
result releases its occurrence-base reference. Earlier results/views can still
retain that storage. Complete occurrence/image/measurement attribute access
materializes and caches a packed active result; remapping, pickling and typed
serialization may materialize it temporarily. HDF5 writing traverses active
blocks directly, without using or changing a packed cache. Interchange-only packing
is released after success or failure unless a caller previously requested the
cached complete columns. These operations are not bounded incremental writers.
No coordinates are copied and invalidation triggers no disk write. Owner
setters apply the same validity operation separately to each affected analysis.
Native copy, extraction, and removal preserve or remap attached results;
newly appended structures remain unevaluated. Adding atoms to a target with
analyses preserves the target's previous atom search scope: new
atoms are outside the evaluated universe and have source index `-1`. Adding
from a source that carries analyses, or appending its structures, requires an
explicit merge policy and currently fails. H5MSM 0.4 and
MolSysDict 0.1 exports reject a system with attached analyses because those
formats cannot store them. The design and remaining gates are
tracked by [`uibcdf/molsysmt#251`](pending_proposals/design_a_sparse_public_interactions_result_and_serialization_contract.md).

### Bounded HDF5 writing

`Interactions.save`, `h5msm.write_layers`, `h5msm.write` and native full-axis
`convert(..., to_form='file:h5msm')` use one interaction-group writer. Codec 2,
H5MSM 0.5 and named collection schema 1 are unchanged. Packed, invalidated and
recalculated results retain their global relation/evidence indices, canonical
frame/row order, parallel observations, participant image vectors, evaluated-empty
coverage, scope/maps, units, software and execution records.

The writer traverses contiguous active source slices, coalescing adjacent ranges
without constructing a complete occurrence-position array. Recalculated slices
translate relation/evidence codes only in the current window. Each observation-column write
has a ceiling of 1 MiB, reduced by `max_ram_usage * chunk_memory_fraction`, with
an irreducible 16-byte floor. Image vectors have their own windows, so one very
populated frame or a high-arity relation cannot force a frame-sized image copy.
This byte policy is for serialization, not the coordinate-frame `chunk_size`.
Registry buffers and source maps are also written in windows. Identity maps are
checked in windows; label codes do not require a complete numeric code array.

Frame offsets, coverage and execution membership metadata still require
work/storage proportional to the structure axis; execution-table preparation
can concatenate its frame vectors. Existing registry/string tables, source observations and
coordinate domains remain resident; HDF5/compression caches and Python overhead
are outside this numeric-window bound. Temporary arithmetic can hold multiple
windows. This is not a total-RSS guarantee, compaction, resumable append writer or
a detector-to-disk output route. No `ChunkedExecutor` coordinate traversal is
performed by serialization. Detector input streaming remains owned by that executor.

Saving never calls the edited result's complete-column packing boundary, even
when a packed cache already exists. Such a cache is preserved as requested by its
caller. Loading still materializes a selected named analysis. Typed dictionaries,
pickle and remap may still pack all active observations. Nontrivial atom/frame
selections or form conversion can materialize/remap before the writer is reached.
Existing standalone overwrite and H5MSM new-path policies are unchanged. A failed
write raises rather than returning a completed analysis; partially written files
are not checkpoints and are not automatically removed.

Guards are `tests/interactions/test_bounded_hdf5_writer.py`: full read-back
semantics, public paths, forbidden packing, preserved caches, tiny numeric
windows and dense single-frame traced-allocation scaling. The reproducible
comparison with the previous writer is maintained in
[the H5MSM benchmark guide](benchmarking/h5msm.md).

### Frame-scoped execution provenance

`parameters` stores scientific criteria, chemical recognition, periodic conventions
and attribution. `execution_records` returns a tuple of dictionaries, each with an
int64 `structure_indices` vector and a `details` dictionary. Frame sets partition
the current evaluated coverage exactly, including zero-row frames. Each vector is
sorted. Projected detectors record `execution`, `execution_chunks` and
`memory_policy`. Water paths additionally retain `hbond_execution`. Legacy eager
adapters expose unknown details (`{}`); no runtime information is invented.

Construct a single calculation with `execution={...}` or supply explicit
`execution_records`; these arguments are mutually exclusive. Returned vectors
and details are independent copies. Internal storage holds one frame vector per
execution, without columns or Python objects per occurrence. Query projection
uses binary searches in sorted run vectors. Its work depends on requested
coverage and execution record count, rather than scanning all occurrence rows
or each complete run's frame vector. Numeric byte accounting includes these
vectors; Python metadata overhead remains excluded.

Queries clip records to selected evaluated frames, even when atom/type filters
yield no observations. Invalidation drops invalid frames from exposed provenance.
Replacement keeps source run membership for surviving frames and appends incoming
records. A stored `execution_chunks` continues to describe the original calculation,
whose frame membership may have been reduced by later edits; it is not a count of
retained frames. Remap transforms membership into new local frame indices, including
repeated extraction. Producer versions remain analysis-wide and must match for
replacement. No geometry hashes or automatic recalculations are introduced.

InteractionsDict and the embedded/standalone interaction group write codec version
2. H5MSM remains 0.5; its named-analysis collection remains schema 1. The dictionary
stores records with NumPy frame vectors. HDF5 stores `execution/details` as JSON
strings plus int64 `execution/structure_offsets` and `execution/structure_indices`;
offsets delimit each record's frame set. An analysis with no evaluated frames writes zero records and
offsets `[0]`. Readers validate exact coverage partitioning. Older MolSysMT builds
supporting only codec 1 reject codec-2 analyses and need updating before reading
newly written files.

Current readers accept version 1 and migrate only the historical runtime keys
`execution`, `execution_chunks`, `memory_policy` from parameters, plus these keys
in water-path `hbond_parameters`, into execution details. Scientific criteria and
references are preserved. Missing details remain unknown. Pickle, typed conversion,
named H5MSM round trips and private selective HDF5 projections preserve the records.
The guard is `tests/interactions/test_execution_provenance.py`, including real
detector recalculation with changed execution policy and native coordinate edits.

### Compatible frame replacement

`Interactions.replace_structures(replacement, skip_digestion=False)` is a
validated native public boundary returning an independent full analysis. The
replacement must be another full result with matching local/source dimensions,
source maps/label, method, parameters, software producer versions, measure units
and effective evaluation scope. It replaces every incoming evaluated frame,
including zero-row frames, and unions coverage. Query views and extracted axes
are rejected. Parameter equality includes scientific criteria and attribution.
Execution policy and block counts may differ; frame-scoped provenance preserves
how retained and incoming observations were calculated. Known/unknown periodic
images cannot coexist in populated active blocks; empty coverage does not
synthesize images.

The private layout stores disjoint immutable source blocks, relation/evidence
maps and frame ownership/count offsets. Relation keys include kind, ordered
roles and all ordered member indices; matching keys reuse existing indices and
new keys append. Occurrence indices are positions in the new frame-ordered
analysis, preserving parallel rows, and survive full interchange. Incoming row
order within each frame is preserved. Frame queries route directly to their
owner blocks and create selected occurrence buffers sharing the global relation
registry. Atom queries reuse block-local inverse indexes, creating indexes for
new blocks only as needed. Replacement allocation depends on the frame axis,
relation registry and active block count, without copying unaffected occurrence
columns. Previously requested packed caches are not retained by new edits.
Unchanged catalog columns, existing block relation/evidence maps and unaffected
sorted frame vectors are shared. Coverage unions preserve first-seen order using
array membership, without a Python dictionary containing the whole frame axis.
Identity maps are implicit. A private sorted fingerprint/index pair uses 16
numeric bytes per relation and is created lazily when incoming definitions need
matching. Fingerprints are process-local accelerators: every hit compares the
full typed participant key, so collisions never identify different relations.
The cache is retained by the returned registry and extended on additions; it is
not persisted or part of public relation identity. Fully matching catalogs avoid
building it. Adding definitions still allocates catalog buffers, and the cold
index build remains proportional to the catalog size. Owner indices use int32
when the number of active blocks permits it, with an int64 fallback; public atom,
structure, relation and occurrence indices keep their existing types.

Edits flatten ownership rather than referencing earlier patched snapshots, and
fully superseded blocks are released unless another result retains them. A
partially active block still retains its old rows; unused relation definitions
are retained. Automatic block/registry compaction and direct detector-to-file
accumulation remain pending. Complete columns, remap, pickle and typed export can
pack the full active analysis, with interchange-only caches released afterward.
HDF5 export writes active source blocks directly in bounded numeric windows. Selected views
own their projected rows; existing packed-base views still share base rows.
Guards are `tests/interactions/test_frame_replacement.py` and the real Buch
recalculation workflow in
`tests/form/molsysmt_MolSys/test_geometry_edit_interactions.py`.

### Explicit observation compaction

`analysis.compact()` returns an independent full packed snapshot. It removes
references to invalidated/replaced occurrence blocks and resets query indexes,
which rebuild lazily. It does not mutate the source, run a detector or attach
the result to a molecular system. Query views are rejected. Already packed
analyses return a separate wrapper sharing their immutable columns.

Coverage order, evaluated-empty structures, local/source axes, atom search
scope, scientific/producer metadata and frame-scoped execution records are
preserved. Active occurrence order, relation indices and occurrence handles are
unchanged. Unused relation definitions and evidence labels remain in the catalog;
compaction does not renumber or prune them. It releases retired observation
storage, rather than rewriting chemical identity or the relation registry.

The implementation reuses active source-span traversal from HDF5 export, copies
one destination column at a time and translates relation/evidence codes in
bounded windows. Variable-arity periodic vectors are copied independently of
row windows. Each completed column obtains an immutable bytes owner, retaining
input-alias protection. While freezing a column, its mutable and immutable
destinations briefly coexist. Peak additional allocation therefore includes
the packed output plus at most one destination column, bounded translation
workspace and frame/run metadata. This is not a constant-memory or total-RSS
guarantee. It does not use or change a source materialization cache.

Old analyses and query snapshots continue to own their data. Replacing the named
analysis and releasing those references permits Python to reclaim retired
buffers; the allocator need not immediately reduce process RSS. Compaction is
explicit because it has an allocation and copying cost. HDF5 export alone does
not require it. Automatic compaction and unused-registry pruning remain future
decisions. The guard is `tests/interactions/test_compaction.py`, including
weak-reference release, dense-frame allocation limits, nonconsecutive/atom
queries, parallel and four-body periodic observations, and codec round trips.

The installed editable ArgDigest checkout used for this checkpoint precedes the
fix for `uibcdf/argdigest#17`. The method temporarily checks non-boolean skip
flags through the existing argument digester; remove this fallback when the
public runtime floor includes that provider fix. The public decorator and
normal boolean trusted-delegation contract remain intact.

Native MolSys coordinate and box form setters invalidate all named analyses
in their selected frames, including evaluated-empty frames. The affected
occurrences and coverage are removed; untouched frames, metadata, index maps,
and old result/query snapshots remain intact. Moving an atom that did not
previously participate still invalidates the frame: new candidates can appear.
Compound participants may also depend on the moved atom's coordinates. Empty atom/frame selections and
identifier/time writes do not invalidate. Full geometry assignment with attached
analyses cannot resize the frame axis; use the supported extract/append routes.
Invalidation snapshots are staged before delegation. Allocation or validation
failures before delegation preserve the system; after delegation starts,
failures conservatively leave selected frames unevaluated because writes may
be partial. No detector runs automatically. Recalculate the complete declared
atom scope of an affected frame explicitly. Assigning a detector result under
an existing name replaces that analysis and does not merge its frame coverage;
`current.replace_structures(fresh)` instead replaces only the frames evaluated
by a compatible full recalculation. This validity primitive does not run a detector. Direct writes through a
separate Structures object still require explicit owner invalidation.
The guard is `tests/form/molsysmt_MolSys/test_geometry_edit_interactions.py`.

Public `msm.set` atom-state and scientific bond-state assignments on native
MolSys invalidate all evaluated frames in every named analysis. Owner-level
`MolSys.chemical_states` replacement does the same. This includes atom charges,
aromaticity, radical and hydrogen assignments, stereochemistry, bond order and
type, aromaticity/conjugation, direction and reference atoms, component
participation and evidence. Bond IDs remain labels and do not invalidate.
Empty atom/bond selections preserve analyses. The atom-state assignment changes
the selected chemical state, not just a frame's copy; supplying one state or
some `structure_indices` therefore does not narrow this conservative rule.
No complete per-analysis chemical dependency graph is assumed.

Assigning or clearing `structure_chemical_state_index` changes the frame
association and invalidates only the selected frames, including evaluated-empty
ones. Invalid associations and incompatible ChemicalStates replacements are
rejected before publishing edits. The same staged snapshot primitive protects
allocation failures and uncertain delegate writes; no detector is invoked.
Earlier views, metadata, source maps and original producer versions survive.
The guard is `tests/form/molsysmt_MolSys/test_chemistry_edit_interactions.py`.

Raw arrays/DataFrames, separate Topology or ChemicalStates aliases, direct
Topology replacement and MolecularMechanics changes require explicit owner
invalidation. They do not acquire an observer protocol through the controlled
setters. Editors of individual observations and finer chemical dependencies remain
separate work; invalidation itself shares the read-only columns.
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
The [MolSysViewer review packet](interactions_molsysviewer_review.md) supplies
pinned fixture/test commands and states the scope of local consumer evidence.

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
