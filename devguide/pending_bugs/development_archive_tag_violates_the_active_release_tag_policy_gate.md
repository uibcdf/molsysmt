---
summary: Development archive tag violates the active release-tag policy gate
issue: uibcdf/molsysmt#317
status: active
opened: 2026-10-04
closed:
severity: medium
verification: reproduced
area: [ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Development archive tag violates the active release-tag policy gate

**Reported:** 2026-10-04 while checking the published chemical-typing checkpoint.
**Status:** Active. Exact-object restoration is verified; publication and maintainer review of the mistaken development-marker retirement remain.

## What

The MolSysSuite conformance run 37192267497 fails at commit
`68c924d842870536857b409aa7eabe6c368962b0` with:

```text
[RELEASE_TAG] noncanonical component release tags: archive/rust-c1-spike-20261002
```

Run: https://github.com/uibcdf/molsysmt/actions/runs/37192267497

The tag intentionally preserves development-spike evidence before temporary
branch deletion. That purpose is recorded by uibcdf/molsysmt#252. It is not a
published release or a Zenodo archive, but the active release-tag check scans
repository tags and rejects this spelling.

## How

The component introduced an archive marker in the tag namespace. Its existing
policy-v1.5.4 workflow applies the release-tag contract to that namespace.
No chemistry, source import or scientific test failed in this conformance step.
The source archive reference is `refs/tags/archive/rust-c1-spike-20261002`,
with annotated-tag object `6456293bb980e32b15b885c5b38a344af4cafd03` and
target commit `87317ba766e8d99e6b5129e25eebb83ffb089c0d`.
Its annotation says to preserve the nonproduction Rust C1 packaging experiment
before branch retirement.

## Why

The published head cannot satisfy repository conformance while this reference
violates the active policy. Silently deleting it would discard an archival
promise made when temporary development branches were removed. Disabling the
release-tag gate or treating this marker as a release would not solve that
contract conflict.

## What is measured and what is assumed

**Reproduced:** GH Run Receptor identified the failed conformance step. Its
compact report did not expose the policy message, so native `gh run view
37192267497 --log-failed` was inspected for the exact diagnostic. The local
reference/object was verified through git. These are CI and archival-reference
observations, not scientific or release qualification.
**Assumed:** A durable explicitly documented development archive outside the
release-tag namespace can preserve the spike without changing tag policy. Its
actual ref/record route must be agreed before deleting or migrating the
published tag; no destructive ref operation has been performed.

## What was refuted

This is not a chemistry regression, missing dependency, release publication,
or a need to weaken the formatter/scientific gates. The separate Ruff CI failure
was formatting debt, corrected with identical ASTs across the 24 changed files.
CI smoke, developer-guide integrity and Conda publication governance passed
on the inspected source head. Those green administrative/smoke checks do not
clear the deferred full-suite backlog.

## Scope and exclusions

Preserve the explicit development-spike evidence and bring its reference into
conformance with the adopted tag policy. No release, tag rewrite, force push,
archive deletion, policy waiver or remote branch change is authorized by this
report. Chemical typing and rotatable-bond work keep their own tracked scope.

## Acceptance criteria

- The exact spike object remains durably identifiable and reviewable.
- The archival record for uibcdf/molsysmt#252 describes the agreed replacement.
- Published references conform to the actual adopted release-tag policy.
- An exact-head MolSysSuite conformance run passes without disabling the check.

## Next action

Review the archival-reference route with the maintainer before changing the
published tag. Record any central rule/provider proposal in MolSysSuite only
if a change to shared policy is actually required. The current observation does
not show a defect in the policy implementation.

## Replacement archive — 2026-10-04

**Implemented and contract-tested:** the 6,200-byte incremental Git bundle in
`devtools/data/development_archives/rust_c1_spike_20261002.bundle` retains the
original annotated tag object and the unmerged experiment. Its adjacent JSON
manifest records SHA-256, original ref, commit and prerequisite
`cb3341fd5cd9f205b9813d60e708a61895f95918`, an ancestor of current main.
The [development archive contract](../development_archives.md) defines
preservation and inspection outside the active release namespace.

The restoration validator creates temporary bare Git storage, borrows only
prerequisite history, restores the bundle and verifies that every archive-specific
object is physically in the restored pack. The guard also rejects corrupted
payloads, wrong identities and a checksummed empty pack even when source storage
still contains the old experiment. The live #252 record points to this replacement;
the original dated integration JSON is intentionally unchanged.

The local and remote annotated-tag identities agree. `gh release view` reports
no GitHub Release for this development marker. Latest published main
`ececfba5067859d7a18d6068be40b5c494a0d3a4` passes smoke, Ruff, developer-guide
integrity and Conda governance. Policy run 37196462010 fails on the same
noncanonical marker; native failed logs confirm the diagnosis. These observations
do not qualify the full release matrix or change the separate scientific backlog.

**Remaining:** publish the replacement, obtain maintainer review of this exact
development ref, retire only that marker and require a successful conformance
run on the resulting published head. Historical release tags remain untouched.
