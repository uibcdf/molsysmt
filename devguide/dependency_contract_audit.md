# Dependency contract audit

This is the maintained, repository-local route for changing a runtime
dependency. The public package contract is the `dependencies` list and
`requires-python` field in `pyproject.toml`. The form adapter's hard/soft
classification is owned separately by `molsysmt/_depdigest.py`. Exact source
SHAs used while a coordinated Conda pair is staged live in the controlled
source manifest named by `devtools/dependency_contract.toml`; those SHAs do
not define public version floors.

`devtools/dependency_contract.toml` inventories the secondary surfaces. It
contains paths, name translations (for example, Python `mmcif` to Conda
`py-mmcif`), and explicit source-provided exceptions, but no second copy of
the public dependency list. Every Conda environment in `devtools/conda-envs/`
must be classified as runtime-bearing or explicitly excluded with a reason.
The two maintained recipes and all workflows consuming the controlled-source
manifest are also inventoried. Main-branch smoke, weekly, benchmark, and docs
workflows share one audited routine Viewer source SHA; exact release-candidate
gates take the candidate SHA as an input instead.

## Updating a dependency

1. Decide whether it is a hard runtime requirement, a soft adapter/extra, or
   a build/test/docs-only tool. Do not infer the category from the environment
   where it happened to be installed.
2. For a hard runtime requirement, edit `pyproject.toml` first. Update
   `_depdigest.py` if the form classification changes. For a changed source
   candidate, update the controlled-source manifest or the explicit Viewer
   workflow input as appropriate.
3. Run `python devtools/scripts/audit_dependency_contract.py`. Update every
   secondary recipe and environment named by its findings in the same change.
   Do not weaken the public floor merely to make the auditor pass.
4. Run the focused tests with `pytest --receptor=llm -n 12` and the fast release
   gate. Before release, build packages and inspect their actual runtime
   metadata, then validate the exact installed Conda pair. The static audit
   does not replace those artifact and compatibility checks.

The auditor is intentionally read-only. The contributor changing a dependency
coordinates the secondary files; CI and the release gate prevent forgotten
copies from silently passing. `--root PATH` supports isolated fixture tests.
Its findings name the file and the missing or conflicting contract. It rejects
unclassified environments, a second hard-coded controlled SHA in a workflow,
and a missing source route for an environment that installs with `--no-deps`.
The lightweight `ci-dependency-contract.yaml` workflow triggers on dependency
metadata, recipes, environments and workflow changes, including YAML-only
pull requests that the ordinary smoke workflow ignores. It also supports
manual dispatch on a candidate branch.

## Limits and retirement of the old broadcaster

Agreement is not compatibility. A wrong floor repeated perfectly in wheel and
Conda metadata still admits a broken installation; PyUnitWizard 0.24.0 versus
the `configure.has_active_policy()` call was one such case. Validate changed
minimum versions against the APIs they must supply, and keep clean installed
runtime tests as release evidence.

The legacy `devtools/requirements.yaml` and
`devtools/broadcast_requirements.py` were retired when this audit was adopted.
The broadcaster could not parse the current Jinja-based Conda recipe and
would overwrite hand-maintained host/build and platform choices. Its former
`devtools/requirements/` directory held one active source manifest; that file
now lives at `devtools/controlled_sources.txt`, and all active workflow
consumers use the new path. Historical archive references preserve the old
path as dated evidence, not as a current instruction.

## Receiving runtime provider floors

The first API-grounded review under uibcdf/molsysmt#524 aligns h5py >=3.11.0,
pandas >=2.2.2, NetworkX >=3.3, Matplotlib >=3.8.4 and tqdm >=4.65.0. The public
requirements remain authoritative in pyproject.toml; this paragraph records the
receiving basis, not an independent version registry. Their rationale and exact
wheel identities are retained in the
[active review](pending_proposals/runtime_dependency_api_floors.md).

Use the executable provider module to exercise HDF5 string/resizing operations,
nullable inventory mapping/Styler, graph components/rings, colormaps, progress
iterator lifecycle and a real NumPy-to-Rust distance calculation:

```bash
python -m pytest --receptor=llm devtools/tests/test_runtime_provider_apis.py
```

Running this with the normal development providers does not qualify minima.
For an intentionally isolated provider-only probe, `--confcutdir=devtools/tests`
avoids the full-package bootstrap; it does not qualify MolSysMT's complete
runtime or replace ordinary source, optional-engine or installed-pair tests.
Use exact wheel payloads, verify import origins and retain their hashes. Never
downgrade the shared prefix to simulate a minimum.

The first probes pass with Python 3.11 and exact selected providers against both
NumPy 1.26.0 and 2.4.6. Separate source receiving with pandas 3.1.0 uncovered
deprecated inplace summary-table drops; the public `info()` guard rejects all
warnings and preserves counts, columns and result representations. Public Viewer
floor/acquisition, existing sibling/optional-provider minima and the NumPy ABI
restriction review remain pending under #524. This partial adoption does not
authorize a release or certify unexecuted provider combinations.

Default `info()` output uses Pandas Styler and its Jinja2 renderer. Jinja2 is
therefore a hard runtime requirement rather than an incidental documentation
dependency. Its floor follows the renderer API required by the supported
Pandas minimum. The provider guard above renders actual HTML; the public/native
guard in `tests/basic/test_info_runtime_renderer.py` exercises MolSys, Topology
and Structures. An explicitly requested dataframe or dictionary does not
render HTML. The active #524 record retains the exact minimum-provider probes
and their limits; provider-only receiving does not qualify a complete installed
MolSysMT runtime.

## Build-backend license contract

The Setuptools requirement in `pyproject.toml` owns the source build minimum.
The current SPDX license expression and `project.license-files` use PEP 639;
MolSysMT selects `setuptools>=77.0.3`, including early license-handling fixes.
Keep the same constraint in both Conda host recipes and the five environments
that explicitly provision Setuptools. The focused
`devtools/tests/test_license_build_contract.py` guard checks these routes and
rejects a backend floor predating PEP 639 support. This is separate from the
runtime dependency audit above.

For a changed license/build boundary, inspect actual source, direct-wheel and
sdist-rebuilt-wheel payloads in the intended backend context:

```bash
python devtools/scripts/validate_license_metadata.py \
    --source path/to/reviewed/source \
    path/to/source.tar.gz path/to/direct.whl path/to/rebuilt.whl
```

The checker verifies MolSysMT's PEP 639 license fields in core metadata 2.4 or
later 2.x minors, the SPDX expression,
declared license files and their original bytes, including the bundled ProLIF
notice. It reads archive members without installing or importing package code.
Its synthetic negative controls reject substituted metadata or notices and
missing files; a file named `LICENSE` alone is insufficient.

Backend import/metadata generation is not a native build. Deliberately exercise
the selected minimum with the real Rust/versioning plugins and distinguish it
from a modern-backend build. Record artifact names/hashes and the interpreter,
backend origins and reused dependencies. An unpacked-artifact smoke is not a
clean installed-package or platform-matrix qualification. This work changes no
license choice and does not authorize rebuilding or replacing public files.

## Documentation dependencies

The optional `docs` extra supplies the theme and external extensions configured
in `docs/conf.py`. Keep it aligned with the documentation Conda environment;
`devtools/tests/test_audit_dependency_contract.py` checks the actual configured
imports against the declared providers. Build documentation in the routine
Python 3.14 environment using `python -m sphinx -b html docs <output-directory>`.
A successful build with notebook execution disabled verifies compilation, not
the scientific calculations saved in notebooks. Record warnings and distinguish
fresh builds from incremental ones; do not compare their counts as a regression
measure. Installed candidate and provider qualification remains separate.

## Temporary source-test runtime constraint

The maintained smoke/full/weekly/benchmark source workflows currently set
`pinned_packages: [mkl<2026.2]` in their Conda configuration. This constrains
MKL only when the solve otherwise installs it; it is not a public MolSysMT
runtime dependency or a requirement to install MKL on every platform. The
optional test packages and the public floors remain unchanged.

The [#402 incident record](archive/resolved_bugs/smoke_environment_selects_an_mkl_runtime_that_cannot_import_numpy.md)
retains the failing official artifact manifest, rejected OpenBLAS solve and
successful exact-source Linux recovery. Remove or revise the ceiling together
across those four workflow routes only after the replacement runtime passes
hosted import and numerical qualification with the complete dependency set.
Do not infer installed-candidate or other-platform qualification from the
single smoke recovery.

Future replacement qualification and retirement of this ceiling are tracked by
[uibcdf/molsysmt#403](https://github.com/uibcdf/molsysmt/issues/403), with the
[active acceptance plan](pending_proposals/requalify_newer_mkl_builds_and_retire_the_temporary_runtime_ceiling.md).
A replacement may be a corrected build of 2026.2.0 or a later version. Withdrawal
of a broken package alone does not qualify that replacement.

## Optional MDTraj parser compatibility

The optional `soft` extra and maintained development/test specifications exclude
PyParsing 3.3.3 after its MDTraj selection regression (uibcdf/molsysmt#484).
Keep the public and Conda compatibility constraints aligned; this does not add
a hard dependency or raise MDTraj's floor on Python 3.11. Follow
uibcdf/molsysmt#486 when a corrected parser is published. The exact exclusion
already permits successors, so receiving a fixed version does not require
re-admitting the broken artifact. Qualify actual package imports before
changing the verified development baseline or claiming compatibility.
