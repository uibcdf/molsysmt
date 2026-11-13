---
summary: H5MSM readers silently coerce malformed integer metadata
issue: uibcdf/molsysmt#745
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: medium
verification: reproduced
area: [form, data]
guard: tests/form/file_h5msm/test_integer_metadata.py
normative:
blocked_by: []
supersedes: []
---

# H5MSM readers silently coerce malformed integer metadata

**Reported:** 2026-11-13 during #256's pre-freeze reader review.
**Status:** Resolved in source; the guarded correction, documentation and bounded receiving are recorded below.

## What

Modular roots 0.5, 0.6 and 1.0 accepted a fractional structural atom count,
a fractional structure count and a boolean layer version. A two-atom,
one-structure file with `n_atoms=2.5` appeared to contain two atoms;
`n_structures=1.5` appeared to contain one structure. Numeric equality also
admitted `schema_version=True` and `1.0` as schema 1. This was malformed
metadata accepted as usable information, not observed corruption of valid files.

A second mechanism enumerated a collection's declared count before checking
the number of stored children. A safely trapped test with an int64-maximum
count proves that ordering defect without allocating the declared population.

## How

Bare `int(...)` conversions in structural, topology, chemical-state,
association and sparse-interaction readers coerced values instead of validating
their encoding. Schema comparisons used Python numeric equality. Collection
checks built expected child-name populations before checking actual membership.

The shared private HDF5 validation helper now requires a scalar signed or
unsigned integer within the supported signed-64 index range, excluding
booleans, floating-point numbers, strings and arrays. Each field retains its
own permitted minimum. Numbered collections compare declared and actual
counts before enumerating existing children. The interaction codec validates
JSON axis counts before construction or selective queries. The structural
iterator reuses the existing owning metadata validator rather than maintaining
a second contract. No public signature, dependency, scientific criterion or
stored schema version changes.

## Why

Silent truncation hides invalid input and makes metadata-only and resident
reads disagree with the file's declared meaning. Collection checks can perform
work proportional to an untrusted declaration rather than stored contents.
This belongs in the admitted pre-1.0 data-integrity work, before the stable
H5MSM decision. It does not establish that supported writers produce malformed
headers or that ordinary valid datasets are damaged.

## What is measured and what is assumed

- The initial valid probe observed 27 acceptances: three roots, three malformed
  structural attributes and three public read routes. Original source bytes
  remained unchanged.
- The first 86-case baseline contains 84 actual missing-rejection failures,
  one actual unsafe-enumeration trap and one invalid collection-test fixture.
  Correcting only that fixture exposes both enumeration failures in the
  separate two-case contract baseline. No giant allocation was executed.
- The initial correction passes those 86 tests.
- The expanded draft omitted the required interaction method, then attempted
  item assignment on MolSys's read-only analysis mapping. These are test-draft
  errors, preserved separately, not product defects. Supplying the real public
  contract yields 200 passing cases.
- The independent positive controls retain integer widths, coordinate values,
  evaluated-empty coverage and units under pm/fs application policy.
- The first wider cohort passes 1,560 cases and reveals three patch regressions:
  one omitted-topology schema rejection and two changed diagnostic messages.
  Restoring selected-layer limits and established diagnostics fixes those paths.
- The corrected wider cohort and public H5MSM doctests pass 1,566 cases with
  684 expected legacy-deprecation warnings, no omissions, native exit 0 and
  unchanged selected inputs. Its peak is approximately 0.50 GiB and host
  available memory stays above 15 GiB.
- The execution receipt records the wider affected cohort, native process
  exits, exact input hashes, selected source/runtime and resource limits.
  Estimates are not used to certify performance or candidate readiness.

## What was refuted

- Retaining coercion to support valid alternative integer widths is unnecessary:
  signed and unsigned scalar encodings inside the supported range still read.
- This does not require a new H5MSM version: represented valid values and
  encodings are unchanged.
- A raw byte copy is not a decoding or validation operation; it may preserve
  malformed bytes. The fix does not claim all file operations validate payloads.
- Metadata-only axis queries do not become whole-layer or scientific validators.

## Scope and exclusions

The correction covers integral headers in the affected modular domain codecs,
their append/iteration/metadata routes, shared chemical-state extensions and
standalone/named sparse-interaction reading. The negative unknown-atom sentinel
and existing negative chemical reference/provenance sentinels retain their
contracts. Already strict mechanics and typed-metadata validation are unchanged.

It does not redesign payload schemas, add new file-backed public queries,
authenticate index identity, change scientific observations, prove bounded
memory for arbitrary input size, qualify the complete source or installed pair,
or publish/freeze H5MSM 1.0. The #256 client/freeze decision and release pause
remain separate.

## Acceptance criteria

1. Public resident, metadata, conversion, iteration and append routes reject
   malformed structural headers; append/read failures preserve source bytes
   and conversion leaves no destination.
2. Named/standalone interactions and their existing selective-reader route
   reject malformed axis/version declarations.
3. Mismatched numbered counts reject before declared-population enumeration.
4. Valid supported encodings, coordinates, coverage and unit policies survive.
5. Affected persistence tests, executable documentation and local fast gates
   pass; the maintained contract, User Guide, Cookbook and course agree.
6. Publish the correction and archive this record with its addressable guard.

## Provenance

Measured on 2026-11-13, Linux x86_64 shared host, Python 3.14.7, one logical CPU,
1.5 GiB test-memory cap, no own swap and a 6.5 GiB host-available reserve.
The receipt identifies NumPy, h5py, Pandas and support-provider versions and
actual import origins. The existing native binary SHA-256 remains
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`.
This is a bounded source composition, not an installed release artifact.


## Resolution — 2026-11-13

Implementation commit `f9a44bf342942ed18a5319fd346c18cbabca8ec1` validates
integral metadata without coercion, checks stored collection counts before
enumeration, shares structural validation with the iterator and retains
selected-layer limits and established codec diagnostics.

The guard exercises the actual public read, conversion, append and iteration
boundaries, source-byte preservation, no failed destination publication,
standalone/named sparse metadata, the existing selective-reader path and valid
integer/unit/coverage controls. Its original rejection/enumeration baselines
fail on the previous mechanism; it does not merely assert a helper's output.

The final affected cohort and executable public docstrings pass 1,566 cases
without omissions. All 684 warnings are expected legacy deprecations. The
fifteen local fast gates, indexes and whole-repository Ruff pass. Four changed
HTML articles rebuild without warnings and their explanations/links are
received; the course's code, outputs, metadata, order, headings and anchors
remain unchanged.

The [execution receipt](../../../devtools/data/h5msm_integer_metadata_receiving_745_20261113.json)
retains failed test drafts and patch regressions, native exits, exact inputs,
provider origins, warnings and resource bounds. The
[maintained format contract](../../h5msm_format.md) owns the reader rule.
This resolves #745, not #256's stable-format/client decision or the final-pair
qualification and publication requirements.
