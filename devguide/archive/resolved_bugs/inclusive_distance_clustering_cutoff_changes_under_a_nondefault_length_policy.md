---
summary: Inclusive distance-clustering cutoff changes under a nondefault length policy
issue: uibcdf/molsysmt#659
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: high
verification: reproduced
area: [structure, units]
guard: tests/structure/test_distance_clusters_unit_policy.py
normative: devguide/SCALABILITY.md
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
Local reproduction with published PyUnitWizard 0.28.1 confirms that hypothesis:
the supplied cutoff converts directly to `1.0 nm`, while the digester's pm/fs
and angstrom/ps detours produce `0.9999999999999999 nm`. The matrix edge
remains `1.0 nm`, so both linkage methods correctly reject the now-altered cut.
This receiving does not certify the complete clustering result or the client's
separately identified provider combination.

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

## Implemented correction and directed evidence

The cutoff digester keeps a validated clustering length quantity in its supplied
units, just as the distance-matrix digester already does. The calculation then
converts both directly to its existing float64 nm comparison space. Parsing,
dimensional validation and runtime finite/scalar/nonnegative checks remain.
Returned lengths still follow the caller's output-unit policy. Other cutoff
consumers retain their existing standardization, including the public mechanical
cutoff setter. No tolerance, algorithm, provider floor or schema is added.

This corrects MolSysMT's unnecessary conversion path, not a demonstrated
PyUnitWizard defect. A caller can already have rounded a quantity before the
operation; the comparison remains exact on its directly converted canonical
values. Different earlier conversion histories are not promised bitwise parity.
Keep the original supplied matrix/cutoff with source evidence when reproducing
a boundary decision; a later unit-presentation round trip is not that input.

Private evidence under `.pytest_cache/external-reference-421/` retains:

- `cluster-659-probe-original`: clean `6c84e731d44426324de0ae06900a7f84787ab86c`
  reproduces the literal nm/ps, pm/fs and angstrom/ps chain, both methods and
  string/quantity cutoffs with published PyUnitWizard 0.28.1. It records the
  supplied/digested values above, without attributing them to the client's
  separate native binary or provider source.
- `cluster-659-baseline`: 25 failures and 48 passes on the old implementation.
  Eight exact-cutoff controls and sixteen mixed-unit policy-invariance controls
  expose altered partitions; one control exposes the intervening standardization.
- `cluster-659-directed`: 151 passes and one test-fixture error caused by using
  a nonexistent root alias for `MolecularMechanics`. The fixture now imports
  the existing class from `molsysmt.native`; no public export is added.
- `cluster-659-directed-fixed`: all 152 affected cases pass, including the 73
  new controls, original pairwise/clustering cases, quantity digesters and the
  public clustering doctest. Final clean receiving will also execute the new
  nondefault-policy doctest example.

The 73 controls independently assert the literal chain partitions and reject a
cutoff one float64 step below the edge, so a fuzzy comparison cannot satisfy
them. Mixed-input-unit cases check policy invariance of each fixed supplied
quantity, not bitwise equivalence of different caller conversion histories.
The public mechanical setter and query-flag control protect the unchanged
non-clustering branches. Inputs and active/caller policies remain unchanged;
returned cutoff/diameter quantities still use the requested presentation unit.

ArgDigest owns the boundary correction. The existing public `@arg_digest`,
`skip_digestion` and SMonitor diagnostics remain; no private helper is decorated.
PyUnitWizard performs the canonical and output conversions. No new optional
engine requires DepDigest; the existing clustering implementation retains its
Müllner method reference, detached producer versions and optional Ackredit path.
The User Guide, Cookbook and course describe the distinction. Their three
notebooks preserve every code cell, execution count and output.

The refreshed bounded component inventory finds PyUnitWizard clean/current at
`f82b618ea88c151a9b43009228126b1cf7fda65c`. Its four reported MolSysMT root
modifications are human-owned files and remain protected; our work stays in the
isolated owner worktree. The final source receiving below covers both provider routes. Public delivery
and the independent client handoff follow that evidence.

## Final clean source receiving

Clean implementation `68350e0b27249b8337c04779ba0a86196d861a18` passes all
210 affected cases with published PyUnitWizard 0.28.1 and the same 210 with
provider source `f82b618ea88c151a9b43009228126b1cf7fda65c`. These are two
provider routes over the same guards, not 420 unique assertions or client E3
acceptance. Both runs include the nondefault-policy public doctest and the
original provenance, Ackredit, diagnostics and shared-unit-policy controls.

Fourteen fast gates pass on that clean source. Five rendered API/User Guide/
course pages contain the direct-conversion distinction; HTML retains exactly
six existing warnings. Repository-wide Ruff lint and format checks pass. Every
code cell/output/execution count in the three edited notebooks is unchanged.
All 8,606 source, 2,463 Viewer-export and (for the source-provider route) 596
PyUnitWizard input hashes agree before/after receiving. Provider source remains
clean at the inspected full commit.

The [portable receiving record](../../../devtools/data/distance_clustering_unit_policy_receiving_659_20261108.json)
retains the original direct-value probe, 25 failing baseline controls, first
151-pass/one-fixture-error run, successful directed run and clean receiving.
Final scientific runs peak at 388,665,344 and 404,017,152 bytes; HTML peaks at
1,343,250,432 bytes. Every monitored attempt keeps more than 14 GB decimal host
availability with no OOM, reserve or pressure stop.

DockingMT's [independent original evidence](https://github.com/uibcdf/molsysmt/issues/659#issuecomment-6729158031)
remains a failed complete selection until its owners rerun all original normal/
nondefault controls, adverse cases and final live checks. No tolerance or client
assertion is weakened. This closes the provider defect only, leaving #256's
mechanics-persistence hold and all installed/platform/exact-candidate gates.
