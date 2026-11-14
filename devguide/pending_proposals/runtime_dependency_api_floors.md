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
are repaired. MDTraj/PyParsing constraints, the NumPy ceiling disposition and
optional-route auditing are received below. The final non-host provider source
review is delivered. MolSysViewer's public minimum and clean installed closure
remain open; no MolSysMT candidate artifact is qualified here.

## What

### ArgDigest bypass contract and Biopython route — 2026-11-04

Consumer receiving under [#549](../archive/resolved_bugs/reconcile_legacy_amino_acid_name_mappings_with_native_protonation_labels.md)
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

Public checkpoint `ad6b71e97` independently matches all 14 checked preparation,
placement and receiving blobs. #621 is independently verified closed; this
review remains partial. The [delivery receipt](../../devtools/data/support_preparation_delivery_621_20261106.json)
retains the verification and complete board checkpoint without treating source
receiving as an installed-runtime or release certificate.

## MDTraj metadata floor and parser exclusion — 2026-11-06

The formerly unbounded optional MDTraj declaration now selects `>=1.11.0`,
aligned with development and test environments. MDTraj stays optional. The
native exporter always passes `formal_charge`, including unknown values;
1.10.2 rejects that keyword. Version 1.10.3 accepts it but its topology copy
loses chain labels and charges. Seven initial export probes passed there,
without qualifying its copy contract. A broader run exposes the missing chain
label; directed public-copy controls then fail on the same provider.

The inspected upstream 1.11.0 source contains
[chain-label preservation](https://github.com/mdtraj/mdtraj/commit/801d4074ab7a36d560cbd5f46e088de56a60dad5)
and [formal-charge preservation](https://github.com/mdtraj/mdtraj/commit/6b59e16f2f9362b9b99bc2313d1136688f6516a5).
Its published metadata retains Python >=3.11. This grounds the selected floor
in consumed operations rather than choosing the newest provider, whose 1.11.2
requires Python >=3.12. Exact public wheels are hash-verified and imported from
an unpacked cache; no environment is created or downgraded.

Final source receiving passes 1,191 cases with 1.11.0/Python 3.13 and the same
1,191 cases with published 1.11.2/Python 3.14, without failures or omissions.
The minimum profile uses the already received public support-library floors.
The newer profile uses the ordinary development support providers; it is not
a second published-support or installed-package qualification. Nine directed
export/copy cases also pass on 1.11.0/Python 3.12. Public Python metadata admits
3.11; its full lane remains part of the final candidate matrix.

The source review additionally reveals MolSysMT's separate selected-subset
metadata defect [#623](../archive/resolved_bugs/mdtraj_topology_subsets_lose_chemical_metadata_and_retain_sparse_hierarchy_indic.md).
The final profiles include its maintained controls and repair; raising a provider
floor alone would not fix that consumer omission.

The parser exclusion stays `pyparsing!=3.3.3`. A paired Python 3.12/MDTraj 1.11.0
public population profile passes all 72 cases with 3.3.2, while the hash-verified
3.3.3 wheel fails 28 and passes 44, including <=/>= and nested-expression
counterexamples. This confirms a real incompatibility at the selected provider
floor. The owning successor qualification remains #486; do not re-admit the
broken artifact or claim a future fix from a version number alone.

Original failures are retained separately: the 1.10.2 API counterexample,
the initial repeated-selection fixture assumption corrected during #622,
the 1.10.3 copy failure, a Python-3.12 broad profile missing optional RDKit,
and a Python-3.13 pytest initialization failure because sandboxing denied the
rerun plugin's local IPC socket. The latter stops before collection; the
unchanged test profile passes when its local IPC is permitted. No test assertion
or required profile is disabled to turn either receiving limitation into a pass.

## Optional-route audit receiving — 2026-11-06

The former route auditor ignored runtime optional requirements. It now reads
the names and complete constraints of the inventory-selected `soft` extra from
pyproject.toml. Environment entries are checked when present, while a names-only
`optional_required` list retains intended MDTraj/parser/OpenFF coverage. Recipes
continue to require only unconditional runtime packages. Conda's toolkit-base
alias resolves to the public OpenFF provider; missing nonrequired engines remain
allowed. No independently maintained version table is introduced.

The executable OpenFF version constants are removed from the lazy-import
validator; that tool retains its import-boundary responsibility. The existing
OpenFF tests still protect known capability minima, accepting a justified later
floor without exact-string duplication. The generalized route tests protect
both OpenFF presence and constraint equality in development/test environments.

Independent review found a meaningful coverage hole: a pip requirement with an
always-false Python marker could appear to satisfy required OpenFF coverage.
The comparison now includes markers, extras and URLs as well as version ranges.
A well-formed matching extra remains parseable; a false or unreviewed override
cannot impersonate the declared provider. The original mutation failures and
the intermediate extras-token parsing failure remain evidence, not waived tests.

Joint source receiving passes 654 route/provider/workflow/documentation cases
without omissions, including 35 audit cases and seven real provider operations.
The static audit does not prove that a solver installed the providers, interpret
every future conditional-platform contract, or replace clean installed receiving.

## NumPy version and ABI disposition — 2026-11-06

Retain `numpy>=1.26` and remove the former `<3` ceiling from public metadata,
both recipes, four runtime-bearing environments and three artifact-test
workflows. Exact Rust/toolchain, Python and release pins remain unchanged.

Locked Rust NumPy 0.29.0, registry checksum
`6a5b15d63a5ff39e378daed0e1340d3a5964703ea9712eb09a0dc66fade996f4`,
defines ABI `0x02000000` in `src/npyffi/numpyconfig.rs` and rejects a greater
runtime ABI in `src/npyffi/array.rs`. Its module-layout branch accepts version
majors >=2. This is an actual ABI restriction, not evidence that a NumPy 3
version necessarily uses another ABI. The suite's incompatibility-based bound
rule does not justify that guessed version-family exclusion.

Existing exact NumPy 1.26.0/2.4.6 probes execute the real unchanged extension;
the current joint provider profile also exercises it. No NumPy 3 artifact is
qualified. The native bridge and dependency maintainers own reassessment on
an ABI transition, a bridge change or a concrete compatibility report. Retain
exact artifacts/import origins, runtime ABI/API values and real calculations;
a demonstrated mismatch can justify a precise restriction. The bridge is not
rebuilt or bypassed by this metadata disposition.

## OpenMM receiving and optional-boundary repairs — 2026-11-06

Optional `openmm>=8.2.0` is grounded in the native exporter's unconditional
`formalCharge` keyword, including unknown values. Upstream first introduces
that API in `fb50d37665b43dbb3df0c136931cd9b8d7ae6d92`; the first stable
8.2.0 tag is `53770948682c40bd460b39830d4e0f0fd3a4b868`. The preceding
8.1.2 source signature lacks it. Development/test acquisition and names-only
optional coverage agree with pyproject.toml; OpenMM remains optional.

Exact public wheels are hash-verified and unpacked without replacing any
shared installation. Actual OpenMM 8.2.0/Python 3.12 and 8.6.1/Python 3.14
each pass the same 2,098-case topology, Context, Simulation, Modeller,
mechanics, reporter and analytical-force selection without omissions. Both
execute a Reference harmonic energy control of 0.5 kJ/mol. The minimum profile
uses the received public support floors and the documented old-SMonitor bridge
exception; the ordinary newer profile keeps its normal bridge. Neither is
clean installed MolSysMT or whole-platform qualification.

The attempted older public 8.1.1 wheel fails its NumPy 2 bindings before the
physical/API call. That is a retained unsupported-provider counterexample,
not proof that the formalCharge call itself raises TypeError. The original
8.2 declaration/copy probe also retains two failures: unbounded metadata and
the distinct consumer bug [#626](../archive/resolved_bugs/openmm_topology_copies_lose_chemical_metadata_and_extraction_misroutes_structure.md).
Its source `207d054cbc3281e43a291d759d9160ebadf61c9d` preserves copy/subset
chemistry, labels, boxes and topology-only structure compatibility. Raising
a provider floor alone would not repair those omissions.

The same review finds [#625](../archive/resolved_bugs/pdbfixer_file_and_text_constructors_bypass_optional_dependency_guards.md):
file/text PDBFixer constructors lacked execution-time availability guards.
Source `80590ef769cf9336b9f4fd45f452b453f1fe72c0` adds the existing DepDigest
boundary, preserving unrelated import causes and native-only conversions.
Its 26 guards, present-provider controls and public examples pass with the
ordinary SMonitor bridge. This diagnoses availability; it does not establish
a PDBFixer scientific/version floor. Public artifacts 1.10/1.11/1.12 already
provide a useful separate cap-completion counterexample; its broader receiving
and declaration remain the next bounded task.

The [OpenMM receipt](../../devtools/data/openmm_runtime_receiving_524_20261106.json)
retains immutable source/artifact identities, actual origins, commands/native
exits, initial failures, fixture corrections and Markdown-only notebook
preservation. Public checkpoint `4d1d5949aa6a717000ac5d01a6a818f0cc99aa5d` independently
matches all 24 changed blobs; #625/#626 are verified closed as completed. The
[delivery record](../../devtools/data/openmm_runtime_delivery_625_626_20261106.json)
retains the source/board receiving. This report remains partial and audit
progress remains 40%.

## PDBFixer floor and non-runtime declarations — 2026-11-06

Source `fac0d870606f85b4b501f8822b4a472c540dc1ed` selects optional
`pdbfixer>=1.11`, retaining both the public pH engine and native alternatives.
Its consumed cap-completion fix is upstream
[b31b57b](https://github.com/openmm/pdbfixer/commit/b31b57b17fb24e96ba9c1f2df08666ccd1d9b56b),
first in stable 1.11. Verified public Conda archives 1.10/1.11/1.12 have source
payloads matching their upstream tags. No incidental installed version defines
the floor, and no unsupported upper bound is added.

The literal ACE–ALA–NME case distinguishes providers through the actual public
`add_missing_hydrogens(..., pH=7.4, engine="PDBFixer")` route. The source has
10 heavy atoms. Provider 1.10 produces only 15 atoms (cap H counts 0/0), fails
the maintained assertion and cannot match the AMBER ACE template. Provider
1.11 completes 22 atoms with ACE/ALA/NME H counts 3/5/4; a separate ForceField
construction accepts 22 particles. The source remains unchanged. The explicit
fixed-state route still requires RDKit; this is not fixed-state PDBFixer support
or a general validation of hydrogen orientation/protonation.

Final actual PDBFixer 1.11/OpenMM 8.2.0/public-support-floor receiving on existing
Python 3.12 passes all 172 selected cases. PDBFixer 1.12/OpenMM 8.6.1 on existing
Python 3.14 passes the same 172, with the ordinary SMonitor bridge. Both have
zero omissions. The initial minimum attempt has 171 passes and one RCSB fixture
setup error from sandbox DNS; that node separately recovers. A harness name
collision overwrote the initial XML with the recovery, so original counts rely
on its observed native terminal/invocation, not that XML. The final complete
selection has distinct, non-overwriting artifacts and is authoritative. Warnings
for unassessed placement, dropped attributes and legacy H5MSM remain explicit.

Source `0a06a01c22906dfbde9ae69a05904200f4cd679c` separately retires unused
runtime declarations. OpenMMTools has no supported runtime route; its two
unexported drafts already fail on missing local utils imports. Retain those
historical drafts and their signature waivers; revival needs a supported API,
acquisition route, grounded provider contract and tests. Plotly has a real
NGLView documentation consumer and moves to the `docs` extra/docs environment,
with annotated development acquisition retained. It leaves runtime soft/DepDigest,
the test environment and unrelated ArgDigest receiving. That receiving route
also declares the accepted OpenMM/MDTraj minima. No showcase or generated HTML
is removed, and no replacement protocol is invented.

The [PDBFixer receipt](../../devtools/data/pdbfixer_runtime_receiving_524_20261106.json)
retains exact public artifacts/origins, direct/public counterexamples, native
exits, final receiving, the corrected evidence collision and notebook protection.
Another 625 dependency/registry/controlled-route/documentation cases pass without
omissions; 14 fast gates pass. These source profiles do not establish clean
installed MolSysMT or a Viewer pair. Batched public delivery follows; #524 stays
partial at accepted audit progress 40%.

## RDKit API and fixture receiving — 2026-11-06

Source `883e4e45ad86e065c092001dd973a02a991f227b` selects optional
`rdkit>=2024.3.4`, aligned with development/test acquisition, controlled
ArgDigest receiving and names-only coverage. The previously absent direct
RDKit declaration in the development environment is explicit now.

Constrained property matching arrives in 2023.09.1, 3D chirality cleanup in
2024.03.1, and the consumed Conformer.SetPositions array API first appears in
stable Release_2024_03_4 (`201fe1ad9c0ea2838506b7eac9c3ed692b13acd2`).
The verified 2023.9.1 wheel lacks the latter two APIs. Actual 2024.3.4 array/API
probes pass with both NumPy 1.26 and 2.4; the source change does not merely select
the newest installed provider. Its direct strided-array limitation is not
exposed by the consumed paths: existing native Structures freeze canonical
contiguous blocks. Four native unit/layout cases protect that boundary.

Paired public 2024.3.4/Python 3.12/public-support-floor and 2025.9.5/Python 3.14
profiles each pass 541 cases and omit one conditional negative-string case:
CCO is valid SMILES with RDKit installed. Positive CCO parsing/conversion is
separately exercised. The selection covers native coordinates/chemistry,
correspondence, symmetry RMSD, coordinate CIP, aromaticity, molecular/atomic
scores, partial charges and fixed-state H preparation. These are not
zero-omission profiles or whole-platform/installed qualification.

The first minimum run passes 530, fails four and omits one. Those four are
malformed reference fixtures [#627](../archive/resolved_bugs/descriptor_sdf_reference_fixtures_duplicate_v3000_valence_on_supported_rdkit_wri.md),
not a native parser defect: older conforming writers already emit VAL and the
tests appended it again. Source `13b82905c870253ef52224ad5801d399b69db22a`
shares a small independent-writer fixture helper, preserving matching fields,
adding only missing evidence and rejecting conflicts/duplicates. Scientific
score/state assertions and production parsing are unchanged; seven new guards
exercise both writer variants regardless of installed version. The
[receipt](../../devtools/data/rdkit_runtime_receiving_524_627_20261106.json)
retains exact artifacts/origins, all attempts, units/immutability and the
preexisting contiguous-storage protection. Public delivery/627 closure follow.

The parallel optional review reproduces two more included-operation defects:
[#628](https://github.com/uibcdf/molsysmt/issues/628) has MDAnalysis
copy/subset bond-evidence and force loss plus two copy failures (native baseline
26 failed, four passed); [#629](https://github.com/uibcdf/molsysmt/issues/629)
has native/OpenMM-to-ParmEd charge/geometry/ID loss (valid baseline 15 failed,
two passed). An earlier 629 attempt also retains 12 invalid test-root-class
imports, corrected only in the fixtures. These distinct consumer defects must
be repaired and qualified; a newer provider floor does not solve them.
Both consumer repairs and finite paired actual-provider receiving are now
complete as recorded below; public delivery and issue closeout follow.

The prior PDBFixer/runtime-docs checkpoint is public as
`dd60ee7d6855a21f24759def1d387abfbbb6a818`; all 16 checked files independently
match GitHub. The
[delivery record](../../devtools/data/pdbfixer_runtime_delivery_524_20261106.json)
retains the verified
[central graph handoff](https://github.com/uibcdf/molsyssuite/issues/137#issuecomment-6701640436).
Graph refresh was requested, not claimed complete. This report remains partial;
accepted audit progress is 40% and no candidate artifact is selected.

## MDAnalysis and ParmEd consumer receiving — 2026-11-06

Source `f81ba2025` repairs #628's provider copy/subset routes without chemical
reconstruction. It preserves nullable/long connection labels, numeric orders,
guessed flags and available forces. Full-context AtomGroup copying and compact
extraction are documented separately. Actual public MDAnalysis 2.8/Python 3.12
and 2.10/Python 3.14 profiles each pass 155 cases without omissions. The
[receipt](../../devtools/data/mdanalysis_runtime_receiving_524_628_20261106.json)
retains the 26-failure/four-pass baseline, two failed harness/probe attempts,
the refuted connection-alias hypothesis, public artifacts and visible warnings.

Source `e270eda9b` repairs #629 with direct explicit-domain native ParmEd export,
faithful represented geometry/chemistry/labels and honest unknown mechanical
assignments. Unsupported target semantics have typed rejection and bounded
preflight findings. Actual public ParmEd 4.3.1/Python 3.12/OpenMM 8.2 and
ParmEd 4.3.1/Python 3.14/OpenMM 8.6.1 profiles each pass 185 without omissions.
The [receipt](../../devtools/data/parmed_runtime_receiving_524_629_20261106.json)
retains the valid 15-failure/two-pass baseline and distinguishes twelve earlier
test-authoring errors. This does not certify every ParmEd writer or simulation.

Source `33a702bfa` aligns optional `MDAnalysis>=2.8.0` and `parmed>=4.3.1`
acquisition and audit coverage. The former grounds public NumPy2 builds and
controlled guessing; the latter fixes consumed NumPy2 setters and imports
after `numpy.compat` removal. No guessed upper bound or hard dependency is added.
Joint conversion/descriptor/documentation receiving passes 1,271; registered
[scientific execution](../../devtools/data/runtime_provider_scientific_receiving_524_20261106.json)
passes 97 cases/64 nodes without omissions. Scopes overlap and tracked human
documentation/report edits make that certificate explicitly development-only.
Source/public delivery is still distinct from installed-release qualification.

## Public delivery of the consumer repair block — 2026-11-06

Checkpoint `82bfa1c82f1d48035679fa4630e81a2506b67bd6` independently matches
all 58 changed public blobs; #627/#628/#629 are verified closed as completed.
The [delivery receipt](../../devtools/data/runtime_provider_delivery_627_629_20261106.json)
keeps those source/board facts separate from installed/graphical qualification.
No new externally reported issue appeared in the complete board refresh:
561 total issues, 98 open; PR #543 remains at `8ab2f5474`. Remaining optional
providers and actual host/installed closure keep #524 partial, progress 40%.

## Final optional-provider source qualification — 2026-11-06

Source `d850f6cc1` uses public Biopython row access, with optional minimum 1.80;
earlier 1.79 integer-row indexing exists but raises NotImplementedError. Final
actual minimum/newer profiles each pass 385, zero omissions. Source `5cd744ebf`
aligns the remaining provider floors and supported acquisition routes, including
optional NGLView >=3.0.4 and Conda-forge AmberTools for PyTraj. The existing
OpenFF minima remain >=0.17.1/0.3.0, with floors stored once in the non-installer
`tool.molsysmt.provider-requirements` table in pyproject. Its ordinary pip extra
and DepDigest commands no longer point to yanked/unusable distributions. Project
existence, exact-version absence and ordinary installer usability are distinct.

Versioned Conda providers derive names/channels from DepDigest and constraints
from pyproject. Unversioned PyTraj keeps its deliberate bundle/ABI disposition.
The route auditor rejects missing/duplicate providers, invented aliases, pip
overrides, channel/constraint drift and malformed declarations. Actual artifact
and engine receiving is separate from those static declarations.

Both final OpenFF/runtime/route profiles pass 199 without omissions. The actual
current PyTraj/native/diagnostic selection passes 146; old/new CPPTRAJ plain
probes retain their distinct engine scope. Source `e5d1dd0f8` corrects #630 and
`fae9ab557` corrects #631; complete NGLView minimum/newer selections each pass
104, including a real doctest and scoped coordinates/resources/theme guards.
The [NGLView receipt](../../devtools/data/nglview_runtime_receiving_524_630_631_20261106.json)
and [remaining-provider receipt](../../devtools/data/remaining_optional_runtime_receiving_524_20261106.json)
retain failed attempts, actual origins, namespace/version anomalies, native
exits, source-only boundaries and exact source commits.

Joint receiving passes 798; registered scientific execution passes 97/64 nodes;
all 14 fast gates pass. HTML compilation exits zero with notebook execution and
autosummary source generation disabled; four existing title-underline warnings
remain visible. Protected human edits are unchanged. Counts overlap. This
finishes finite optional-provider source qualification, not #524's compatible
public Viewer floor or clean installed closure. Public delivery/board closeout
of the new corrections follows; accepted audit progress remains 40%.

## Final optional-provider delivery — 2026-11-06

Public checkpoint `7e61fcc5c924669f197dcf31a9a5686e796d2670` independently
matches all 39 changed blobs. #630/#631 are verified closed as completed; the
audit-related closed count is 19. The complete board has 563 issues, 98 open,
and unchanged PR #543 at `8ab2f5474`. The
[delivery receipt](../../devtools/data/remaining_optional_runtime_delivery_630_631_20261106.json)
retains source/board receiving and the independently verified
[central graph notice](https://github.com/uibcdf/molsyssuite/issues/137#issuecomment-6702909839).
Owner-side graph refresh is requested, not claimed complete. Optional-provider
source review is delivered; #524 stays partial for the compatible public
Viewer floor and clean installed closure. Accepted plan progress remains 40%.

## Remaining scope and acceptance criteria

The [coordinated release plan](../pre_1_0_completion_handoffs_20261110.md#molsysviewer-contract-feedback-startup-evidence-and-artifact-plan)
records **MolSysMT 1.0.0 and MolSysViewer 1.0.0** for final clean installed
qualification. The maintainer defers an intermediate release and chooses to
wait for that final pair. The published addon floor still requires evidence
from compatible artifacts and clean minimum/newer installed receiving. Keep
the older published pair in its tested scope.

The latest local profiles pass 385/385 for Biopython minimum/newer, 86/86 for
OpenFF minimum/newer and 146 for PyTraj acquisition/native/diagnostic/auditor
receiving. Counts overlap with prior blocks. Original missing-helper and guard
authoring failures are retained, not converted into provider defects or omitted
cases. Biopython uses the public row-indexing protocol, operational since 1.80;
OpenFF floors stay unchanged. PyTraj acquisition is Conda-forge AmberTools with
explicitly disabled pip routing, guarded native ABI and no invented bundle-to-
provider version equivalence. Static route checking does not qualify a resolver.

The completed NGLView source review includes #630's internal validation keyword
leak and #631's independent widget initial structure. Their delivery and guards
are recorded above; frontend and installed-artifact limits remain. The OpenFF
acquisition review likewise retains its delivered Conda-only route. Those
completed source corrections are not additional outstanding implementation.

Public checkpoint `f5c909e75d786a20d92f4b57e6fa2875a3ba651e` independently
matches all 32 checked source/test/documentation/receiving blobs. #623 is
verified closed as completed. The immutable
[central #137 handoff](https://github.com/uibcdf/molsyssuite/issues/137#issuecomment-6700875331)
is published and its body independently verified; graph refresh was requested
from its owner and is not claimed completed. The
[delivery receipt](../../devtools/data/optional_runtime_delivery_623_20261106.json)
retains these boundaries. This report stays partial.

- Resolve the public Viewer acquisition/floor boundary with its owner. Source
  receiving and the redesigned host's eventual public release remain distinct;
  complete clean installed-runtime closure with the actual qualified host artifact.
- The final optional-provider source block, guards and #630/#631 closeout are
  delivered as recorded above. Retain these API-grounded floors, Conda-only
  routes and finite consumer evidence while completing the actual host/installed
  exit. Retired unsupported/docs-only declarations keep their distinct
  dispositions. Source receiving does not supply a public Viewer floor.
- For each retained bound/exclusion, record exact provider behavior, owner and
  reassessment condition. The NumPy version/ABI disposition above is complete;
  preserve exact development/build/release pins and any demonstrated restrictions.
- Retain the central #137 source/graph handoff as adoption advances. Reopen a
  non-host provider review if actual changed usage, metadata or receiving
  exposes a concrete gap. Keep #524 open until the host and installed closure
  are complete.

### Finite exit at the coordinated pair — 2026-11-14

The remaining work is the following existing compatibility boundary, rather
than another general optional-provider audit:

| Required conclusion | Evidence needed to close it |
| --- | --- |
| Public MolSysViewer minimum | Agree the version carrying the consumed addon/lifecycle APIs; verify its actual compatible package and record the inclusive minimum in pyproject.toml and the audited secondary surfaces. A source SHA or future version label alone is insufficient. |
| Clean installed runtime closure | Receive the exact coordinated packages outside checkouts, recording import origins, artifact identity and resolver/dependency consistency. Exercise ordinary public/native get/info, conversion, addon lifecycle and the agreed persistence/session workflows. Preserve failures and unsupported scopes. |
| Minimum and newer provider profiles | Exercise the declared compatible bounds using real artifacts and record the actual solved versions for each admitted Python lane. API probes and development overlays remain supporting source evidence. An old provider build unavailable for a newer Python minor is not a tested minimum environment. |

The existing dependency auditor and installed-pair tooling own these checks;
this table adds no installer, speculative floor, compatibility cap or separate
release matrix. Candidate construction, hosted qualification and publication
retain the agreed pause. Final producer selection and the same exact artifacts
remain prerequisites for the installed conclusion.

## Provenance

Local Linux source checkout, shared Python 3.14.7 development environment and
read-only reuse of an existing Python 3.11 environment for isolated provider
probes. Wheels and scratch outputs remain under `.pytest_cache/stabilization-524`.
No environment is created, installed over or downgraded; no package is published.
