---
summary: Clean package installations omit the mmCIF runtime dependency.
issue: uibcdf/molsysmt#200
status: resolved
opened: 2026-09-02
closed: 2026-10-02
severity: high
verification: reproduced
area: [deps, packaging, form]
guard: tests/test_distribution_manifests.py
normative:
blocked_by: []
supersedes: []
---

# Clean package installations omit the mmCIF runtime dependency

**Reported:** 2026-09-02, while exercising the staged MolSysMT 0.22.0 candidate
through MolSysViewer in a clean Conda environment.
**Status (2026-10-02):** Resolved. Runtime declarations, the portable parser,
and the clean public pair are corrected. The original remote-ID conversion
`msm.convert("1BRS", selection='molecule_type=="protein"')` was repeated
successfully from a pre-existing clean Conda prefix containing public
MolSysMT 0.22.4 build 3 and py-mmcif 1.1.1, without importing this checkout.
It returned a MolSys with 4,638 selected atoms.

## Updated package boundary — 2026-09-24

The old statement below that the coordinated installation awaited MolSysMT
build 3 is historical: build 5 of 0.22.0 passed the 15-cell exact-pair
staging matrix (`35967239820`). The later 0.22.3/0.23.3 technical pair passed
20/20 installed cells on the five native platforms and Python 3.11–3.14,
including bundled BCIF conversion, the staged package provenance guard, and
MolSysViewer resources. See [`python_3_14_checkpoint.md`](../../python_3_14_checkpoint.md).
The original missing-`mmcif` path is therefore guarded in staging, but this
does not prove a public-channel MolSysMT release or close this issue yet.

## What

The documented conversion from a PDB identifier fails after installing MolSysMT from
its package channels because no installed distribution provides the imported `mmcif`
module:

```python
import molsysmt as msm

msm.convert("1BRS", selection='molecule_type=="protein"')
```

The conversion exhausts its BCIF and CIF routes with `ModuleNotFoundError: No module
named 'mmcif'`. The same path is reached by `molsysviewer.new_view("1TRS")`.

## How

The CIF converters import `mmcif.io.IoAdapterCore` and the BCIF converters import
`mmcif.io.BinaryCifReader`, but `pyproject.toml`, the production environment, and the
Conda recipe do not declare a distribution that provides them. Development and test
environments still install `py-mmcif`, which masks the omission locally.

Before correction, the provider package on the `uibcdf` channel additionally lacked
Windows and two of the Unix platform artefacts used by the MolSysMT release matrix.
Provider-side portable packaging was resolved by `uibcdf/py-mmcif#1`.

## Why

PDB-identifier conversion is a documented entry point and is also the ordinary route
used by MolSysViewer. A package that imports successfully but cannot execute this route
does not satisfy the MolSysMT runtime contract. The defect blocks coordinated clean
installation evidence for MolSysMT and MolSysViewer.

## What is measured and what is assumed

**Measured:** the staged MolSysMT 0.22.0 package failed in a fresh Python 3.13 Conda
environment with the missing-module error recorded in `uibcdf/molsysmt#200`.

**Inspected:** current CIF and BCIF adapters still import the upstream `mmcif` API; no
equivalent parser was incorporated into MolSysMT when the package declaration was
removed.

**Measured:** the pure-Python `IoAdapterPy` and `BinaryCifReader` in py-mmcif 1.1.1 read
the bundled `1bna.cif` and `1bna.bcif.gz` without loading the native extension, yielding
the `1BNA` block with 55 categories in both cases.

**Measured:** commit `cdb9fb93` of the UIBCDF py-mmcif fork produced both
`mmcif-1.1.1-py3-none-any.whl` and `py-mmcif-1.1.1-py_0.tar.bz2`. The Conda package
test installed the noarch artefact with Python 3.14.7 and passed the CIF and BCIF probe.

**Measured:** MolSysMT converted the bundled HP35 CIF and BCIF inputs to
`molsysmt.MolSys` in an isolated environment containing the pure-Python wheel and no
native mmCIF extension. The targeted form and dependency suite passed 724 tests with 12
workers.

**Measured:** `uibcdf/py-mmcif` run `35495992796` built one noarch candidate at commit
`68c02b02` and installed that exact artifact through the Conda solver on `linux-64`,
`linux-aarch64`, `osx-64`, `osx-arm64`, and `win-64`, with Python 3.11, 3.12, 3.13,
and 3.14. All 20 functional cells read CIF and BCIF inputs successfully; the workflow
completed successfully and its publication job was deliberately skipped.

**Measured during matrix hardening:** run `35494912467` exposed that installing a local
package archive directly does not solve its runtime dependencies. Run `35495276656`
verified four platforms but exposed a Windows local-file channel URI crash. Run `35495555035`
then proved that the solver installed `requests`, `msgpack-python`, and the candidate on
Windows, but exposed a real parser defect: `IoAdapterPy` interpreted an absolute drive
path as a URL. The final run therefore guards both packaging metadata and the consumer's
actual absolute-path use case instead of weakening the probe to a relative path.

**Measured:** publication run `35496771848` rebuilt the candidate from py-mmcif commit
`bc17dc2b`, passed the same 20-cell matrix, and completed its upload job. An independent
channel query then observed `uibcdf/noarch::py-mmcif-1.1.1-py_0` with SHA-256
`dff089e19d9d6282e94dce5f7ef64717b04a44fd83a3a7b46d1d94b2d318d933` and the declared
`requests`, `msgpack-python`, and Python runtime requirements. A fresh environment
resolved that public package with Python 3.14.7 and passed the CIF and BCIF probe.

**Measured on 2026-09-22:** the MolSysMT distribution-manifest guard still failed
because it compared the PyPI distribution name `mmcif` with the Conda distribution
name `py-mmcif` literally. The guard now translates that one known provider name
before comparing constraints, and a mutation test proves that removing
`py-mmcif` from the recipe is still detected. All seven manifest tests passed
locally on Python 3.13 and the focused Python 3.14 pair probe passed the same
guard. This repairs the guard, not the still-pending corrective staging build.

## What was refuted

- MolSysMT did not absorb the needed parser implementation. An earlier local
  `CIFFileHandler` was narrower and was later removed.
- `mmcif_pdbx` is not a drop-in replacement: it exposes a different namespace and API
  and does not provide `BinaryCifReader`.
- Porting the C++ extension to MSVC is not required for initial functional Windows
  support because upstream already provides CIF and BCIF readers in Python.
- Passing artifact builds did not establish this capability: the staging build used
  `--no-test`, and recipe checks did not execute a CIF or BCIF conversion.

## Scope and exclusions

This work covers correct runtime declaration, use of py-mmcif's portable public adapter,
functional clean-install tests, and provider artefacts for the supported MolSysMT
platforms. It does not promise performance parity between the native and pure-Python
parsers, nor does it include an MSVC port of the optional C++ acceleration.

## Acceptance criteria

- Every supported installation route declares a distribution that provides `mmcif`.
- MolSysMT does not require `IoAdapterCore` when the supported pure-Python adapter is
  available.
- Provider tests read representative CIF and BCIF inputs without the native extension.
- Clean MolSysMT package tests exercise conversion through the declared dependency.
- The coordinated staging matrix resolves and passes on every advertised platform and
  Python version before release promotion.
- That matrix performs an offline conversion of the bundled HP35 BCIF file and verifies
  its 596 atoms; package presence alone is not sufficient evidence.

## Dependencies and risks

Pure-Python parsing may be slower than the native adapter, so performance is measured
separately and must not be conflated with functional correctness.

## Provenance

- Initial clean-environment reproduction: Python 3.13.15, staged MolSysMT 0.22.0,
  reported 2026-09-02 in `uibcdf/molsysmt#200`.
- Source and fallback probe: py-mmcif upstream 1.1.1 merged into the UIBCDF fork,
  Python 3.13, Linux x86-64, 2026-09-20.
- Portable package build and MolSysMT integration: py-mmcif `cdb9fb93`, Python 3.13.14
  and Conda test Python 3.14.7, Linux x86-64, 2026-09-20.
- Hosted portable matrix: py-mmcif `68c02b02`, run `35495992796`, five Conda
  platforms and Python 3.11--3.14, 2026-09-20.
- Public provider package: py-mmcif `bc17dc2b`, publication run `35496771848`,
  `uibcdf/noarch::py-mmcif-1.1.1-py_0`, independently installed with Python 3.14.7,
  2026-09-20.


## Closure — 2026-10-02

The clean public PDB-ID reproduction used Linux x86-64, Python 3.14.7,
`uibcdf/linux-64::molsysmt-0.22.4-pyabi3h03bb3b7_3.conda`, and
`mmcif` imported from that same environment. This is one fresh Linux
request, not a new remote-download matrix on every platform. The existing
20-cell public matrix independently covers bundled BCIF and PDB-text routes.

The addressable guard `tests/test_distribution_manifests.py` verifies
actual Python and Conda runtime declarations and deliberately removes
py-mmcif from a recipe to prove that the omission is detected. The installed
pair validator separately executes real BCIF conversion and rejects missing
provider dependencies. The original defect cannot be hidden by adding mmcif
only to a development environment.
