---
summary: Provide reusable declared-state atom correspondences and unaligned symmetry-corrected RMSD.
issue: uibcdf/molsysmt#310
status: resolved
opened: 2026-10-13
closed: 2026-10-13
verification: measured
area: [api, structure, docs]
guard: tests/structure/test_get_symmetry_corrected_rmsd.py
normative: devguide/chemical_correspondence.md
blocked_by: []
supersedes: []
---

# Chemically constrained pose RMSD

**Reported:** DockingMT requests a provider-owned correspondence operation in
uibcdf/molsysmt#310. On 2026-10-13 the maintainer accepted implementation of the
two reusable public tools, including explicit scientific attribution.
**Status:** Resolved in source with an experimental declared-state profile.
Frozen release artifacts and uncorrected DockingMT populations remain unchanged.

## What

Separate chemical admission of source-index bijections from geometric evaluation.
Expose `topology.get_atom_correspondences` without coordinates and
`structure.get_symmetry_corrected_rmsd` without ligand superposition.

## How

The experimental `declared_graph_isomorphism@1` profile retains a complete
covalent component, including atoms omitted from the metric. RDKit enumerates
non-uniquified stereochemical matches; MolSysMT checks declared atom/bond labels,
population membership and source axes. Enumeration requests one extra candidate
to detect overflow. Equivalent metric projections retain one full-context witness.
Rust positional kernels evaluate the mappings through projected coordinate blocks.
Cached maps are checked against ordered current chemical digests and witnesses.

Offline bibliography distinguishes methodological inspiration (Bell and Zhang,
2019; Meli and Biggin, 2020) from RDKit/MolSysMT execution. The algorithms are not
claimed as faithful reproductions. Completed results retain detached records;
optional Ackredit contributes contextual credit to the application's session.

## Why

Pose RMSD must preserve the ligand's position/orientation relative to its receptor.
Arbitrary atom order can inflate RMSD, while element-only assignment can falsely
admit chemically inequivalent atoms. The benzamidinium +1 case in the issue admits
phenyl symmetry but must not silently exchange the declared N-single and N-double/+1.

## What is measured and what is assumed

Initial controls enumerate the analytic twelve benzene dihedral permutations and
two benzamidinium phenyl permutations. Detailed tests, examples and performance
receipts are added before closure. Numeric working budgets are estimates; graph
objects, import caches, caller-owned source arrays and process RSS are outside them.
There is no hard wall-clock matching bound or arbitrary-macromolecule speed claim.

## What was refuted

- Positional selection lists cannot carry a permutation: ordinary atom selection
  sorts indices. Correspondence pairs preserve both independent source axes.
- RDKit `GetBestRMS` aligns the probe and changes its pose.
- Default `CalcRMS` search omits chirality and may symmetrize conjugated terminal
  groups. Its explicit-map geometry is useful as a bounded comparison oracle.
- Existing uniquified SMARTS matches collapse distinct permutations on one atom set.
- Missing chemical evidence, a truncated search and arbitrary nearest neighbors
  cannot certify the requested chemical minimum.

## Scope and exclusions

One complete covalent component, one fixed state per source, complete declared
atom chemistry, supported covalent orders and assigned potential tetrahedral/
double-bond stereo. No protonation, resonance, tautomer, aromaticity or coordinate
stereo inference; no dative or enhanced stereo, superposition or implicit imaging.
Many query structures compare against one reference. Original positional results
require an explicit baseline map. No DockingMT threshold/report rewrite, new
H5MSM result domain or frozen artifact change is part of this implementation.

## Acceptance criteria

Positive/negative chemistry controls; independent analytic symmetry and positional
geometry; source reordering and explicit baseline; units and empty/repeated/nonconsecutive
structure selections; native/file eager/chunked parity; search/budget failures;
cache mutation and changed-chemistry refusal; real Ackredit reuse, absence, failure,
lazy import and detached reading; updated API, Foundations, Toolbox, Cookbook and course.

## Dependencies and risks

RDKit remains optional and guarded. Candidate enumeration can be combinatorial,
especially with explicit H. The initial profile rejects incomplete or unsupported
chemistry rather than weakening constraints. Provider implementation completes
here. DockingMT owns its
separately registered corrected evaluation under its existing scientific issues.

## Provenance

Original demand and 3PTB applied-state clarification: uibcdf/molsysmt#310.
Bell and Zhang: https://doi.org/10.1186/s13321-019-0362-7.
Meli and Biggin: https://doi.org/10.1186/s13321-020-00455-2.
Reviewed RDKit matching/CalcRMS source is available in the project checkout;
runtime versions are retained per result. This is source qualification, not a
new installed release or retrospective corrected docking claim.

## Resolution — 2026-10-13

Implemented both public tools and classified them experimental in the normative
API registry. The first profile preserves exact declared chemical assignments,
including indexed-H representation and implicit-H policy. It returns empty maps
for incompatible supported declarations, and refuses missing, malformed or
unsupported chemistry. A future H-representation/resonance policy requires its
own explicit scientific contract; neither is silently applied here.

Complete-context witnesses are lexical within each deduplicated metric projection.
Cached results validate schema, rule version, populations, current chemical
context, witnesses and consistency digests before geometry. Rust component and
positional-RMSD primitives are reused; there is no new compiled implementation.
The shared chemical view avoids restoration hooks on borrowed state records.
Canonical software bibliography and CIP declarations are shared across general
chemical tools, preventing same-version metadata conflicts in Ackredit.

Source qualification on Linux/Python 3.14: **255 passed**, no skips/failures,
using `-n 12 --receptor=llm`. The selection includes the two new tool modules,
real Ackredit controls, existing positional RMSD, substructure matching,
rotatable bonds, CIP, ring/aromaticity tools and existing interaction attribution.
The 56 warnings are the existing bundled H5MSM 0.4 deprecation route. The analytic
benzene dihedral group and unaligned displacement controls are independent truth;
RDKit CalcRMS with explicit qualified maps checks geometry only. No entire chemical
profile, installed artifact, downstream recovery cutoff or universal speed is certified.

Both doctests pass (eight examples). All three new notebooks and the added cells
in Common Core modules 13/16 execute with the development Python 3.14 kernel;
unchanged course cells retain their existing outputs. Course structure, docstrings,
API stability, dependencies and the 14 fast gates pass. Sphinx HTML builds without
new notebook/schema errors; the existing warning debt remains uibcdf/molsysmt#144.

The reproducible [benchmark tool](../../../devtools/scripts/benchmark_symmetry_rmsd.py)
and [receipt](../../../devtools/data/symmetry_rmsd_20261013.json) separate warm
construction+evaluation, cached native eager/chunked and file chunked routes.
The receipt records raw samples, environment, source hashes/working-tree state,
input hashes, numeric storage and whole-process peak RSS. Refer to the receipt
for timings; this one six-atom/12-map workload is not a large-molecule study.

The durable rules are in [the chemical correspondence contract](../../chemical_correspondence.md).
Provider guards are `tests/structure/test_get_symmetry_corrected_rmsd.py`,
`tests/topology/test_get_atom_correspondences.py` and
`tests/topology/test_correspondence_attribution.py`. DockingMT owns adopting this
public provider in a separately registered corrected evaluation and preserving
its original source-identity results.

## CI formatting recovery — 2026-10-13

The first published source head passed developer-guide and Conda-governance checks,
but Ruff and suite conformance refused four Python files at their format step.
Local lint had passed; the complete formatting command had not covered these four
final edits. Their whitespace was corrected and both repository-wide commands,
`ruff check .` and `ruff format --check .`, now pass. Scientific behavior, inputs
and benchmark runtime hashes are unchanged. The source checkpoint retains its
255-test evidence; the follow-up head's remote checks are verified separately.
