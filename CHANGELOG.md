# Changelog

All notable changes to MolSysMT are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
from `1.0.0` onward. The `1.x` public contract and deprecation policy are defined in
`devguide/deprecation_policy.md`; the stable public surface is
`devtools/data/public_api_stability.json`.

Detailed pre-1.0 history is recorded in the git tags and commit log.

## [Unreleased] — 1.0.0 (in preparation)

First stable release, establishing the `1.x` public API contract. Highlights below;
individual entries are finalized as the release is cut.

### Added
- Explicit form support-tier registry (`molsysmt/_private/form_tier.py`): every
  discovered form is classified Tier 1/2/3; unknown forms fail instead of receiving
  contractual support.
- Machine-readable public API stability registry
  (`devtools/data/public_api_stability.json`) with `stable` / `experimental` /
  `outside-contract` classifications, and a stability-derived function support-tier
  mapping enforced by `devtools/scripts/validate_function_tiers.py`.
- Release-readiness gate: `devguide/release_gate.md` policy and
  `devtools/scripts/release_gate.py` aggregator.
- `physchem.get_electronegativity`: per-atom Pauling electronegativity
  (dimensionless; unknown/dummy elements return `NaN`).
- `physchem.get_sasa` accepts a unit-aware `probe_radius` argument (default 1.4 Å)
  and an `n_sphere_points` argument (Shrake–Rupley sampling density), both honoured
  by the native `MolSysMT` and the `mdtraj` engines.
- Reusable CPU cell-list neighbour-search primitive
  (`molsysmt.lib.structure.neighbor_list`): `neighbor_list_csr` (CSR offsets/indices,
  vacuum and periodic, query/ref generality) and `neighbor_pairs`, shared by
  `physchem.get_sasa` and `structure.get_contacts` (the former per-function
  `get_contacts_cell_list` implementation was folded into this primitive). The
  primitive also optionally returns neighbour distances (`return_distances`).
- `physchem.get_sasa` gains a `use_cell_list` argument (default `'auto'`) that
  accelerates the native CPU Shrake–Rupley occlusion scan from O(N²) to ~O(N) for
  large systems, with numerically identical results. The kernel builds a
  per-structure cell list and parallelises over the flattened (structure, atom)
  work, so both a single large structure and many structures scale (subject to the
  usual `configure.parallel_mode` / `parallel_threshold` gating).
- `structure.get_neighbors` threshold mode now uses the cell-list primitive on the
  native path (atom neighbour search, `output_type='numpy.ndarray'`), replacing the
  full O(N·M) distance matrix with an ~O(N) search; results are identical and it
  transparently falls back to the distance-matrix path for the other cases. The
  h-bond engines (`hbonds.get_buch_hbonds`, `hbonds.get_luzard_chandler_hbonds`)
  inherit the speed-up since they generate candidates through `get_neighbors`.
- First-class support for dummy atoms/groups (`DUM`/`X`) in `physchem`: neutral
  pseudo-elements with zero mass and radius, and neutral group-property fallback
  in the residue-level getters (`get_charge`, `get_hydrophobicity`, `get_polarity`,
  `get_volume`, `get_surface_area`, `get_area_buried`, `get_buried_fraction`,
  `get_transmembrane_tendency`), so whole-system queries no longer raise on dummy
  entries while genuine unknown residues still raise.

### Changed
- (to be finalized) conversion-fidelity and chemical-state hardening across form
  adapters.
- `physchem.get_sasa` now uses a unified Shrake–Rupley sampling density of 240
  sphere points by default for both engines (previously 100 for the native
  `MolSysMT` engine and 960 for `mdtraj`). Numerical SASA results shift slightly
  accordingly; use `n_sphere_points` to restore the previous densities.

### Deprecated
- `molsysmt.warmup_numba`: use `molsysmt.warmup`. Not removed before `1.1.0`.

### Removed
- The MMTF and MSMPK forms were removed before the 1.0 public contract was established
  (BinaryCIF/mmCIF are the supported structural exchange formats; H5MSM is the native
  persistence format).

### Fixed
- Doctest collection no longer shadows re-exported public symbols under
  `--import-mode=importlib` (e.g. `molsysmt.convert`).

[Unreleased]: https://github.com/uibcdf/MolSysMT/compare/main...HEAD
