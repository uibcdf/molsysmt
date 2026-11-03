---
summary: Performance audit rejects its H5 reference before producing measurements.
issue: uibcdf/molsysmt#539
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: inspected
area: [ci, performance, form]
guard: devtools/tests/test_benchmark_reference.py
normative:
blocked_by: []
supersedes: []
---

# Benchmark reference preparation and runtime identity

**Reported:** performance gate of PR #538, without a local original-environment
reproduction from the reporter.
**Status:** resolved by the compiled editable source route and successful
exact-source hosted preparation, complete measurements and threshold audit.
The original failed job's unrecorded backend origin remains unknown.

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

## Correction and local receiving — 2026-11-03

The performance workflow now installs the compiled checkout editably, matching
its scripts' explicit source imports and the ordinary source CI route. It uses
the same pinned minimal Rust 1.97.1 toolchain as source smoke. No shared local
environment is rebuilt or replaced by this work.

Reference preparation remains the same full H5-to-PDB public conversion. The
runner now records the effective executable/Python version, Python-package and
Rust origins, package/provider versions, input existence/size and molecular
classification reason before conversion. A missing backend or invalid reference
fails before timed phases. Diagnostics belong to the benchmark tooling; no
library API or scientific classifier fallback is added.

`devtools/tests/test_benchmark_reference.py` covers a fresh process under the
same QA profile, converting all 20 structures / 4,369 atoms and comparing every
output coordinate with MDTraj's H5 reader within PDB's 0.00005 nm rounding plus
0.000001 nm numerical margin. A backend-unavailable control rejects preparation
without writing the PDB. The workflow contract rejects the old noneditable
installation and requires installation, guards and timing in that order. It
also retains the 0.15 comparison threshold. The guard executes in hosted CI
before the ordinary complete benchmark command.

The workflow guard fails against the preceding installation route; the initial
three-case local receiving passes in 57.11 seconds, zero skips/failures. Final
combined receiving with the nightly/full-route, controlled-dependency,
dependency-audit and smoke-command guards passes **40 tests**, zero skips/failures,
exit 0, 68.75 seconds, using two workers. Receptor and JUnit counts agree. This
uses the existing Linux Python 3.14.7 development environment and reused compiled
backend. Full-tree Ruff lint/format, dependency contract/import checks and devguide
integrity/index checks pass. The hosted audit remains pending at this checkpoint. The original generic CI exception is preserved as historical failure;
this repair addresses a demonstrated incoherent route without inventing its
missing retrospective runtime evidence.

No baseline, input, timed workload, repetition count, threshold, public dependency
floor or scientific method is changed. Source reference preparation does not
qualify an installed package, complete benchmark run or release. Keep #539 open
until the actual hosted route produces its preparation evidence and timings.

## Published source and hosted request — 2026-11-03

Correction and guards are published in
`3920346fb4126ec28f15f5ea6edc7e944f7b2589`.
[Performance audit 41706735371](https://github.com/uibcdf/molsysmt/actions/runs/41706735371)
is manually dispatched on that exact commit. GitHub and GH Run Receptor report
it queued with no executed job steps at this snapshot. No timings, hosted
preparation success or final audit outcome are claimed. This workflow does not
upload packages or publish releases. #539 remains open pending that execution.

## Resolution and terminal hosted receiving — 2026-11-03

[Run 41706735371](https://github.com/uibcdf/molsysmt/actions/runs/41706735371),
job 126163924551, completes successfully on exact source
`3920346fb4126ec28f15f5ea6edc7e944f7b2589`. The three fresh-process/reference
controls pass in 112.53 seconds without skips. The ordinary complete benchmark
command then executes, and all **21 compared paths** conform to the unchanged
15% threshold. The original input, workloads, iteration/repetition settings and
baseline remain unchanged. GH Run Receptor reports terminal PASS, agreeing with
GitHub's job and all executed preparation/measurement/comparison steps. There
are no downloadable run artifacts; the native log carries the runtime, complete
measurement summary and comparison evidence.

The actual failing-command boundary is now observable: the runtime reports
Python 3.14.10 from the Conda executable, package and Rust origins in the same
checkout, MolSysMT `0.23.0+382.g3920346fb`, NumPy 2.5.4, Pandas 3.1.0, MDTraj
1.11.2 and h5py 3.16.0. The H5 exists, is 1,268,562 bytes, and is assessed as
valid file:h5 with no failure reason. These are runtime observations rather
than inferred setup-python versions.

The original failure remains failed, not retroactively diagnosed from absent
metadata. Controlled reproduction established the shadowing mechanism; the
corrected source route removes that incoherence and now executes the entire
unchanged gate. Hosted medians do not establish universal speed improvements,
a noise-calibrated regression protocol or later-source performance. This is
source benchmark receiving, not installed-package or release qualification.
Native raw/compact evidence is retained in ignored
`.pytest_cache/stabilization-539/corrected-hosted.raw.log` and the receptor cache.
