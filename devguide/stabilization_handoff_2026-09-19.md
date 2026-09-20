# MolSysMT stabilization handoff — 2026-09-19

This is a dated operational assessment for the MolSysMT development team. It orders
existing work; it does not replace the owning GitHub issues, change their state, or make
new release claims. Reproduce every external observation before closing an issue.

## Executive recommendation

Prioritize installability and truthful CI before broad style migration or new features:

1. resolve the coordinated MolSysMT/MolSysViewer Conda release path;
2. connect meaningful tests to pushes on `main` and repair the CI badge;
3. triage the undeclared `mmcif` runtime boundary in a clean environment;
4. repair the three public `extract` dispatch failures;
5. migrate legacy trees into Ruff incrementally as background maintenance.

The suite-wide Zenodo and DOI policy is owned by `uibcdf/molsyssuite#24`. It must govern
future publication and DOI claims, but it does not authorize a GitHub Release, Conda
promotion, Zenodo mutation or historical backfill.

## Priority map

| Order | Work | Why now | Exit evidence |
| --- | --- | --- | --- |
| 1 | `uibcdf/molsysmt#195` with `uibcdf/molsysviewer#82` | Python 3.13 is supported, but the recorded Conda pair is not yet proven installable and releasable together | exact staged pair installs on Python 3.11–3.13 and all supported platforms; versions, provenance, Rust extension and Viewer resources match |
| 2 | `uibcdf/molsysmt#185` | source changes can still suppress the smoke suite with `[skip ci]`, while the README badge targets missing `CI.yaml` | source/test pushes cannot skip smoke tests; data changes run integrity validation; real workflow badge and green scheduled signal |
| 3 | `uibcdf/molsysmt#200` | a fresh Conda environment reproduced the documented PDB-ID path without its `mmcif` runtime dependency | current clean-environment reproduction, explicit dependency/parser decision, regression covering the supported installation path |
| 4 | `uibcdf/molsysmt#210` | three declared forms expose a public operation that currently fails with an internal `TypeError` | each form returns a value or a domain error; contract-debt exceptions disappear |
| 5 | `uibcdf/molsysmt#212` | common Ruff adoption is incomplete, but the critical core gate remains active | bounded directory migrations with behavioral tests; remove the central exception only when every maintained Python tree is covered |

## 1. Coordinated distribution truth

`uibcdf/molsysmt#195` is high severity and active. Its latest durable report says all 15
MolSysMT staging artifacts were produced, while MolSysViewer staging and the exact-pair
installation matrix remained pending. That checkpoint is historical evidence and must be
remeasured against the current channels.

`uibcdf/molsysviewer#82` deliberately withholds GitHub Releases for newer tags until the
dependency channels and release gates are closed. On 2026-09-19, read-only GitHub queries
reported the latest published Releases as MolSysMT 0.12.0 and MolSysViewer 0.7.0; this
does not prove which Conda artifacts currently exist.

Recommended sequence:

1. inventory exact candidate tags, channel labels and package coordinates without
   publishing;
2. rerun the resolver and clean installed-pair matrix for Python 3.11, 3.12 and 3.13;
3. classify every blocked cell as code, packaging, external runner or missing evidence;
4. obtain explicit release authority before promotion or GitHub Release publication;
5. apply the central Zenodo policy after publication and verify public records
   independently from GitHub and Anaconda.

Stop if the candidate identities or dependency versions are not frozen. Never repair the
cycle by publishing one repository on behalf of the other.

## 2. Continuous-integration truth

`uibcdf/molsysmt#185` remains visibly reproducible in the current checkout:

- `AGENTS.md` requires `[skip ci]` unless explicitly instructed otherwise;
- `.github/workflows/ci-smoke.yaml` suppresses its job when that marker is present;
- `README.md` still links `actions/workflows/CI.yaml`, which does not exist.

The fix should preserve bounded runner cost while making source verification opt-out
impossible. A documentation-only commit may remain skippable; a change under `molsysmt/`
or `tests/` must run at least the smoke suite, and a change under `molsysmt/data/` must run
the data-integrity gate. Add a test that resolves every workflow named by a README badge.

Do not close the issue merely because the MolSysSuite Ruff policy workflow is green: that
workflow owns common formatting and linting, not MolSysMT scientific or functional tests.

## 3. Clean-install PDB conversion

`uibcdf/molsysmt#200` reports that both MolSysViewer's README entry path and MolSysMT's
documented PDB-ID conversion fail in a fresh Python 3.13 Conda environment because the
RCSB `mmcif` API is used but undeclared. Development and test environments concealed the
omission by installing `py-mmcif` independently.

The durable analysis is now
[`pending_bugs/clean_conda_install_omits_mmcif_runtime_dependency.md`](pending_bugs/clean_conda_install_omits_mmcif_runtime_dependency.md).
Source history refuted the hypothesis that MolSysMT had incorporated a replacement
parser. The selected resolution is to restore `mmcif` as a hard dependency, consume its
portable public adapter instead of requiring `IoAdapterCore`, and publish a functionally
tested noarch Conda provider. Provider-side Windows and packaging work was resolved by
`uibcdf/py-mmcif#1`; `uibcdf/noarch::py-mmcif-1.1.1-py_0` is independently visible and
passed a clean Python 3.14 CIF/BCIF installation probe.

Do not close `uibcdf/molsysmt#200` until a clean installation exercises both a CIF/BCIF
conversion and the coordinated MolSysMT–MolSysViewer staging matrix. Do not substitute
`mmcif_pdbx`: its namespace, API, and BCIF coverage are not compatible with the current
adapter contract.

## 4. Public form-dispatch defect

`uibcdf/molsysmt#210` is a bounded medium-severity bug. The public dispatcher passes
atom- and structure-index arguments to three forms whose `extract` signatures cannot
accept them. The decision is semantic, not a rename:

- the two molecular-mechanics forms may need a domain-level unsupported-operation error;
- the amino-acid sequence form is indexed by groups and must not silently ignore an atom
  selection.

Start with failing tests for all three forms. The accepted behavior may be a value or a
MolSysMT domain error naming the form, never the current internal `TypeError`. Remove the
three entries from `EXTRACT_CONTRACT_DEBT` only after the dispatcher contract passes.

## 5. Ruff migration as bounded background work

`uibcdf/molsysmt#212` owns the temporary policy exception. The 2026-09-12 measurement
reported 13,500 shared-baseline findings in the core. A repository-wide rewrite would be
difficult to review and could disturb registration imports or generated adapters.

Migrate one owned directory per change. Keep formatting-only commits separate, inspect
import removals and ordering for side effects, and run the scientific tests for that
slice. This work should not displace the installability and CI defects above. The existing
critical `F821`, `F822`, `F823`, `B006`, `B023` core gate remains the safety floor.

## Suggested first working session

1. Update the durable report for `#195` with current tags, channel coordinates and the
   exact remaining matrix cells.
2. Cross-link the release decision in MolSysViewer `#82` without duplicating analysis.
3. Perform only read-only resolver and package-inventory checks.
4. If the pair is already installable, run the complete installed-pair matrix and close
   stale claims with evidence. If not, isolate the first failing cell and repair that
   dependency boundary before touching releases.

## Reproduction commands for this assessment

```bash
gh issue view 195 --repo uibcdf/molsysmt
gh issue view 82 --repo uibcdf/molsysviewer
gh issue view 185 --repo uibcdf/molsysmt
gh issue view 200 --repo uibcdf/molsysmt
gh issue view 210 --repo uibcdf/molsysmt
gh issue view 212 --repo uibcdf/molsysmt
gh release list --repo uibcdf/molsysmt --limit 5
gh release list --repo uibcdf/molsysviewer --limit 5
```

External package and workflow state changes over time. Record the date, exact package
coordinates, interpreter, channels and run IDs whenever this assessment is refreshed.
