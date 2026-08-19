---
summary: The evidence matrix cannot show the surfaces the manuscript will lead with.
issue: uibcdf/molsysmt#190
status: open
opened: 2026-08-19
closed:
verification: measured
area: [tests, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Proposal: let the evidence matrix say "gap" about the experimental surfaces

**Raised:** 2026-08-19, during the external audit recorded in
[`../archive/assessments/external_audit_august_2026.md`](../archive/assessments/external_audit_august_2026.md),
while working out what a referee would check first.
**Status:** proposed. Nothing here questions the current contract's correctness; it
questions its scope at the moment a manuscript points readers at it.

## What

[`scientific_validation.md`](../scientific_validation.md) scopes the evidence contract to
the stable surface: *"Its domain files must classify every Stable scientific API exactly
once as `validated`, `partial`, or `gap`."* The generated matrix therefore reports

| Status | Stable APIs |
| --- | ---: |
| validated | 43 |
| gap | 0 |

which is exactly true and reads as *everything is validated*. The true reading is
*everything stable is validated*, and 43 further scientific symbols are outside the
frame by construction:

```bash
$ python -c "
import json
reg = json.load(open('devtools/data/public_api_stability.json'))['symbols']
matrix = open('devguide/scientific_evidence_matrix.md').read()
experimental = [k for k, v in reg.items()
                if v['stability'] == 'experimental'
                and k.split('.')[1] in ('build', 'physchem', 'hbonds', 'structure', 'topology')]
print(len(experimental), 'experimental scientific symbols')
print(sum(1 for k in experimental if k in matrix), 'of them appear in the matrix')"
43 experimental scientific symbols
0 of them appear in the matrix
```

They are every `build` entry point, `physchem.get_sasa` and the ProtOr and surface
family, `structure.get_secondary_structure`, `structure.get_rmsf`, all four `hbonds`
criteria, and the two sequence-alignment functions.

The proposal is to extend the evidence registry to name the experimental scientific APIs
a publication will claim, and classify each one — including as `gap`. Not to validate
them all. To make their status visible in the document a reader is sent to.

## How

The vocabulary already exists and is unused: `gap` is a defined status with zero
occurrences, and `scientific_validation.md` already states that a gap *"does not imply
that an operation lacks ordinary tests or that its implementation is incorrect"*. That
sentence was written for this situation and has nothing to describe.

Concretely:

1. Add a `claimed` scope to the evidence registry: the set of APIs a publication asserts
   results for, independent of stability classification. Every member is classified.
2. Generate a second section of the matrix for that scope, so the summary table reports
   stable and claimed separately and neither number absorbs the other.
3. Where evidence already exists but is not governed, record it and say what class it is.

The third point is most of the work, and the current state is uneven rather than absent:

- **`build.build_peptide` has real external evidence.**
  `tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py` compares 40 random
  decapeptides against LEaP for atom count, bond count, maximum bond length within
  0.0045 nm and minimum non-bonded heavy-atom distance. It is `skipif` on `tleap`, but
  `ambertools` is in `devtools/conda-envs/test_env.yaml`, so it runs in `ci-weekly.yaml`.
  This is evidence class *external* under the hierarchy and it is invisible in the matrix.
- **`physchem.get_sasa` has parity, not an oracle.**
  `tests/physchem/get_sasa/test_get_sasa_n_sphere_points.py` compares the native engine
  against MolSysMT's own MDTraj engine at `rtol=0.03`. `tests/scientific_truth/README.md`
  is explicit that external tests must construct the backend directly and *"must not call
  a MolSysMT converter to construct the oracle"*, so this does not meet the suite's own
  standard, and a 3% relative tolerance on an absolute area is loose for one.
- **`structure.get_secondary_structure` has no oracle at all.** Its tests assert the
  output shape, that the simplified codes are drawn from `{H, E, C, NA}`, and per-class
  counts. Nothing compares the assignment with DSSP or any independent implementation.

## Why

**These are the surfaces the paper will lead with.** Native structure preparation without
OpenMM or PDBFixer is the differentiating claim; `README.md` puts it first. A referee who
follows the citation to the evidence matrix finds it absent — and absent is worse than
`gap`, because `gap` is a statement and absence is a frame.

**The contract's own honesty is what makes this fixable cheaply.** The classification
that puts `build` outside the stable surface is right, and the audit found no case of the
project claiming more than it can support. The defect is that the strongest verification
artifact in the repository has nothing to say about the part a reader most wants to check.

**One of the gaps is real and worth knowing before submission.** Secondary structure is
reported per group and used in the documentation and course; no independent comparison
exists. That is a legitimate thing to publish with — stated. It is not a legitimate thing
to publish with silently.

**Making the SASA comparison meet the suite's standard is small.** Constructing an MDTraj
trajectory directly from a NumPy fixture and calling `shrake_rupley` is the pattern
`tests/scientific_truth/external/mdtraj/test_geometry.py` already uses.

## What is measured and what is assumed

Measured: the 43 experimental scientific symbols and their zero appearances in the
matrix; the scope sentence in `scientific_validation.md`; the zero `gap` entries; the
LEaP parity assertions and their `skipif`; the presence of `ambertools` in the CI test
environment and the absence of any `-m` deselection in `ci-weekly.yaml`; the SASA
tolerance and engine routing; the three secondary-structure assertions.

Assumed — *estimate*: that the manuscript will claim results for preparation, SASA and
secondary structure. That is a guess about a document that does not yet exist
([#191](https://github.com/uibcdf/molsysmt/issues/191)), and the `claimed` scope cannot
be populated until it does. What can proceed regardless is the registry mechanism and the
three evidence corrections above.

Not measured: the `hbonds` criteria and the ProtOr family were not exercised. They are
listed as members of the uncovered set, not as known gaps.

## What was refuted

*The LEaP parity suite is effectively disabled.* This was the audit's reading from the
`skipif` alone and it is wrong. `ambertools` is installed in the CI test environment and
the weekly job applies no marker deselection, so the 40-sequence parity runs there. The
`skipif` protects a developer's minimal checkout, which is what rule 6 of the suite
permits.

*Experimental means unvalidated.* It does not, and `build_peptide` is the counterexample:
external evidence exists and the classification is about contract stability, not about
correctness.

## Scope and exclusions

Covers the registry scope, the generated matrix, and the three named evidence
corrections.

Excludes any change to stability classification: promoting `build` to `stable` is a
contract decision and is explicitly not what this asks for. Excludes validating all 43
symbols; the deliverable is a classification, and `gap` is an acceptable value for most
of them. Excludes the manuscript itself, which is
[#191](https://github.com/uibcdf/molsysmt/issues/191), and the README's silence about
stability, which is [#186](https://github.com/uibcdf/molsysmt/issues/186).

## Acceptance criteria

1. `scientific_validation.md` defines a scope for claimed-but-not-stable APIs, and
   `validate_scientific_evidence.py` enforces that every member is classified.
2. The generated matrix reports stable and claimed separately, and its summary can show a
   non-zero `gap` without that being a failure.
3. `build_peptide`'s LEaP parity is recorded as external evidence.
4. The SASA comparison constructs its MDTraj oracle directly from a fixture, under a
   governed tolerance from `tolerances.json`, or is classified `gap`.
5. `structure.get_secondary_structure` is classified `gap` or acquires an independent
   oracle.

## Dependencies and risks

The risk is scope creep: a `claimed` scope invites validating everything before
submission. The mitigation is that `gap` is a passing value, and the criterion is
visibility, not coverage.

## Provenance

Measured 2026-08-19 on Linux 7.0.0-28-generic x86_64, Python 3.13.14, MolSysMT
`0.21.0+325.g7cedab74a` at repository commit `dc0e06014`.
