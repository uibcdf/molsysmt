---
summary: Implement halogen-bond observations with reusable site recognition
issue: uibcdf/molsysmt#277
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [api, docs, structure, units, tests]
guard: tests/interactions/halogen_bonds/test_get_halogen_bonds.py
normative: devguide/interactions_api.md
blocked_by: []
supersedes: []
---

# Halogen-bond observations with reusable sites

**Reported:** 2026-10-01, maintainer authorization to continue the family roadmap.
**Status:** Resolved; the first reference profile is implemented and remains experimental.

## What

Add an experimental halogen-bond detector and independently usable chemical-site
recognition. Preserve full geometric participants, sparse coverage and optional
scientific attribution without adding a competing chemical store.

## How

`physchem.get_halogen_bond_sites` uses general declared-graph SMARTS matching
to identify ordered donor/halogen and acceptor/reference pairs. The first
`interactions.halogen_bonds.get_halogen_bonds` profile is
`distance_two_angles`/`smarts_donor_acceptor`, reproducing the pinned ProLIF 2.2.2
XBAcceptor/DoubleAngle core. Defaults are X-A <=0.35 nm, D-X-A in [130,180]
degrees and X-A-R in [80,140] degrees. Public angular ranges retain units.

The four roles are `donor`, `halogen`, `acceptor`, and `acceptor_reference`.
Different reference atoms on one acceptor produce distinct directional
observations, not a silently aggregated atom pair. Scope queries count all
four participants. Calculation does not attach results automatically.
Projected coordinate blocks, existing compiled candidates and general angle/MIC
tools supply geometry. Periodic observations must be represented coherently as
one D-X-A-R chain and report the actual images. Input chemistry is not rebuilt
or repaired. Accepted sparse results remain in RAM.

## Why

Halogen bonding was pending in the original family inventory. ProLIF documents
its geometry as adapted from Auffinger et al., not as the original paper's exact
criterion. The latter uses element-specific X-O van der Waals limits and
discusses approximately 165/120-degree geometry. Scientific/descriptive naming
and separate attribution preserve this distinction. General recognition belongs
in `physchem`, not in a renderer or a detector-specific conversion branch.

## What is measured and what is assumed

**Inspected:** pinned ProLIF commit
`19f1800218387c49536eb9d3e8cd3044fdb337ee`, its XBAcceptor SMARTS and DoubleAngle
distance/inclusive-angle comparisons. Mol* uses another elemental/neighbor rule,
a 0.40 nm default, near-linear donor geometry and a different acceptor test;
it is not an alias of the initial profile.

**Contract-tested:** 523 tests passed in 118.63 seconds with the affected suite:

```bash
python -m pytest tests/interactions tests/physchem/test_get_hbond_sites.py \
  tests/physchem/test_get_halogen_bond_sites.py \
  tests/scientific_truth/curated/test_attributed_interaction_methods.py \
  tests/scientific_truth/curated/test_halogen_bonds.py --receptor=llm
```

Fourteen warnings came from explicit low-RAM controls (9) and deprecated H5MSM
0.4 fixture reads (5). Native, RDKit, composite and H5MSM form tests pass.
Controls protect all four role memberships, frame deduplication, known-empty
coverage, neighbor identity, units, image reconstruction, typed/named persistence,
optional Ackredit, block projection and numerical-budget failures.

**Scientifically validated, bounded scope:** unmodified ProLIF 2.2.2 generated
seven chemical controls / 56 synthetic structures / 18 observations. Its source
module hashes are recorded in the offline JSON. The 21 form/oracle guards compare
interior relation identities exactly and measures within 1e-12. MolSysMT records
15 default observations: three nominal simultaneous distance/angle-boundary
observations accepted by the angstrom reference fall below the 80-degree angular
limit after conversion/evaluation in nm. Their geometry differs by roundoff
(within 1e-15), not a changed chemical rule. The guard independently verifies
those measures and actual strict-cutoff membership instead of broadening the
production threshold or silently changing oracle expectations. The initial
reference guard exposed this distinction; it is explicit in the normative API,
docstring, tutorial and curated provenance. No biological accuracy is claimed.

**Lifecycle-tested:** both public docstrings pass 11 examples; three new
notebooks execute with saved outputs. The four Module 38 conceptual extensions
are updated; their existing biological code/outputs are unchanged and were not
rerun. The course validator passes 156 notebooks; the docstring validator passes
208 public functions and stability registry passes 229 symbols. Ruff, lazy
soft-dependency validation and public signature drift checks pass. Sphinx renders
the new API/tutorial/recipe pages with resolved new links and no parser diagnostics
on those three pages. The full build still emits existing unrelated docstring,
MyST/course and reference diagnostics; it is not a clean release-documentation gate.

**Estimate:** coordinate/chain blocks reserve one quarter of configured numeric
RAM, candidates one eighth and sparse accumulation/packing one half. Chemistry,
Python overhead and process RSS are outside those budgets. No new comparative
runtime benchmark, GPU route, or argument for a new Rust kernel is claimed.

## What was refuted

- Naming the adapted profile `auffinger` without qualification would imply
  original-paper thresholds that it does not use.
- Reusing hydrogen-bond acceptor SMARTS would change the published halogen rule.
- Collapsing all acceptor reference atoms would discard one angle's identity.
- Independent angle-wise PBC shifts can fail to describe one observed geometry.

## Scope and exclusions

The first profile reproduces geometry and SMARTS on complete source chemistry,
with all-frame observations rather than residue fingerprints. It does not
claim attractive energy, original-paper parity, full Mol* feature parity,
water-mediated detection or universal halogen/acceptor chemistry. F is not a
halogen donor in this profile. No ProLIF production dependency or new compiled
kernel is planned; further kernels require measured justification.
MolSysViewer's initial renderer remains independently scoped under
`uibcdf/molsysviewer#114`; this family is not a new 1.0 consumer gate.

## Acceptance criteria

- Public functions are form-agnostic, digested and unit-safe with lazy RDKit.
- Analytical distance/two-angle controls and a pinned independent reference
  protect site membership, inclusive boundaries and rejected geometry.
- Nonconsecutive/repeated frames, empty frames, all atom-set scope modes,
  four roles, periodic images and deterministic results are verified.
- Native, RDKit, composite chemistry/coordinates and H5MSM calculations agree;
  named/typed persistence retains occurrence and attribution metadata.
- Chunked delivery does not load unrelated analyses or full structural series;
  candidate and resident-result budget failures remain explicit.
- Docstrings, User Guide, Cookbook, Four Paths, API registry and relevant gates
  reflect implemented behavior before closure.

## Provenance and references

- [Pinned ProLIF source](https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/interactions/interactions.py)
- [Pinned geometric core](https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/interactions/base.py)
- [Auffinger et al., 2004](https://doi.org/10.1073/pnas.0407607101)
- [ProLIF paper](https://doi.org/10.1186/s13321-021-00548-6)
- `uibcdf/pharmacophoremt#11` records the requested downstream reference review.

## Resolution

The general chemical-site tool lives in `physchem`; source graph SMARTS matching
remains in `topology`, chain reconstruction in `pbc`, numeric angle measurements
and compiled spatial candidates in `structure`. The consumer owns only its
scientific criterion, role-aware scope and sparse accumulation. Existing
hydrogen-bond imaging delegates the shared chain helper without changing its
scientific acceptance or metadata contract, covered by the affected suite.

The initial profile is complete as an experimental detector. Original-paper
element-specific criteria and the different Mol* elemental/neighbor geometry
remain future independent profiles, not aliases. Hydrophobic association, metal
coordination and water-mediated hydrogen bonds remain pending under #250; no
placeholder public APIs were added. MolSysViewer renderer qualification and
whole-library Ackredit adoption retain their existing separate issue scopes.

## Validation provenance

Measured on 2026-10-01, Linux x86_64, Python 3.13.14, NumPy/RDKit from the shared
MolSysSuite development environment (RDKit 2025.09.5). The source patch is based
on published review commit `915ef542f`; the closing issue names the implementation
commit. Installed MolSysMT metadata `0.21.0+606.ga03eb4bf6` identifies the local
package installation and is not proof of this source revision. The isolated
ProLIF 2.2.2 oracle installation lived under `/tmp` only; no production dependency
or shared environment was changed. Runtime source hashes and Python/RDKit versions
are in `devtools/data/halogen_bond_validation_systems.json`.
