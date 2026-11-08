---
summary: Public comparison rejects supported Boolean component_type attribute flags.
issue: uibcdf/molsysmt#646
status: active
opened: 2026-11-07
closed:
severity: medium
verification: inspected
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
