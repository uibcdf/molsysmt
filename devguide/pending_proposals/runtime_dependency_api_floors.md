---
summary: Ground runtime dependency floors and restrictions in consumed APIs.
issue: uibcdf/molsysmt#524
status: partial
opened: 2026-11-03
closed:
verification: measured
area: [deps, packaging]
guard: devtools/tests/test_runtime_provider_apis.py
normative: devguide/dependency_contract_audit.md
blocked_by: []
supersedes: []
---

# Reviewing runtime provider contracts

**Reported:** central adoption request under uibcdf/molsyssuite#137.
**Status:** partial; numerical, rendering and support-provider floors have actual
source API/ABI receiving. Pandas 3.1 summary and native-placement compatibility
are repaired. Viewer acquisition, optional-provider/restriction review and clean
installed closure remain open; no MolSysMT candidate artifact is qualified here.

## What

### ArgDigest bypass contract and Biopython route — 2026-11-04

Consumer receiving under [#549](../pending_bugs/reconcile_legacy_amino_acid_name_mappings_with_native_protonation_labels.md)
exposes a limitation missed by the earlier focal API probes: public ArgDigest
0.13.0 allows a truthy non-boolean `skip_digestion` to bypass its own validator.
The existing sequence-identity invalid-flag guard fails unchanged. This is the
already resolved upstream [ArgDigest #17](https://github.com/uibcdf/argdigest/issues/17),
fixed in acbead8. The first local release tag containing that fix is 0.14.0.
No new provider defect or duplicated host bypass implementation is introduced.

The public Anaconda release endpoint independently confirms
`noarch/argdigest-0.14.0-py_0.tar.bz2` under `main`, SHA-256
`983dca0f6bd0944d81fb1efc01e1dfa5c951e95abac6e7a0a08a13b7370d3b9e`.
The cached archive digest and all 37 imported Python payload files match.
ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and optional Ackredit 0.9.0
together pass 363 consumer cases in the existing Python 3.14.7 environment,
including invalid bypass flags at seven public boundaries. No environment is
created and no shared package is replaced.

The minimum is therefore `argdigest>=0.14.0`, aligned across pyproject.toml,
both Conda recipes and the three explicitly declaring runtime environments.
Other runtime minima and optionality are unchanged. The installed-closure
negative fixture now deliberately places a synthetic transitive floor above
the new direct minimum; it still tests the stricter transitive rejection.
The dependency-contract audit passes. Central graph/source adoption follows the
batched publication checkpoint; this local change does not qualify a package.

The same review corrects host metadata for Biopython: its import key remains
`Bio`, while both installer names are explicitly `biopython`. The old absent-
provider diagnostic incorrectly proposed `conda install ... Bio`. Real DepDigest
absence checks now retain the host catalog error and the correct command.
Alignment and identity guard only the selected Biopython engine. The receiving
guard is `tests/topology/get_sequence_identity/test_naming_schemes.py`.

One attempted minimum-provider run exits before pytest collection: the current
editable SMonitor distribution registers a new pytest bridge absent from the
0.16.0 package, mixing its plugin source with the old core. The explicit floor
probe disables only that incompatible newer entry point with `-p no:smonitor`;
Pytest Receptor, xdist and all scientific/assertion selections stay enabled.
Normal development receiving keeps the current bridge enabled. This is a
bounded mixed-environment harness limitation, not a SMonitor 0.16 runtime bug or
an exemption for hosted/installed qualification. Actual versions/import origins,
JUnit and verified archive evidence remain in the #549 working evidence.

An additional health check of the unchanged shared development environment
exits one. `pip check` reports missing pdb2pqr for packmol-memgen/proprep,
NumPy <2 constraints from ndfes/fetkutils/edgembar and proprep, and proprep's
Biopython <1.86 constraint against installed NumPy 2.4.6 and Biopython 1.88.
Those distributions and constraints are not changed by this work. The passed
source/provider tests do not qualify the whole workspace's installed closure.
Keep this observation in the remaining optional-provider/environment review;
do not downgrade shared scientific dependencies or remove user-installed extras
as an incidental naming fix. No environment repair is performed here.

### Initial review basis

At review basis 77fb24c0d779984ed65bc95176a9581cf8d07c42, six required runtime
providers have no lower bound; NumPy has an existing bounded range. Optional
runtime providers also need an API-grounded review. Installed versions and
exact controlled-source pins do not establish public minima.

## How

Inspect real provider calls, consult primary versioned documentation/source,
and exercise selected APIs with exact wheels unpacked only into ignored cache
directories. Preserve the shared development environment and existing source
candidate identities. Align reviewed declarations through the existing
dependency-contract audit. These tests do not establish a clean installed pair,
every optional engine, every supported interpreter or every provider version.

## First core receiving

| Provider | Consumed boundary and proposed disposition |
| --- | --- |
| NumPy | Keep the existing 1.26 baseline, which supports Python 3.12; exercise its array operations and the bundled native bridge. Review the existing `<3` against the actual rust-numpy ABI guard, rather than a guessed future incompatibility. |
| h5py | String dtypes, `Dataset.asstr`, slicing/resizing and H5MSM persistence. Selected >=3.11.0 includes upstream NumPy 2 compatibility. |
| pandas | Nullable typed columns, `DataFrame.map`, `Styler.hide`, selection and extraction. Selected >=2.2.2 is upstream's first generally NumPy-2-compatible release. Receive the independently reported 3.1.0 context separately, without adding an unsupported cap. |
| NetworkX | Graph, components, bridges, biconnected components and minimum cycle basis. Selected >=3.3 includes NumPy 2 cleanup and supports Python 3.11. |
| Matplotlib | Colormap registry, CenteredNorm, TwoSlopeNorm and RGB/hex mapping. Selected >=3.8.4 contains upstream's NumPy 2 wheel-build change. |
| tqdm | Standard/auto iterators and the OpenMM progress reporter. Selected >=4.65.0 is the release declaring Python 3.11 support; iteration, updates and closing are exercised. |
| MolSysViewer | Ordinary conversion and redesigned bound tools have different requirements. Public tag 0.24.0, source 1a4c97a58b68b69f3a836546c9e4ac6187c3efa2, has AddonSpec but lacks the `MolSysView.closed` lifecycle property required by `get_addon`. A source pin is not a published version floor. Coordinate the redesigned host requirement before changing package metadata. |

Primary sources:

- [NumPy 1.26 release](https://numpy.org/doc/1.26/release/1.26.0-notes.html).
- [h5py 3.11 release](https://docs.h5py.org/en/3.11.0/whatsnew/3.11.html).
- [pandas 2.2.2 release](https://pandas.pydata.org/docs/whatsnew/v2.2.2.html).
- [NetworkX 3.3 release](https://networkx.org/documentation/stable/release/release_3.3.html).
- [Matplotlib 3.8.4 source history](https://matplotlib.org/3.8.4/users/github_stats.html), PR #27993.
- [tqdm 4.65.0 release](https://tqdm.github.io/releases/#v4650-2023-03-03).

## What is measured and what is assumed

The [receiving receipt](../../devtools/data/runtime_provider_floor_receiving_524_20261103.json)
retains exact wheel filenames/SHA-256, checked import origins, source inputs,
commands, successful runs and failed/limited controls. The five selected floors
are aligned in pyproject.toml, both Conda recipes and all four runtime-bearing
environments. No optional dependency is made mandatory.

Using an existing Python 3.11.16 interpreter, the six provider tests pass with
exact NumPy 1.26.0, pandas 2.2.2, h5py 3.11.0, Matplotlib 3.8.4, NetworkX 3.3
and tqdm 4.65.0. They pass again with the same providers and NumPy 2.4.6.
The bundled unchanged Rust extension processes arrays in both runs. Test times
are 24.71 and 48.32 seconds, respectively, with zero omissions/warnings. These
are API/ABI probes, not complete minimum-environment MolSysMT qualification.

The first attempt to run the provider-only module reached the repository-wide
bootstrap and exited 3 because that existing interpreter has no PyUnitWizard.
It is not a passing run. The standalone probes use `--confcutdir=devtools/tests`
to avoid the unrelated full-package bootstrap. They still execute all six
assertion-based provider tests and the real extension in a subprocess. Ordinary
source receiving retains the normal conftest and all selected tests.

With Python 3.14.7, exact unpacked pandas 3.1.0, NetworkX 3.3 and tqdm 4.65.0:

```bash
python -m pytest --receptor=llm -n 2 tests/native tests/chemical_states tests/interactions/test_aromatic_reference_selections.py tests/form/file_h5msm/test_public_h5msm_v05.py
```

The repaired receiving adds `tests/basic/test_info_pandas_compatibility.py` and
`devtools/tests/test_runtime_provider_apis.py` to that same invocation. The
strict summary guard subsequently gains three nonzero-population cases, which
are received separately in its final nine-case run and the default 31-case run;
the earlier 1,886-case run does not include those three later additions.

- Initial receiving: 1,874 passed, zero omissions/failures, 112.53 seconds;
  615 warnings include 597 production `info()` inplace-drop deprecations.
- A first new test filtered only FutureWarning, incorrectly allowing 120
  Pandas4Warning instances. Strengthening it to reject every warning makes all
  six original cases fail. That is the reproduced regression control.
- `info()` now builds the same zero/absent population-column list and performs
  one returned `drop`, avoiding deprecated inplace calls and repeated drops.
- Receiving after the repair: 1,886 passed, zero omissions/failures,
  118.25 seconds. Of 37 warnings, 17 are a pre-existing test fixture's own
  inplace drop, two are tqdm 4.65.0 datetime deprecations on Python 3.14,
  and the remaining 18 are legacy/intentional molecular fixture warnings.
- The final strict summary guard has nine passing cases with no warnings:
  MolSys/Structures, three result representations, zero-column omission and
  preservation of a declared nonzero water population. The default shared
  pandas 2.3.3 environment passes 31 provider/route/summary tests with no warnings.

The public summary format and selection semantics do not change. The guard is
`tests/basic/test_info_pandas_compatibility.py`. No warning is suppressed.
All 14 fast release gates, the dependency-route auditor, developer-guide/index
checks and whole-tree Ruff lint/format (4,318 files) pass. The four unrelated
pre-existing autosummary edits and the shared compiled backend are unchanged.

The existing NumPy `<3` is unchanged in this first batch. The locked
rust-numpy 0.29 source targets ABI 0x02000000 and explicitly rejects a greater
runtime ABI. That is a concrete native boundary, but no NumPy 3 artifact has
been tested and a version-major bound is not identical to an ABI bound. Finish
its disposition under #524 rather than treating future incompatibility as proven.

## Additional newer-provider observations — 2026-11-04

The failed full-source run 41755216514 on exact metadata candidate 4ea80278f
retains separate future-Pandas work: the Linux/Python 3.14 log reports 162
Pandas4Warning instances from `_native_placers.py` inplace `sort_values` and
138 from its inplace `reset_index`. Another 137 are from an existing conversion
test fixture's inplace `drop`. They are deprecations, not the two failing donor
guard assertions owned by #552. Keep their removal in this provider review;
do not suppress them or infer a new version ceiling. These counts belong to
this one full-suite log, not every platform or the earlier summary-only repair.

## What was refuted

Unbounded requirements do not guarantee the required APIs. Repeating the
currently installed versions would neither identify a useful minimum nor
explain the existing NumPy restriction. Public Viewer 0.24.0 is not sufficient
for the redesigned addon merely because it supplies AddonSpec. None of these
observations authorizes a public sibling release or changing its source.

## Default styled-output closure — 2026-11-06

The default public and native `info()` paths return Pandas Styler. Rendering
that result requires Jinja2, which was available incidentally in the development
environment but missing from the public runtime declaration. The supported
Pandas 2.2.2 provider explicitly requires Jinja2 3.1.2 for this optional Pandas
feature. MolSysMT makes that feature its default, so Jinja2 >=3.1.2 is now a
hard requirement in pyproject.toml and the runtime classification, both recipes
and all four maintained runtime-bearing environments. The public output and
selection semantics remain unchanged.

The original declaration guard fails while the existing renderer succeeds,
exposing the hidden dependency rather than mistaking an extra-rich environment
for a closed runtime contract. Corrected receiving passes 35 provider, route,
public/native rendering and strict-summary cases using the exact public Jinja2
3.1.2 wheel. Seven isolated provider probes also pass with the existing Python
3.11 interpreter and the selected minimum NumPy, Pandas, h5py, Matplotlib,
NetworkX and tqdm wheels. These execute actual HTML and a real NumPy-to-Rust
distance call; they do not import and qualify the whole MolSysMT installation.

No environment was created, installed over or downgraded. Source receiving,
minimum API probes and a future clean installed-candidate qualification remain
distinct. The remaining Viewer acquisition/floor, sibling/optional-provider and
NumPy restriction reviews below still prevent closing #524.

Source `44fd0acf0788f1c9d06fe2a3a7446ad52c9e2550` contains this renderer
correction. Combined receiving with #620 passes 4,592 cases and the affected
documentation/public-doctest profile 599. These scopes overlap the directed
profiles above. The [renderer receipt](../../devtools/data/runtime_renderer_receiving_524_20261106.json)
retains the exact wheel, import origins, source hashes, native exits, commands
and limits. No clean installed-candidate or Viewer floor is claimed. The last
observed Viewer GitHub Release remains 0.24.0; an actual compatible public
artifact is still required before setting a new host minimum.

Public checkpoint `8d466268c` independently matches all 43 checked precision,
renderer and tracking blobs. The [delivery receipt](../../devtools/data/precision_renderer_delivery_620_20261106.json)
records that verification and #620 closure. This delivers the renderer subset;
it does not close this review or qualify the future installed pair.

## Native placement and newer Pandas — 2026-11-06

The recorded `_native_placers.py` deprecations still reproduce on current main
with exact unpacked Pandas 3.1.0. Six new public guards fail on `Pandas4Warning`
when restoring hydrogens/heavy atoms or adding cappings, using both MolSys and
MolSysDict inputs with two structures. All warnings are errors; filtering only
FutureWarning would miss this provider's deprecation category.

The build helper repeats endpoint normalization and ordering immediately before
the existing ChemicalStates setter performs the same work. Remove that duplicate
private helper and let the established chemical owner normalize typed storage.
The replacement guards check expected groups/counts, canonical bond pairs and
nullable dtypes, retained old bonds and coordinates, both structures, result form
and input independence. This changes no placement formula, public signature,
supported chemistry or source/provider floor. Original private-helper tests are
superseded by the public pipeline controls and existing chemical-owner tests.

The first test-authoring attempt also exposes a fixture error: MolSysDict 0.2
correctly rejects the builder's experimental mechanics domain. The fixture now
omits that domain explicitly before transport; this does not change production
persistence or discard user data. The corrected original receiving has six
failures from the one reproduced Pandas deprecation, not six independent bugs.

Corrected combined receiving passes 965 native-placement, chemical-storage,
periodic and vector cases on exact Pandas 3.1.0, without failures or omissions.
Production placement no longer emits the deprecated sort/reset warnings. Two
Pandas4Warning instances remain in an existing test fixture's own `drop` call;
the other 120 warnings are retained molecular/legacy-format diagnostics. The six
new public controls reject every warning and pass. Their first post-repair run
also exposed an invalid test lookup of nonexistent `MolSys.n_atoms`; it now uses
the supported native `get(n_atoms=True)`. No public attribute is added for a test.

That broader receiving independently discovers #621: a fixed-state H consumer
retains the MIC helper's pre-phase-two signature. Its dedicated owner record and
regression distinguish this correction from the Pandas compatibility repair.

## Support-provider floor receiving — 2026-11-06

Independent Anaconda release queries confirm the selected exact noarch builds
under `main`: PyUnitWizard 0.28.1 build py_0, mmCIF 1.1.1 build py_0, ArgDigest
0.14.0 build py_0, DepDigest 0.15.1 build py_0 and SMonitor 0.16.0 build py_1.
Archive SHA-256 and every imported Python payload match the existing cache.
PyUnitWizard's cache had a historical staging URL; the public main endpoint now
independently supplies the same artifact identity. No provider is installed or
replaced in the shared development environment.

| Provider floor received | Actual consumed boundary and receiving |
| --- | --- |
| PyUnitWizard 0.28.1 | Active-policy authority, quantity conversion/context, float64 coordinate preparation and QuantityRecord/RecordError serialization through public structures YAML and CCD records. |
| mmCIF 1.1.1 | IoAdapter text input, BinaryCifReader, PdbxReader with selectList, DataContainer/DataCategory getters and explicit/gzipped/CCD resource handling. |
| ArgDigest 0.14.0 | AliasTable, Domain, FunctionContract, caller helpers, scientific-array pipeline and strict Boolean bypass; native context, precision and argument-contract controls. |
| DepDigest 0.15.1 | DeclaredRegistry with adapter loading, lookup/failure causes, retry/refresh, visibility and selective public conversion; availability guards remain separate from metadata inspection. |
| SMonitor 0.16.0 | Signal, catalog diagnostics, structured exception/warning bundles, profile resolution and warning reconstruction; no dependency on the newer private catalog helper because the host retains its documented fallback. |

The selected source profile passes 581 cases and explicitly skips 14 optional
ownership-study cases that require ArgDigest >=0.17.0. Those omissions do not
establish coverage at 0.14.0 and do not justify raising the runtime floor merely
to run an optional study. A separate 133-case profile passes actual CCD parsing,
fixed-state preparation including the #621 controls, and the three public
preparation doctests with these same public provider payloads. Scopes overlap.

As in the earlier floor harness, only the development distribution's newer
`smonitor` pytest bridge is disabled with `-p no:smonitor`, because that entry
point is absent in 0.16.0. The SMonitor core, real catalog/handler tests,
Pytest Receptor and xdist remain active. Ordinary development qualification
keeps its normal plugin enabled. This is not clean installed-runtime closure
or optional-engine/version-matrix qualification.

Optional Ackredit 0.9.0 is also received from its actual public `main` archive.
The historical locally built cache archive has a different container SHA-256;
all 62 Python files nevertheless match the public payload byte-for-byte. The
current floor profile imports a separately unpacked, hash-verified public
archive. Earlier code-level receiving is source-parity evidence, not proof of
that local archive's canonical installed-artifact identity. No Ackredit runtime
defect was found; no provider issue or source modification is warranted by a
different local build container alone.

These results ground the retained support-provider floors. The reviewed values
in pyproject.toml remain unchanged. Finish the remaining optional-feature and
NumPy restriction review and the actual Viewer acquisition boundary below;
these source profiles do not close #524.

Placement source `4f8b0336425292608490b8217e43de2d003ca6f1` and the
[support-floor receipt](../../devtools/data/runtime_support_floor_receiving_524_20261106.json)
retain all three changed placement/test files, actual public artifacts and
import origins, original failed attempts, commands, exits and the fourteen
explicit ownership-study omissions. Thirteen additional strict Pandas/placement
controls pass without warnings, including the existing chemical owner's empty,
reversed and metadata-bearing tables. Scopes overlap. #621's separate receiving
binds its consumer correction and preserves its responsibility independently.

## Remaining scope and acceptance criteria

- Resolve the public Viewer acquisition/floor boundary with its owner. Source
  receiving and the redesigned host's eventual public release remain distinct;
  complete clean installed-runtime closure with the actual qualified host artifact.
- Review every optional runtime-feature declaration, including the documented
  PyParsing exclusion; source-inventory inspection is not optional-engine qualification.
- For each retained bound/exclusion, record exact provider behavior, owner and
  reassessment condition. Finish the NumPy version/ABI-bound disposition;
  preserve exact development/build/release pins.
- Run dependency-route and pertinent runtime checks, then report immutable
  owner evidence to uibcdf/molsyssuite#137. Keep #524 open until this review is complete.

## Provenance

Local Linux source checkout, shared Python 3.14.7 development environment and
read-only reuse of an existing Python 3.11 environment for isolated provider
probes. Wheels and scratch outputs remain under `.pytest_cache/stabilization-524`.
No environment is created, installed over or downgraded; no package is published.
