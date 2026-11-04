---
summary: Reference bond helpers do not consistently validate atom-index maps.
issue: uibcdf/molsysmt#554
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: reproduced
area: [argdigest, build]
guard: tests/element/group/test_reference_bond_map_validation.py
normative:
blocked_by: []
supersedes: []
---

# Reference bond input-map validation

## What and how

On source 93d29bf23e2c54f238f7ada984a4b23420b4b3b0, saccharide,
small-molecule, terminal-capping and water reference bond helpers accept an
atom_indices list of strings and return string endpoints. A six-family probe
also finds that extra explicit indices are ignored while short maps fail with
incidental KeyError/IndexError. Those inputs violate the intended parallel
integer mapping contract; this is not evidence that stored bond tables are
chemically wrong.

```python
import molsysmt as msm
msm.element.group.saccharide.get_bonded_atom_pairs(
    'NAG', ['C1', 'C2', 'C3'], atom_indices=['a', 'b', 'c'])
# [['a', 'b'], ['b', 'c']]
msm.element.group.water.get_bonded_atom_pairs(
    ['O', 'H1', 'H2'], atom_indices=[100, 10, 20, 999])
# [[100, 10], [100, 20]]; the extra index is ignored
```

## Why

The documentation-only correction #548 defines successful outputs and supported
input preconditions. It does not enforce every malformed map. #550 fixes flat
atom-name containers, not this separate argument. Native consumers and PR #543
must not create their own string-to-index coercion or silently guess alignment.
The related consumer is uibcdf/molsysviewer#264.

## Scope and acceptance

Use ArgDigest at the public native boundary and existing SMonitor catalog errors
to enforce a flat integer map aligned to the supplied names. Decide scalar
single-atom compatibility, booleans, negative and duplicate indices, empty input
and readonly/strided arrays explicitly before implementation. Preserve valid
mapping outputs, family ordering, reference data, caller ownership and the
unknown/None/empty/error distinctions for valid queries. Add rejection guards
before reference-database access and verify diagnostic fields as well as type.
Coordinate any public signature or skip_digestion change with the addon.

No optional engine is needed for these bundled reference lookups; DepDigest
remains responsible for actual optional-engine boundaries. No new dependency,
Rust kernel, competing chemical store or scientific method is proposed here.

## Provenance

2026-11-04, Linux x86_64, shared Python 3.14.7, NumPy 2.4.6. The first bounded
48-call six-family probe ran from the root checkout; the four-family string-map
probe independently ran from the isolated #548 worktree at the same source.
Their raw records are under `.pytest_cache/template-bond-contracts-548-550/`.
No runtime fix or complete input-enforcement qualification is claimed.


## Resolution — 2026-11-04

All seven public reference-bond entry points now use a scoped ArgDigest registry.
Its name-to-map dependency validates aligned inputs before reference access;
SMonitor ArgumentError identifies the invalid argument/caller and
ArgumentLengthError carries expected/actual lengths. It reuses the existing flat
name, sorted/skip and unit-detection helpers without narrowing the generic
atom_indices selection digester.

The chosen map contract is flat, unit-free, unmasked, nonnegative integers within
int64 range, with exactly one entry per supplied name. Strings, floats, booleans,
negative/out-of-range values and nested maps are rejected without coercion.
Repeated indices remain allowed: this is not a permutation or uniqueness proof.
Empty names accept None or an empty one-dimensional map. Readonly/strided signed
and unsigned integer arrays remain usable without mutation. Existing scalar
single-name amino-acid/ion routes and valid trusted skip calls are retained.

All seven public signatures are unchanged. No skip option is added to a helper
that did not already have one. Existing trusted skip routes require already
valid inputs. The three #550 families now receive flat names at their public
boundary instead of repeating their in-body normalization. Group/template data,
bond criteria, endpoint/row ordering and valid unknown/empty/layout outcomes
remain unchanged. Invalid inputs now reject before those legacy lookup outcomes.
The User Guide, recipe, Foundations, Module 03, paired contracts and manifest
explain the same behavior; three notebook payload comparisons preserve code,
outputs, IDs, metadata and counts.

### Evidence

On baseline 8b6e6d10e, the selected 28 new value/length/diagnostic cases all fail:
string endpoints are accepted in four families, maps are truncated or produce
incidental errors, and recursive digestion loses the public caller in three
cases. The guard is not satisfied merely by any exception: it requires catalog
errors, exact diagnostic fields and no reference-database reads.

A first full group run obtains 605 passes and one failure in the new expected
unsigned ATP result. That test initially used a chain expectation for the known
PG-O1G/PG-O2G star. Correcting the literal expected edges does not change runtime
or existing assertions. Intermediate evidence is retained rather than relabelled.

Final receiving and supporting checks:

| Check | Outcome and scope |
| --- | --- |
| Complete group suite with the published ArgDigest floor | 627 passed, no omissions/errors/failures, two legacy H5MSM notices; includes all 186 new guard cases and earlier #548/#550 controls |
| Existing argument/build/native-query consumers | 659 passed, no omissions/errors/failures, four legacy H5MSM notices |
| Direct CIF/BinaryCIF consumers plus the initial 165-case new guard | 197 passed, zero warnings/omissions/failures |
| Documentation and seven helper doctests | 572 passed, no omissions/errors/failures; 529 warnings: 514 Sphinx/MyST deprecations, eight legacy H5MSM, six headless plotting and one intentional attribute drop |
| Public docstring fidelity/content | All 246 functions pass |
| Public signatures and notebook payloads | Seven signatures and three notebook code/output/metadata payloads preserved |

The 659/197/572 supporting runs preceded the final unit/mask rejection guard;
the final 627-case group run includes that guard. No claim of repeated execution
of unchanged supporting suites or a full platform/installed-pair gate is made.
Fast release and Ruff results are recorded in the final receiving checkpoint.

The floor is the unmodified Conda ArgDigest 0.13.0 py_1 payload already cached
in the development installation. Its archive SHA-256 is
273ae5053d0aaa2d207ec9a2c684588fe3da539219b1d91cdea3b1f8dd265007;
the cached archive matches Conda's retained repodata SHA, all 37 Python payload
files match the archive, and import origin/version were checked separately.
This is source receiving with a public provider payload, not a new environment,
clean solver closure or an installed MolSysMT artifact. No dependency floor is
raised. Other supporting checks use the shared development providers.

Raw JUnit files are retained under `.pytest_cache/reference-map-554/`:
`baseline-junit.xml`, `focused-junit.xml`, `argdigest-floor-junit.xml`,
`final-argdigest-floor-junit.xml`, `native-build-junit.xml`, `cif-junit.xml` and
`documentation-junit.xml`. Recorded nonzero baseline exits remain failures.
A separate intermediate group JUnit is supplementary only: its original tool
wrapper did not retain the process session/exit result; the final explicit run
supplies the authoritative passing exit.

### Scope and providers

No optional scientific engine, new scientific formula, reference-table repair,
Rust build, quantity conversion, Ackredit event or competing chemical store is
introduced. DepDigest remains applicable at actual optional-engine boundaries.
The small private validators are not new public molecular capabilities. #549's
name-context study and PR #543's integration remain separate work. Signature
preservation avoids an addon calling-convention migration; the native correction
still needs receiving on that PR's eventual combined source.

Commands use `python -m pytest --receptor=llm -n 2` with the listed modules in the
isolated branch `dev/reference-map-validation-554`. The floor run prepends the
verified cached public provider's site-packages directory to PYTHONPATH; all
runs use published Pytest Receptor 1.2.1 and the existing controlled Viewer
runtime. No package is installed or shared source/provider modified. Hosted
routine CI and exact-candidate qualification are later evidence boundaries.


### Final receiving checkpoint

All fourteen fast release gates and whole-tree Ruff lint/format pass on the
final correction (4,330 formatted files). The 186-case addressable guard is
included explicitly in both the hosted native smoke invocation and its local
run_tiers.sh counterpart. No addon test module or retained donor digester is
removed. This adds the reported failure controls to routine receiving rather
than relying only on a future full-suite run.
