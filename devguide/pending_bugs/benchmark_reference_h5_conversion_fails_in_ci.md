---
summary: Performance audit rejects its H5 reference before producing measurements.
issue: uibcdf/molsysmt#539
status: active
opened: 2026-11-03
closed:
severity: medium
verification: inspected
area: [ci, performance, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Benchmark reference preparation and runtime identity

**Reported:** performance gate of PR #538, without a local original-environment
reproduction from the reporter.
**Status:** original failure inspected; a compatible source/backend-shadow
mechanism independently reproduced. Exact hosted cause and correction remain pending.

## What and how

[Performance run 41689119788](https://github.com/uibcdf/molsysmt/actions/runs/41689119788),
job 126102695348, fails in `benchmarks/competitors/run_matrix.py` while converting
the catalogued solvated-villin MDTraj HDF5 trajectory to its reference PDB.
`validate_molecular_system_argument` raises ArgumentError for the input before
any timed benchmark executes. The raw log and compact GH Run Receptor failure
are retained under ignored `.pytest_cache/stabilization-review-next/`.

The checkout is GitHub's PR merge commit
`3260eb21ffcb03d5b4f91126bd411b010d6c7fb9`, combining PR head
3c13ba1a5c248de11622ff015b24551f72c59846 with base
d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42. The installed development wheel
is identified as `molsysmt-0.23.0+378.g3260eb21f`. The workflow's Conda inventory lists Python
3.14.10, NumPy 2.5.4, Pandas 3.1.0, MDTraj 1.11.2 and h5py 3.16.0. These are
environment-manifest observations; setup-python's separate 3.14.9 version is
not proof of the interpreter used at the failing command. The original log does
not print that command's effective interpreter, input existence, classification
reason or compiled-extension origin.

This input is MDTraj/Pande `file:h5`, not the H5MSM 0.5 schema. No new H5MSM
version follows from this failure.

## Inspected route and controlled reproduction

The performance workflow installs MolSysMT noneditably with `pip install .`.
The runner and competitor modules then explicitly put the checkout root first
on `sys.path`. A fresh checkout can consequently supply Python sources while
the compiled Rust extension is present only in the installed wheel prefix.

A paired fresh-process experiment reuses the existing real noneditable Linux
wheel prefix; no environment or package is created or replaced. Temporary
source trees contain the current Python/data paths and copied benchmark scripts,
with the source Rust binary absent or present. Only the host development
installation's MolSysMT-specific editable finder is excluded inside those
subprocesses, so it cannot accidentally supply a binary from another checkout.
All other installed dependencies and the actual wheel remain available.

With no source binary, the H5 exists and is 1,268,562 bytes, but the assessment
reports `KeyError: 'file:h5'` and public conversion raises ArgumentError. Making
the existing source binary visible changes the same input to valid `file:h5`,
and the public count returns 4,369 atoms. The paired receipt records package and
binary origins in `539-source-shadow-receipt.json` under the ignored task cache.
Temporary source trees and PDB outputs are removed automatically.

An earlier source-overlay attempt inherited the shared editable finder and
therefore did not isolate backend absence. A long conversion attempt timed out;
the shorter diagnostic showed the binary was still coming from the original
checkout. Those attempts are not accepted negative controls or evidence of a
native conversion hang. The corrected paired experiment checks the actual
binary origin before interpreting its outcome.

## What remains uncertain

This establishes a real failure mode of the inspected installation/import
combination; the original failing CI process did not record its binary location.
Its exact cause is therefore not retroactively certified. Do not conclude the
file was missing/corrupt, a third-party version was incompatible, or an H5MSM
reader needs changing from the generic exception alone.

## Next action and acceptance

Capture effective Python, MolSysMT and Rust origins, relevant provider versions,
input existence and `assess_molecular_system(h5).reason` in the failing route.
Choose one coherent benchmark runtime: an editable compiled source checkout,
consistent with the ordinary source CI, or an installed-only process that cannot
be shadowed by checkout sources. A mixed route is not an installed qualification.

Add an addressable fresh-process guard for reference preparation and verify the
same full scientific input before running the unchanged performance audit and
thresholds. No missing timings count as a successful audit. PR #538 stays
unmerged pending its applicable integration checks; this issue is independent
of #537's archive correction and Viewer #269's installed-source campaign.

## Scope

Runtime/source identity and benchmark reference preparation are in scope.
No alternative dataset, relaxed performance threshold, scientific method,
dependency floor or package publication is introduced by this investigation.
