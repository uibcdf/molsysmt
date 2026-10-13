---
summary: Support anchored and caller-supplied chemical correspondences for pose RMSD
issue: uibcdf/molsysmt#387
status: resolved
opened: 2026-10-13
closed: 2026-10-13
verification: measured
area: [structure, api]
guard: tests/structure/test_get_symmetry_corrected_rmsd.py
normative:
blocked_by: []
supersedes: []
---

# Anchored and caller-supplied chemical correspondences

**Reported:** 2026-10-13, maintainer request following the accepted #310 tools.
**Status:** Resolved in source, contract-tested and parity-tested; installed release qualification is separate.

## What

Extend `topology.get_atom_correspondences` and `structure.get_symmetry_corrected_rmsd`
with partial compulsory atom pairs and complete caller-proposed metric maps.
Preserve chemistry validation, independent raw baselines, deterministic source-index
results, bounded coordinate delivery, units and existing scientific attribution.

## How

Keyword-only `fixed_atom_correspondence` supplies injective partial query/reference
source-index pairs, including omitted atoms in the complete covalent context.
`candidate_atom_correspondences` supplies one complete selected-population map or
an explicit collection. Both can be combined if compatible. Full-context chemical
extensions validate proposals; no invalid proposal is silently discarded.

Anchors use temporary RDKit atom properties on detached graph copies inside the
compiled search. Candidate extension probes also encode exact atom/bond labels and
selected membership. Greedy one-witness existence probes select lexical complete
witnesses without enumerating omitted-H permutations. Geometry reuses the existing
Rust RMSD reducer and projected coordinate executor.

`search_scope` identifies unrestricted, anchored or supplied-map completeness.
The constraints are detached and included in the consistency digest. Cached results
retain their scope; combining them with new arguments is rejected as ambiguous.
Earlier unconstrained schema-1 caches remain unrestricted.

## Why

Scientists may know atom correspondences independently of chemical symmetry, or
receive selected candidate maps from an upstream comparison. Anchors can reduce
search; complete proposals can bypass global enumeration while remaining chemically
checked. Baseline pairs previously defined only the raw positional measure.

## What is measured and what is assumed

Initial focused source tests: 92 passed on 2026-10-13 with Python 3.13.14, twelve pytest
workers and pytest-receptor. Two benzene anchors permit max_matches=1 whereas an
unrestricted request at that cap fails. One anchor yields two rather than twelve
completed candidates. This is a candidate-count observation, not a wall-clock claim.

No large-ligand timing or total-RSS benchmark has been made for the extension.
Input normalization and graph allocation remain outside the numeric RAM estimate.

## What was refuted

- Post-filtering all symmetries cannot reduce the enumeration workload before its cap.
- Replacing isotope labels to encode pins would change chemically meaningful evidence.
- A valid selected-only map is insufficient when its omitted context cannot extend.
- A minimum over proposed maps cannot be called an unrestricted symmetry minimum.
- Silently discarding invalid proposals would conceal a caller's correspondence error.

## Scope and exclusions

Same declared fixed-state profile as #310; no chemical relaxation, resonance
normalization, alignment, MIC or protonation changes. Constrained results remain
experimental. No package publication, tag, dependency-floor or H5MSM schema change.

## Acceptance criteria

Public tests protect analytic anchored/supplied RMSDs, enumeration pruning,
whole-context witness validity and ordering, independent source axes, invalid input
and chemistry, reuse/digest changes, and H5MSM streaming with nonconsecutive/repeated
structures and active units. Existing attribution and unconstrained results regress
unchanged. Docstrings, Foundations, Toolbox, Cookbook and course reflect the API.

## Dependencies and risks

RDKit remains optional and guarded. The compiled search API is used through existing
support, with no new dependency. Existence probes bound returned vectors but not
search time; canonical-witness probes have quadratic worst-case count per candidate.

## Provenance

2026-10-13, Linux development environment, Python 3.14. Dependency versions and
final validation commands are recorded in the resolution after completion.

## Resolution — 2026-10-13

Implemented both keyword-only arguments in the owning topology tool and geometry
consumer, preserving positional arguments and the schema-1 unconstrained reuse route.
The normative contract is [chemical_correspondence.md](../../chemical_correspondence.md).
All user-facing layers describe conditional scope and distinguish anchors/proposals
from the independent raw baseline. Attribution continues to report inspiration and
executed software separately; no new borrowed scientific algorithm is claimed.

Validation on Linux / Python 3.14.7:

```bash
python -m pytest -n 12 --receptor=llm \
  tests/topology/test_get_atom_correspondences.py \
  tests/topology/test_correspondence_attribution.py \
  tests/structure/test_get_symmetry_corrected_rmsd.py \
  tests/topology/test_get_rotatable_bonds.py tests/topology/get_substructure_matches \
  tests/physchem/test_get_cip_stereochemistry.py \
  tests/interactions/test_scientific_attribution.py tests/structure/get_rmsd \
  tests/physchem/test_get_aromaticity.py tests/physchem/test_get_aromatic_rings.py \
  tests/physchem/test_normalize_aromatic_bond_orders.py tests/topology/test_get_rings.py
```

284 passed, zero failures/skips; 56 expected bundled H5MSM-0.4 deprecation warnings.
The primary guard asserts that anchored and supplied-map minima differ from the
analytic unrestricted minimum, map selection remains correct, caches preserve scope
and reject edits, and H5MSM streaming agrees under active angstrom units.
Supplemental topology tests verify pre-cap pruning, all-or-error proposals,
whole-context chemical/stereo admission and lexical witnesses independently of bond
insertion order. Attribution tests exercise the real optional provider.

Both public docstrings pass all 12 doctest examples in Python 3.14. Three full
Toolbox/Cookbook notebooks and the changed cells in course modules 13/16 execute
with the existing Python-3.14 kernel; other course cells/outputs are preserved.
The 247-function docstring validator and 156-notebook course validator pass.
`ruff check .`, `ruff format --check .` and all 14 fast release gates pass.
No new full HTML build or full multi-platform/installed qualification was run.

Dependency metadata for the Python-3.14 source run: RDKit 2025.9.5,
ArgDigest 0.15.0+1.g5c6711e, PyUnitWizard 0.28.1+3.g2ab37a5,
Ackredit 0.11.0+3.g71f7f19, pytest 9.1.1, xdist 3.8.0,
pytest-receptor 1.1.0+19.g6d87a24. The initial 92-test run used Python 3.13.14;
its results are separate from the final Python-3.14 regression evidence.

No release, frozen installed candidate, dependency floor or H5MSM format was changed.
