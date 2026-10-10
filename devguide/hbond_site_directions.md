# Fixed-state hydrogen-bond site directions

**Role:** normative public contract. **Tracking:** uibcdf/molsysmt#375.
**Stability:** experimental, bounded maintainer admission on 2026-10-10.

`interactions.hbonds.get_hbond_site_directions` composes public `get_hbond_sites`, general
SMARTS matching and the numeric geometry shared with `structure.get_vectors`. It never changes chemistry,
coordinates or named interactions, adds H, infers a pocket or selects a
pharmacophore projection distance. Forms must supply the attributes required by
the selected state and geometry. RDKit is lazy and optional, but required by this
first profile's environment matching even with elemental site recognition.

Recognition, local direction characterization and occurrence detection share
the public `interactions.hbonds` namespace. Site directions depend on a donor/
acceptor definition and local coordinates, not on previously calculated hydrogen
bonds. These tools remain reusable by pharmacophore and other client workflows.
The former pre-release `physchem` exports were removed on 2026-10-10; their
signatures and result schemas are unchanged. Generic geometry remains in
`structure`, periodic conventions in `pbc`, and graph matching in `topology`.

## Scientific definition

`method='ideal_local_geometry'` describes geometric hypotheses; `site_method`
names recognition independently. Its detached result remains in `sites`, with
the original chemical rule, state, evidence, versions and bibliography. Elemental
recognition can admit unsuitable acceptors; geometry does not make those rules
universally accurate or silently widen the following bounded coverage.

| Role/environment | Definition | Indexed support |
| --- | --- | --- |
| Recognized donor–H pair | Observed normalized D→H | D, H |
| Neutral ordinary aldehyde/ketone/amide C=O oxygen | Two ideal trigonal directions in its substituent plane | O, C, C substituent |
| Neutral pyridine-like aromatic nitrogen | Negative normalized sum of normalized neighbor bonds | N, two covalent neighbors |
| Neutral nitrile nitrogen | Opposite normalized N→C | N, C |

For carbonyl O let `u` be the unit O→C bond. Project the unit C→substituent bond
perpendicular to `u` and normalize it as `t`. The directions are
`-u/2 + sqrt(3)*t/2` and `-u/2 - sqrt(3)*t/2`: unit vectors making 120 degrees
with O→C. Choose the lowest-index heavy C substituent, otherwise the lowest-index
indexed H. This determines the transverse sign and local slot 0; renumbering
source atoms can exchange local slot labels. No global axis fixes the sign.

SMARTS in `interactions/hbonds/_hbond_directions.py` require declared orders, formal charges
and aromatic metadata. Acids/carboxylates, esters and C=O attached to S/P are
excluded from the ordinary carbonyl model. Amines, ether/alcohol/water O, sulfur/
phosphorus and dative-bound acceptors are unsupported. Covalent extra neighbors
are restricted by the matched environment. A recognized donor's observed D→H
vector is available independently of the acceptor coverage.

These are independently specified ideal geometric hypotheses, inspired by
[RDKit feature-direction helpers](https://www.rdkit.org/docs/source/rdkit.Chem.Features.FeatDirUtilsRD.html),
inspected at `cbfb37abddcd5b5feeac97d53530ae6be83cac0d`. Exact helper parity is not
claimed: the single-heavy-neighbor helper's observed carbonyl cone behavior is
recorded in the owning proposal. The result bibliography labels the source as
`geometric_inspiration`, separately from executed RDKit/MolSysMT versions. No
paper is credited as establishing this numerical profile and no electronic
orbital, energetic accuracy or improved scientific performance is claimed.

## Axes and sparse representation

The dictionary schema is `molsysmt.hbond_site_directions@1`, experimental.
All atom indices refer to the original source axis. Donor sites follow sorted
recognized (D,H) pairs; acceptor sites follow sorted recognized acceptor indices.
One atom can be both donor and acceptor, and a donor can have several indexed H.
The roles are separate sites, not collapsed by atom index.

- `site_atom_indices`: int64 anchors; `site_roles` uint8 (0 donor, 1 acceptor).
- `site_models`: uint8 codes 0 unsupported, 1 observed donor-H, 2 carbonyl
  trigonal, 3 aromatic N bisector, 4 nitrile linear.
- `support_atom_indices` and `support_atom_offsets`: CSR support membership,
  anchor first. Supporting neighbors can lie outside the requested atom selection;
  both donor and H must be selected, whereas only the acceptor anchor must be.
- `evaluated_structure_indices`: ordered int64 source indices, retaining repeats.
- `status`: uint8 `(n_selected_structures, n_sites)`, 0 unsupported chemistry,
  1 defined geometry, 2 undefined geometry. This bounded resident matrix preserves
  missing outcomes; it is not an atom-pair or padded direction tensor.
- `directions`: float64 `(n_records, 3)`, dimensionless, finite and normalized.
  `origins`: aligned length quantity in the active PyUnitWizard standard/backend.
- `direction_site_indices`, `direction_structure_indices` and
  `direction_structure_positions`: int64 correspondence. The last distinguishes
  repeated requested structures. `direction_indices` is uint8 local multiplicity
  (0, or 0/1 for carbonyl).
- `image_offsets`: int64 `(n_records + 1,)` indexing int32 `image_vectors`
  `(n_packed_support_atoms, 3)`. Each record has the number and order of supporting
  atoms of its static site. No Python object is stored per directional record.

Ordering is requested structure position, site, local direction. A typed empty
result retains `(0,3)` vector/image matrices, empty int64 correspondence, offset
`[0]` and the appropriately shaped status matrix. There is no unevaluated marker:
the requested axis is the evaluated scope of this call. Unsupported and undefined
remain distinct even when both yield no directional records.

## Missing geometry and periodic images

Missing indexed carbonyl-plane support, zero bonds or collinear carbonyl/aromatic
support are undefined. Dimensionless normalization/plane degeneracy uses 1e-12.
Unsupported or undefined sites emit no finite direction. Nonfinite coordinates
and singular/unrepresentable boxes raise rather than inventing results.
`chemical_state='structure'` requires one known state across the requested axis;
an empty axis cannot resolve such a state. Explicit/reference state geometry
accepts an empty requested structure list.

With PBC and an available box, the shared general vector kernel supplies the actual
MIC image of each supporting bond. Row-vector images reconstruct
`r_support + image @ box`, with anchor image zero. Carbonyl C carries the O→C
image and its substituent carries the sum of O→C and C→substituent images.
N neighbors and donor H carry their anchor-bond image directly. Composed images
outside int32 range fail explicitly. Without a box or with `pbc=False`, images
are zero. Reconstruction is local and immutable; whole molecules are not moved.

## Delivery, attribution and limits

Full declared chemistry is recognized before selecting anchors. H5MSM 0.5 axes
are obtained from metadata by the common index validator; its chemistry-only
reader supplies the state, and `ChunkedExecutor` supplies projected coordinates.
Forced streaming requires a declared route. Eager work and blocks are bounded.
Sparse resident output, status, packing, unit presentation and a block reservation
are checked against `configure.max_ram_usage`; source graphs, Python/allocator
overhead are outside the numeric estimate. This is not an RSS guarantee or
unlimited trajectory result. The general Rust vector/MIC primitive is reused;
the remaining fixed-arity model arithmetic is vectorized NumPy. Projected blocks
call the numeric helper owned by `structure` and shared with public `get_vectors`,
without repeating form discovery or converting intermediate lengths to user
units. PBC validation remains owned by `pbc`; final origins alone are presented
through PyUnitWizard.

Optional Ackredit receives one completed calculation, plus the chemical
recognition it composes; never a credit event for every direction. The producer
version is recorded at computation. Loading a newer package cannot rewrite it.

The result is a detached derived dictionary, not an `Interactions` analysis.
It is not attached automatically, has no direct named H5MSM persistence route
and does not alter the existing stored Interactions contract. Consumers retain
its typed arrays, source axis and provenance in their own derived workflow.
H5MSM input round trips in the examples store molecular inputs, not this result.

## Verification

`tests/interactions/hbonds/test_get_hbond_site_directions.py` checks independent analytic
carbonyl and nitrogen controls, observed donors, exclusions, unsupported versus
undefined outcomes, multiplicity, rotations/translations, neighbor order, actual
orthogonal/triclinic images, input/output units and four backends, source
immutability, nonconsecutive/repeated indices, selected states, H5MSM projected
delivery, bounded chunks, budgets and typed empties. RDKit is not used as an
independent universal geometry oracle. The public notebook, persistence recipe
and independently executable course section demonstrate the contract.

This source delivery does not qualify frozen installed artifacts under
uibcdf/molsysmt#334. Broader acceptor coverage and consumer adoption remain in
uibcdf/molsysmt#375; environmental refinement belongs to uibcdf/molsysmt#323.

## Local performance controls — 2026-10-10

Run `python benchmarks/get_hbond_site_directions.py --output /tmp/site_directions.json`
with the development interpreter and optimized native extension. Each case runs
in a fresh process, records one cold and three warm calls, checks analytic
geometry and retains source hashes. The
[receipt](../benchmarks/baselines/get_hbond_site_directions_20261010.json) was
produced after focused tests finished, without concurrent test execution. Other
host load was not controlled. These are observed costs, not thresholds or proof
of energetic/scientific accuracy.

The retained receipt predates the namespace migration and therefore records the
original `physchem` file paths and their exact hashes. It is historical evidence;
the maintained benchmark now calls `interactions.hbonds` and records its paths.

| Case | Sites × structures | Finite directions | Warm median | Top-level numeric bytes |
| --- | --- | --- | --- | --- |
| Many structures | 1 × 10,000 | 20,000 | 0.216 s | 2,430,114 |
| Many sites | 100 × 1,000 | 200,000 | 0.436 s | 23,517,816 |
| Periodic support | 100 × 1,000 | 200,000 | 0.457 s | 23,517,816 |

Times include recognition, projected delivery, model arithmetic, sparse packing,
final concatenation, units and attribution. Numeric bytes include the top-level
arrays and origins; nested metadata and Python overhead are additional. Process
peak RSS in the receipt includes imports, input coordinates, outputs and caches
and must not be confused with result storage. The reducer timings separately
include geometry and block packing, excluding recognition/final presentation.

Preliminary measurements exposed repeated public-wrapper preparation in tiny
blocks. Sharing the general numeric vector helper removes that redundant work;
no additional compiled model kernel was justified by these bounded workloads.
The preliminary run overlapped other checks and is not retained as a controlled
before/after speed comparison. Large heterogeneous chemistry, disk throughput
and installed package qualification are outside these measurements.
