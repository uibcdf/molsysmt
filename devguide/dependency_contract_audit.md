# Dependency contract audit

This is the maintained, repository-local route for changing a runtime
dependency. The public package contract is the `dependencies` list and
`requires-python` field in `pyproject.toml`. Runtime features in selected
`project.optional-dependencies` extras remain optional. Supported constraints for
providers acquired outside pip live in that file's
`tool.molsysmt.provider-requirements` table; this table is not an installer extra.
The form adapter's hard/soft
classification is owned separately by `molsysmt/_depdigest.py`. Exact source
SHAs used while a coordinated Conda pair is staged live in the controlled
source manifest named by `devtools/dependency_contract.toml`; those SHAs do
not define public version floors.

Installation hints are acquisition metadata, independently of hard/soft status.
Ackredit remains optional and MolSysViewer remains required; both advertise
their reviewed `uibcdf` Conda route with `pypi=None`. A required provider may
use a named Conda route instead of a PyPI hint, but its plain package name
and explicit channel must be valid and its requirement must still occur in
`pyproject.toml`. The auditor rejects missing runtime requirements, malformed
routes, constraints/extras/markers embedded in a route and missing channel metadata.
This metadata does not certify a public PyPI release, installed compatibility
or a provider version. Third-party routes and local pip source/editable
installation are unchanged. MolSysSuite #167 owns shared route policy;
MolSysMT #730 owns this consumer correction.

The inventory's `runtime_extras` classifies public runtime extras by name;
currently it selects `soft`, independently of test and documentation tools.
Their names, version constraints, extras, markers and URLs are read from
pyproject.toml. An environment must match each optional provider it explicitly
provisions. `optional_required` additionally protects deliberate feature coverage
by name, including MDTraj and its parser. `conda_provider_required` protects
Conda-only capabilities, including PyTraj and both OpenFF providers in development
and test environments. Missing nonrequired optional engines are allowed; recipes
still provision only unconditional runtime requirements. Versioned Conda-only
providers join the auditor's optional requirements through the non-installer
table. Their package names and channels come from DepDigest, without a second
version registry. Unknown extras, conflicting declarations and duplicate aliases
cannot hide a missing provider.

The auditor compares markers, requested extras and direct URLs as well as version
specifiers. For example, a pip requirement disabled by a false Python marker
cannot substitute for an unconditional required OpenFF provider. A matching
static declaration still does not prove installation or availability on a lane;
the actual installed-candidate checks remain separate. Lazy-import enforcement
stays in `validate_dependencies.py`; optional coverage and bounds belong to this
auditor rather than an independently maintained OpenFF version constant.

`devtools/dependency_contract.toml` inventories the secondary surfaces. It
contains paths, name translations (for example, Python `mmcif` to Conda
`py-mmcif`), and explicit source-provided exceptions, but no second copy of
the public dependency list. Every Conda environment in `devtools/conda-envs/`
must be classified as runtime-bearing or explicitly excluded with a reason.
The two maintained recipes and all workflows consuming the controlled-source
manifest are also inventoried. Main-branch smoke, weekly, benchmark, and docs
workflows share one audited routine Viewer source SHA; exact release-candidate
gates take the candidate SHA as an input instead.

## Identifying imported MolSysMT builds

`molsysmt.__version__` labels the imported package's build. The bootstrap first
uses the generated `_version.py` inside that package, as configured in
`pyproject.toml`. If that stamp is absent, distribution metadata is eligible
only when its file inventory explicitly locates `molsysmt/__init__.py` at the
actual imported file. Missing or unrelated records produce `0+unknown`, rather
than borrowing another installation's version or guessing a release number.
An invalid local stamp also produces `0+unknown`; an import error inside a
broken generated module remains visible.

Resolution runs at package import. Scientific producers reuse the cached
`__version__`, including their detached Ackredit records. No Git process,
network request, runtime build tool or per-calculation metadata lookup is
introduced. Existing stored producer versions remain unchanged when a later
installation reads, queries, remaps or saves the result. Unknown legacy
producer metadata remains unknown.

A build version is not an authenticated source fingerprint. An editable
checkout may change after its stamp was generated. For source studies, record
the actual import origins, commit, working-tree changes and relevant file
hashes separately; retain exact artifact hashes for installed qualification.
Installing or rebuilding the reviewed source refreshes its generated stamp.
Do not rewrite historical observations to substitute the reader's version.

`tests/test_runtime_version.py` exercises the actual bootstrap in isolated
fresh processes with conflicting metadata and a forbidden subprocess launcher,
and checks cached producer attribution on the complete scientific package.
`tests/interactions/test_software_provenance.py` protects original producer
versions across persistence. The isolation stubs are bootstrap controls, not
installed-package or provider-policy qualification.

The supported build-stamp mechanism is described in
[versioningit's runtime-version documentation](https://versioningit.readthedocs.io/en/stable/runtime-version.html).
Python documents the optional file inventory and `locate_file()` in
[the distribution metadata API](https://docs.python.org/3/library/importlib.metadata.html).
The origin-matching fallback above is MolSysMT's own bootstrap policy.

## Updating a dependency

1. Decide whether it is a hard runtime requirement, a soft adapter/extra, or
   a build/test/docs-only tool. Do not infer the category from the environment
   where it happened to be installed.
2. For a hard or runtime-optional requirement, edit `pyproject.toml` first. Update
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
floor/acquisition and remaining optional-provider minima stay pending under #524.
The NumPy major-version restriction disposition is recorded below. This partial adoption does not
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

## Native NumPy ABI

NumPy retains its `>=1.26` baseline. The former `<3` ceiling is removed because
the inspected native bridge restricts runtime ABI rather than NumPy version
major. Locked Rust NumPy 0.29.0 targets ABI `0x02000000` and rejects a greater
runtime ABI; its module-layout loader accepts NumPy version majors >=2.
Existing receiving executes the real extension under NumPy 1.26.0 and 2.4.6.
It does not establish NumPy 3 compatibility. No native bridge, toolchain or exact
build/release pin is changed by this metadata correction.

MolSysMT's native-bridge and dependency maintainers own reassessment when NumPy
introduces another ABI, the native bridge changes, or a concrete compatibility
report arrives. Retain exact public artifacts and import origins, inspect the
runtime ABI/API values, execute real extension calculations and receive affected
consumers before claiming compatibility. A demonstrated incompatibility can
justify a precise new restriction under the suite's version-bound rule. The
[#524 record](pending_proposals/runtime_dependency_api_floors.md) retains the
crate identity and source/installed evidence limits.

## Optional MDTraj compatibility

The optional provider floor is MDTraj 1.11.0. Version 1.10.3 supplies the atom
`formal_charge` argument but loses charges and chain labels through topology
copies. Upstream 1.11.0 includes the metadata-preserving copy corrections and
supports Python 3.11. Native exports and public copies are guarded in
`tests/form/mdtraj_Topology/test_runtime_provider_contract.py`. MolSysMT's own
selected-subset metadata correction is separately owned by #623; a provider
floor cannot repair a consumer omission.

The optional `soft` extra and maintained development/test specifications exclude
PyParsing 3.3.3 after its MDTraj selection regression (uibcdf/molsysmt#484).
Keep the public and Conda compatibility constraints aligned; this does not add
a hard dependency or raise the supported Python minimum. Follow
uibcdf/molsysmt#486 when a corrected parser is published. The exact exclusion
already permits successors, so receiving a fixed version does not require
re-admitting the broken artifact. Qualify actual package imports before
changing the verified development baseline or claiming compatibility.

## Conda-only optional providers

The PyTraj provider is acquired through Conda-forge AmberTools. The standalone
pip project is obsolete for current Python. DepDigest owns this route with
`pypi=None`, `conda="ambertools"`, and `channel="conda-forge"`; it remains a soft
provider and is not promoted to a mandatory runtime dependency or a fabricated
PyPI alias. The development/test environments select AmberTools directly.

OpenFF Toolkit and Units also use Conda-forge acquisition. The registered routes
are `openff.toolkit` through `openff-toolkit-base` and `openff.units` through
`openff-units`, both with `pypi=None`. Their supported constraints remain in
`pyproject.toml` under `tool.molsysmt.provider-requirements`.

The table keys identify capabilities; the values identify providers and version
constraints for audit comparison. They do not claim a usable PyPI installer or
request pip installation. DepDigest's package name derives the Toolkit base
alias, so it is not repeated in the route inventory. Provider requirements must
use registered soft Conda-only capabilities, distinct distribution/package
identities and version constraints without markers, extras or direct URLs.

An environment inventory can require such a route using
`conda_provider_required = ["pytraj", "openff.toolkit", "openff.units"]`.
These are exact capability keys in the
DepDigest registry, without package versions. The auditor derives the package
and channel from that owner, keeps Conda and pip entries separate, and rejects
missing/duplicate bundles, standalone overrides, disabled-route pip requirements
and constraints that disagree with `pyproject.toml`. PyTraj has no declared
universal version floor; its AmberTools acquisition remains unversioned. A bundle
version is not interpreted as a PyTraj version. Invalid
or unknown capability declarations fail explicitly. No second package/version
mapping is maintained in the route inventory.

An explicitly provisioned Conda-only provider follows the same route even in an
environment that does not require it for coverage. A pip override in the docs
environment cannot bypass these checks. Absent nonrequired providers remain
optional. Disabled-route packages cannot reappear in any public pip extra.

This static check verifies acquisition declarations, not a resolver result,
native ABI or scientific engine behavior. A declared channel's presence does
not prove which artifact a solver chooses. Retain exact URLs/hashes, import
origins and actual engine tests for receiving. PyTraj's extension ABI differs
between bundles sharing a version label; the existing finalizer and chain-ID
checks remain necessary. Reassess the acquisition baseline with provider/build
evidence rather than assigning an AmberTools version to PyTraj.

The auditor compares declared Conda constraints; it does not infer Conda package
versions from installed Python distribution metadata. Those identities can
differ, including the received OpenFF Units minimum's Python metadata. Retain
the actual package artifact and its provider execution evidence separately.
