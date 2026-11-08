---
summary: Public comparison rejects supported Boolean component_type attribute flags.
issue: uibcdf/molsysmt#646
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: medium
verification: reproduced
area: [basic, argdigest]
guard: tests/basic/compare/test_compare_component_metadata.py::test_component_type_flags_preserve_equality_and_negation
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

## Resolution — 2026-11-07

Qualified source `ad67e0e915ba23d90cb9d6331c063c342852d67a` passes 220 clean-source cases with zero
skips, failures or errors, including the changed public compare doctest and
54 new public metadata controls. The same source passes all fourteen fast gates
and applicable whole-library/addon plus affected-test Ruff checks. The 13
legacy-H5MSM warnings remain expected. Final test peak is 314,970,112 bytes
under one CPU, a 2 GiB process-tree cap and zero swap; no OOM or resource stop.
No compiled kernel, dependency, graph comparison algorithm or chemical assignment
changes. The independent #647 scalar-ID setter defect remains open.

The guard checks literal labels/types, both flag values, both outputs, partial
missing metadata, genuine differences, native/H5MSM storage, unchanged table
identity/content/dtypes and normal/nondefault unit-policy authority. Reverting
the digester repair restores the reported refusal before those comparisons.
Setter Boolean labels and unsupported comparison requests still fail publicly.
The receipt is [the source receiving record](../../../devtools/data/component_comparison_receiving_646_20261107.json).
Only Markdown cells changed in the comparison tutorial/course: all code cells,
outputs, IDs and notebook metadata remain unchanged. Full notebook/HTML and
consumer workflow, installed-platform and candidate qualification are not claimed.
