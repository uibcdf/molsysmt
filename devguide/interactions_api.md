# Interaction Analysis API

`molsysmt.interactions` owns chemically interpreted analyses over molecular
systems. Distance-only proximity remains a geometric primitive in `structure`;
it is not by itself an interaction classification. The first public families
are `interactions.hbonds`, `interactions.disulfides`, and the experimental
`interactions.ionic`, `interactions.pi_pi`, `interactions.cation_pi` and
`interactions.halogen_bonds` and `interactions.hydrophobic`. Other families need
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

## Planned family coverage

The initial eight-family inventory under `uibcdf/molsysmt#250` has seven
implemented experimental detectors: hydrogen bonds, disulfide candidates,
ionic observations, pi-pi, cation-pi, halogen bonds and hydrophobic observations.
Metal coordination does not yet have a public detector. Water-mediated hydrogen
bonds are also explicitly pending under the maintainer's 2026-10-01 decision.
These additions need
separate scientific contracts and reusable chemical preparation; they are not
mandatory 1.0 gates. Phosphate/sulfate and aromatic charge-delocalization
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
