---
summary: Inclusive distance-clustering cutoff changes under a nondefault length policy
issue: uibcdf/molsysmt#659
status: open
opened: 2026-11-08
closed:
severity: high
verification: asserted
area: [structure, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Inclusive clustering cutoff depends on the caller's length policy

## What

DockingMT independently reports that the same explicitly unit-bearing matrix
and cutoff produce different partitions under nm/ps and pm/fs session policies.
With distances `[[0, 1, 2], [1, 0, 1], [2, 1, 0]] nm` and cutoff `1 nm`,
complete linkage should return `[0, 0, 1]` and single linkage `[0, 0, 0]`.
Its pm/fs run instead returns three singleton clusters for both methods while
the result still declares an inclusive `<=` cutoff. See
[uibcdf/molsysmt#659](https://github.com/uibcdf/molsysmt/issues/659) and consumer
uibcdf/dockingmt#79 for the original observation and independent receiving scope.

## How

The consumer used clean editable MolSysMT
`8af8628e61ac28b519827802c39cf2e3eaa48b7e`, Python 3.14.10 and a separately
identified PyUnitWizard source. Normal-policy receiving passed; the nondefault
selection failed before its later controls and final live checks. Its recorded
producer label is not silently replaced after #657's subsequent correction.

Inspection shows the shared cutoff digester standardizes its argument before
the clustering implementation converts both the matrix and cutoff to nm.
The distance-matrix digester retains its quantity. Asymmetric unit conversion
is a plausible hypothesis, not yet a measured internal-value diagnosis.
Local reproduction remains pending; this intake does not certify either the
reported provider combination or the complete clustering result.

## Why

A session's output-unit policy must not decide membership of a geometric
cluster. This is numerical-boundary correctness and takes priority over the
#256 composition review. The defect has its own owning issue; it does not erase
the completed #604 feature implementation or substitute for independent client
acceptance.

## Intended correction and guard

Reproduce first with the original exact boundary and the published development
provider. Inspect actual canonical values at the owning digestion/calculation
boundary. Preserve the explicit inclusive comparison; do not add an implicit
fuzzy cutoff or weaken the consumer's expected partition.

Cover both linkage methods, quantity/string cutoffs, original and
caller-normalized input-unit combinations, exact and strictly separated cutoffs,
default/nondefault policies, and source/caller preservation. Reuse the general
unit tools and existing public validation/attribution paths. If a provider
limitation is independently demonstrated, report it there with consumer evidence.
Source receiving, the reported provider combination and DockingMT's own E3
qualification remain separate evidence.
