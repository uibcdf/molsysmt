---
summary: Public comparison rejects supported Boolean component_type attribute flags.
issue: uibcdf/molsysmt#646
status: active
opened: 2026-11-07
closed:
severity: medium
verification: reproduced
area: [basic, argdigest]
guard:
normative:
blocked_by: []
supersedes: []
---

# Component-type comparison flags

## What

DockingMT reports that `msm.compare(source, source, component_type=True,
include_none=True, output_type="dictionary")` raises MolSysMT ArgumentError
before comparison. The public comparator supports the component-type branch,
but the named digester only accepts Boolean flags for `basic.get`. This is a
component-owned digestion boundary, not an established ArgDigest defect.

## Evidence and scope

The consumer's synthetic normal/nondefault-unit reproduction and original
provider identity are recorded in uibcdf/molsysmt#646, with related receiving
under uibcdf/dockingmt#33/#49. Current source inspection confirms the caller
restriction; local runtime acceptance remains pending. This does not reopen
#616's already resolved text-storage fidelity contract.

## Intended outcome

Accept True/False comparison flags without broadening component-value setters
or masking actual invalid requests. Keep getters, native chemical assignments,
source metadata and unit-policy authority intact. Test native and H5MSM-recovered
labels/types, unequal metadata, include_none and dictionary/Boolean returns,
invalid flags/assignments, and source preservation under normal/nondefault units.
Run a failing baseline before the smallest repair, then focused serial receiving
with the shared-host resource bounds. Consumer workflow and exact-artifact
qualification remain separate.

## Failing baseline and local repair

The final unchanged-runtime baseline fails 26 cases and passes 28 controls,
all remaining failures at the reported component-type digester. An earlier
34-failure baseline also exposed an independent scalar component-ID setter
defect, now owned by #647. Comparison mismatch controls use aligned one-item
label vectors so their failure mechanism remains comparison, not that setter.
Both original results are retained.

The local repair adds only the exact basic.compare caller to Boolean acceptance.
Setter normalization still precedes that branch; no broad catch or bypass is
introduced. Existing ArgDigest/SMonitor diagnostics remain the public boundary.
There is no new API, scientific method, optional engine or dependency; DepDigest
and Ackredit need no new integration here. Prepared-source receiving passes 220 cases, including all 54 new controls, the public compare doctest and existing component editing/recovered-append tests. Thirteen expected legacy-H5MSM warnings are retained. Runtime is 30.66 seconds; cgroup peak is 315,367,424 bytes, with no swap or OOM. Clean committed-source and fast-gate acceptance remain pending.
