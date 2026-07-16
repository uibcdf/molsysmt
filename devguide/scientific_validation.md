# Scientific Validation Contract

This normative document defines the evidence required before MolSysMT describes
a stable scientific operation as scientifically validated. The executable suite
lives under `tests/scientific_truth/`.

## Evidence hierarchy

Scientific validation requires at least one expected result that is independent
of the implementation under test:

1. a closed-form analytic construction;
2. a versioned external reference dataset or published value;
3. an independently implemented external tool with a documented convention.

Parity between MolSysMT forms, engines, CPU/GPU paths, or eager/chunked execution
is valuable regression evidence but is not independent scientific truth.
Metamorphic properties strengthen an oracle but do not replace one.

## Box and PBC convention

Box matrices use shape `(n_structures, 3, 3)`, with each row representing one
cell vector. Lengths are `(a, b, c)`. Angles are `(alpha, beta, gamma)`, where
alpha is between `b` and `c`, beta is between `a` and `c`, and gamma is between
`a` and `b`. Lengths use nanometers, angles use radians internally, and volumes
use cubic nanometers.

Minimum-image calculations use fractional coordinates relative to the row-vector
box matrix and return the shortest periodic displacement supported by the cell.

## Tolerance governance

The executable tolerance source for this suite is
`tests/scientific_truth/conftest.py`.

- Public box lengths, angles, and reconstructed matrices are rounded to six
  decimal places by their current API implementation. Their absolute tolerance
  is therefore `5e-7` in the reported unit, with zero relative tolerance.
- Small, well-conditioned float64 determinant and MIC examples use an absolute
  tolerance of `1e-12`, with zero relative tolerance.
- External geometry comparisons that traverse float32 storage, notably MDTraj
  trajectories and periodic-cell representations, use an absolute tolerance of
  `1e-6` in the reported unit, with zero relative tolerance. The same governed
  tolerance is used for the paired MDAnalysis comparisons so the external
  agreement matrix has one conservative threshold.
- Format precision, approximate algorithms, and single-precision backends must
  define separate named tolerances with an explicit numerical rationale.

A tolerance must not be loosened solely because a test fails. Increasing one
requires documenting whether the cause is floating-point propagation, public
rounding, file-format precision, an external convention, or an intentionally
approximate method.

Signed periodic quantities must be compared through their wrapped difference.
For dihedrals, use `atan2(sin(observed-expected), cos(observed-expected))` so the
equivalent branch-cut values `-pi` and `+pi` agree. Exact analytic invariants
take precedence over external numerical artifacts. For example, the identity
least-RMSD is exactly zero even when a float32 QCP implementation reports a
small positive value for a five-atom self-comparison.

## Initial validation index

| Quantity | Public API | Evidence | Analytic system | Tolerance |
|---|---|---|---|---|
| Box lengths and angles | `molsysmt.pbc.get_lengths_and_angles_from_box` | Analytic | Orthorhombic `2 x 3 x 4 nm`; triclinic `(2, 2, 3) nm`, `(90, 90, 60) deg` | `5e-7` in output units |
| Box construction | `molsysmt.pbc.get_box_from_lengths_and_angles` | Analytic | Canonical 60-degree row-vector cell | `5e-7 nm` |
| Box volume | `molsysmt.pbc.get_volume_from_box`; `get_volume_from_lengths_and_angles` | Analytic | `24 nm^3`; `6 sqrt(3) nm^3` | `1e-12 nm^3` |
| Orthorhombic MIC distance | `molsysmt.structure.get_distances` | Analytic | `x=0.1` and `1.9 nm` in a `2 nm` cell | `1e-12 nm` |
| Triclinic MIC distance | `molsysmt.structure.get_distances` | Analytic | fractional displacement `(-0.1, -0.1, 0)` in the canonical 60-degree cell | `1e-12 nm` |

## Ensemble and transformation validation index

| Quantity | Public API | Evidence | Analytic system | Tolerance |
|---|---|---|---|---|
| Geometric and weighted center | `molsysmt.structure.get_center` | Analytic | Three explicit Cartesian points with unit and `(1, 2, 3)` weights | `1e-12 nm` |
| Radius of gyration | `molsysmt.structure.get_radius_of_gyration` | Analytic and metamorphic | Three collinear points; weighted two-point distribution; common rigid transform | `1e-12 nm` |
| RMSF | `molsysmt.structure.get_rmsf` | Analytic and metamorphic | Two atoms in two explicit frames; common rigid transform | `1e-12 nm` |
| Rigid fitting | `molsysmt.structure.least_rmsd_fit` | Analytic | Asymmetric four-point structure with a known rotation and translation | `1e-12 nm` |
| Principal geometric axes | `molsysmt.structure.get_principal_axes` | Analytic and metamorphic | Anisotropic six-point Cartesian distribution; translated and rotated copy | `1e-12` |
| Principal inertia axes | `molsysmt.structure.get_principal_axes` | Analytic | Diagonal six-point unit-mass distribution with moments `(10, 20, 26)` | `1e-12` |
| Principal-axis alignment | `molsysmt.structure.align_principal_axes` | Analytic and failure-path | Rotated anisotropic distribution; isotropic degenerate distribution | `1e-12` |
| Explicit proper rotation | `molsysmt.structure.rotate` | Analytic and metamorphic | Known per-frame matrices; rotation/inverse round trip | `1e-12 nm` |
| Temporal unwrapping | `molsysmt.pbc.unwrap` | Analytic | Orthorhombic and canonical 60-degree triclinic boundary crossings | `1e-12 nm` |
| Covalent reconstruction and wrapping | `molsysmt.pbc.wrap_to_pbc`; `wrap_to_mic` | Analytic | Boundary-spanning bonded chains in orthorhombic and triclinic cells | `1e-12 nm` |

Weighted centers and radii reject empty selections, non-finite or negative
weights, length mismatches, and zero total weight. A one-atom radius of
gyration and a one-frame RMSF are exactly zero. Temporal unwrapping and
single-frame covalent reconstruction are separate contracts: `unwrap`
restores each atom's trajectory continuity, while the wrapping functions use
bond connectivity only when `keep_covalent_bonds=True`.

Principal axes are rows ordered by ascending eigenvalue and are canonicalized
to a right-handed basis. Their individual signs remain arbitrary. Equal
eigenvalues define a degenerate subspace, so principal-axis alignment rejects
those structures. Explicit rotation matrices must be finite, orthonormal, and
have determinant +1. Least-RMSD fitting rejects selections with fewer than
three non-collinear points because they cannot determine a unique 3D rotation.

Chunked Rg and RMSF are required to agree with eager execution to `1e-12 nm`
on the bundled pentaalanine trajectory. This is execution-parity evidence and
does not replace the analytic oracles above.

## External geometry validation index

The initial external fixtures are declared as NumPy arrays in
`tests/scientific_truth/conftest.py`. The external tools and MolSysMT each consume
those arrays directly; no MolSysMT conversion path constructs the oracle input.
The first implementation was verified with MDTraj 1.11.1 and MDAnalysis 2.10.0.

| Quantity | MolSysMT API | MDTraj oracle | MDAnalysis oracle | System | Tolerance |
|---|---|---|---|---|---|
| Pair distances | `get_distances` | `compute_distances` | `calc_bonds` | Four Cartesian points, two rigidly related frames | `1e-6 nm` |
| Angles | `get_angles` | `compute_angles` | `calc_angles` | Two explicit triplets, two rigidly related frames | `1e-6 rad` |
| Signed dihedrals | `get_dihedral_angles` | `compute_dihedrals` | `calc_dihedrals` | One explicit quartet, two rigidly related frames | `1e-6 rad` |
| Raw RMSD | `get_rmsd` | — | `rmsd` without centering or superposition | Reference plus rigid transform | `1e-6 nm` |
| Least RMSD | `get_least_rmsd` | `rmsd` | `rmsd` with centering and superposition | Reference plus rigid transform | `1e-6 nm` |
| Triclinic MIC distance | `get_distances` | `compute_distances` with periodic cell | `calc_bonds` with triclinic dimensions | Canonical 60-degree cell | `1e-6 nm` |

The oracle versions above are provenance for the initial verification, not an
instruction to pin soft dependencies globally. The dedicated scientific CI
environment must record its resolved versions and run all indexed external tests
without skips.

## Curated molecular validation index

Artifact hashes and source notes are maintained in
`tests/scientific_truth/curated/PROVENANCE.md`.

| System | Scientific quantities | Independent readers or oracle | Frames |
|---|---|---|---|
| Met-enkephalin | Backbone distances, angles, and signed dihedrals | MDTraj and MDAnalysis | One PDB model |
| Pentaalanine | Coordinates, box, time, MIC distances, phi/psi dihedrals, and CA least-RMSD | MDTraj HDF5 plus paired H5MSM artifact | Distributed subset of a 5000-frame trajectory |
| Solvated chicken villin HP35 | Covalent reconstruction after deliberate periodic image shifts in distinct solvent molecules | MDTraj periodic bond distances | Frames 0, 10, and 19 |
| Trp-cage 1L2Y | Reader identity, CA coordinates and distances, phi dihedrals, and CA least-RMSD | MDTraj and MDAnalysis | All 38 NMR models or a documented representative subset |
| NGLView `md_1u19` | Boundary-spanning MIC distances and XTC box delivery | MDTraj and MDAnalysis | Frames 0, 25, and 50 |

The curated layer tests scientific behavior on realistic molecular data. The
paired HDF5/H5MSM pentaalanine check is artifact parity evidence; the geometry
calculations become external scientific evidence when their expected values are
computed independently by MDTraj.

## Adding validated operations

Each new entry must state the mathematical quantity, convention, input and
output shapes, units, periodic behavior, dtype, tolerance, degenerate behavior,
and oracle provenance. Curated molecular reference systems must be bundled,
versioned, deterministic, and documented before they become validation evidence.
