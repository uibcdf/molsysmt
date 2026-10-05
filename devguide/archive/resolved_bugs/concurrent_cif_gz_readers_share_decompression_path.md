---
summary: Concurrent local CIF.GZ readers share an unsafe decompression path.
issue: uibcdf/molsysmt#326
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/file_cif_gz/test_input_isolation.py
normative:
blocked_by: []
supersedes: []
---

# Concurrent compressed CIF reads share temporary files

**Reported:** 2026-10-05, during isolated consumer qualification for
uibcdf/molsysmt#298.
**Status:** Resolved with source-preservation, concurrent-read and cleanup guards.

## What

Concurrent public conversion of the same local compressed CIF can fail because
the reads create and remove the same decompressed file. A successful single read
can also overwrite and then delete an unrelated existing sibling `.cif` file.
The input directory may be an installed resource or a read-only source tree.

```bash
python -m pytest --receptor=llm tests/form/file_cif_gz/test_input_isolation.py
```

Before the fix, the finalized regression selection produces six failures and
two passes in 4.35 s. Both neighbor-preservation controls show the existing file
is deleted. Both concurrent controls fail after denied shared-directory writes.
The failure-cleanup controls demonstrate the adapter supplies no private working
directory. The two existing multi-container diagnostic controls already pass.

## How

`molsysmt/form/file_cif_gz/to_mmcif_PdbxContainers_DataContainer.py`
called `IoAdapter.readFile(item)` without `outDirPath`. The upstream adapter
chooses the input directory, or falls back to the process working directory.
Its decompressed basename is shared by independent callers. It later removes
that path without distinguishing it from a preexisting source neighbor.

Each read now owns a standard-library TemporaryDirectory and supplies it through
the existing upstream `outDirPath` argument. Parsing completes before cleanup,
and the data container remains independent of those temporary files. The context
cleans decompression, ASCII/log artifacts on normal return or failure. Parser
selection, input locator, catalog warning and first-container semantics remain
those of the current adapter. No new public argument, helper API or dependency
is required; temporary-directory ownership has no standalone molecular contract.

## Why

Independent jobs reading the same scientific source must not interfere or destroy
unrelated source files. The isolated DockingMT/PharmacophoreMT driver used manual
caller-owned decompression as a bounded workaround. It now uses the public
compressed-input conversion directly. The original dated qualification receipts
remain historical evidence and are not overwritten.

## What is measured and what is assumed

Tests use the bundled HP35 molecular fixture through public conversions. Real
parser calls run concurrently, with a barrier after decompression. Directory
write guards cover both input and working directories, including privileged
execution where chmod alone cannot enforce read-only access. Outputs must retain
596 atoms, exact atom IDs and exact nm coordinates. Existing neighboring bytes
must remain unchanged. Captured temporary directories must be distinct and
absent after completion. A failing reader creates a partial artifact before
raising; its entire directory must disappear. The actual catalog emitter is
called for a synthetic two-container input and its first container is returned.

The routine environment selects IoAdapterPy; explicit Python selection and the
installed default are tested. IoAdapterCore's same argument was inspected in
source but its compiled implementation is not installed or claimed as executed.
No timing or memory benchmark is claimed.

## What was refuted

Switching to a new CIF parser or fully materializing decompressed text in a Python
string is unnecessary. The installed dependency at the public floor already
accepts an explicit output directory. A mutex only coordinates one process and
does not protect existing neighboring files. Disabling cleanup would leave
competing stale files. A read-only input directory alone is insufficient because
the upstream adapter can fall back to a shared working directory.

## Scope and exclusions

This fixes local file:cif.gz parsing into a data container and all native routes
that delegate through that adapter. Public signatures, chemistry and numerical
units are unchanged. Parsing remains eager and temporary disk must be available.
Uncompressed CIF, remote fetching, file writers, binary CIF and general parse
error diagnostics are separate routes. No PBC or interaction inference changes.

## Acceptance criteria

The input-isolation module must pass, including concurrent read-only inputs,
preexisting sibling preservation, failure cleanup and original diagnostics.
Existing compressed/uncompressed CIF native/parity controls and the updated
adapter doctest must pass. Both real #298 consumer drivers must succeed together
on the shared compressed 1QKU source without manual decompression. User Guide,
Cookbook and common course explanations must describe the read-only behavior.

## Provenance

Linux, Python 3.14.7, NumPy 2.4.6, mmcif 1.1.1 (the declared dependency floor),
IoAdapterPy and released ArgDigest 0.13.0 source. Provider base:
`30d862564eac48c5e1cc630849266443edb562c9`, 2026-10-05.


## Resolution

**Contract-tested.** The compressed-input adapter now supplies an independent
working directory to the installed parser and removes it with standard-library
context ownership. The qualification driver no longer manually decompresses its
input. Foundations, the compressed-CIF form page, the explicit-template Cookbook
and Common Core Module 1 describe concurrent/read-only source handling and eager
parsing. Notebook edits are prose-only; executable cells and saved outputs are
unchanged.

```bash
python -m pytest --receptor=llm tests/form/file_cif_gz tests/form/file_cif \
    --doctest-modules \
    molsysmt/form/file_cif_gz/to_mmcif_PdbxContainers_DataContainer.py
```

On the Python 3.14 environment above: **27 passed in 6.32 s**, including eight
regression cases, existing native conversion/parity controls and the new public
adapter doctest. The concurrency controls additionally verify distinct temporary
directories are removed on success; failure cleanup and original warning emission
are covered separately. The regression module's public conversions and assertions
about source/sibling bytes, identities and coordinates fail with the original
adapter; supplying a path without delivering the parsed molecular data cannot
satisfy those controls.

The two full #298 drivers also pass concurrently, reading the same compressed
1QKU fixture directly. DockingMT produces the same 2,392/22 receptor/ligand PDBQT
atoms, named-charge audit and provisional receptor assessment. PharmacophoreMT
retains the same EST inventory and six hydrophobic sites. Typed histories,
original coordinates, source maps and evaluated empty interaction coverage survive
H5MSM recovery in both processes. The isolated consumer copies and their proposed
patches remain those of the previous checkpoint. No new consumer source changes
or biological acceptance are claimed.

Ruff, dependency-import checks, public docstrings and the maintained 156-notebook
course structure gate pass. The Python 3.14 Sphinx environment lacks the optional
sphinxcontrib.bibtex extension and cannot build documentation; the existing Python
3.13 documentation environment is used separately for the HTML build. This is
not an installed-package or complete Python-matrix qualification. The HTML build
passes in that documentation environment, with the existing #144 warning baseline.
Only generated cosmetic changes to three unrelated autosummary files were restored;
all intended documentation edits remain.
