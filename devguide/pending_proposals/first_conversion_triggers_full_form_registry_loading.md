---
summary: Avoid loading the complete form registry on first conversion.
issue: uibcdf/molsysmt#382
status: partial
opened: 2026-10-10
closed:
verification: measured
area: [form, performance, deps]
guard: tests/form/test_declared_registry_integration.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# First conversion triggers complete form-registry loading

**Reported:** 2026-10-10 by ElastNetMT, consumer uibcdf/elastnetmt#26.
**Status:** DepDigest 0.15.1 is publicly admitted and uibcdf/depdigest#39 is closed.
Consumer adoption and local source validation are complete. Required platform,
supported-interpreter and installed-pair admission remain under the paused #334.
Existing preparation statements below describe their dated checkpoints; they
do not mean that the provider requirement is still blocked.

## What

The reported first conversion to `molsysmt.MolSys` initialized all eligible form
adapters. Metadata-based detection already avoided that cost, but target validation
and conversion dispatch used the generic scan-on-first-access registry.
Reduce this cold cost without changing scientific conversion behavior, dependency
visibility or supported registrations.

## How

`digest_to_form` imports `_dict_forms_lowercase`, constructed by iterating
`molsysmt.form._dict_modules.keys()`. DepDigest's `LazyRegistry` initializes by
importing every eligible plugin. A direct `_dict_modules[form]` lookup also starts
that scan; changing only the lowercase-name dictionary moves the cost rather than
removing it.

MolSysMT already owns adapter-local `form.json` declarations and
`form.catalogue`. Detection uses declared class/extension keys and confirms the
candidate with its real detector. Converter modules are independently lazy strings
resolved by `form.load_converter`. Reuse these pieces.

DepDigest owns generic discovery, configuration/dependency filtering, plugin
loading, caches and load diagnostics. Its current public `LazyRegistry` interface
does not accept an identity-to-plugin declaration index or provide an indexed
lookup without whole-registry initialization. Request that additive capability
from its owner, then make MolSysMT supply declarations and consume it. Preserve
the existing legacy route for unindexed extensions where appropriate, with an
explicit contract. Do not implement a competing registry in MolSysMT.

## Why

Cold startup dominates small client workloads such as local PDB preparation for
ElastNetMT. The incoming consumer record independently separates first/repeated
file preparation from prepared input and retains exact contact/node parity.
Its 1TCD workload and its consumer-level times are not interchangeable with the
provider-only 181L conversion measured here.

## What is measured and what is assumed

Three initial diagnostic workers on source
`3347a108a19177482dcab4bd73a02374c960cd5e` validate only
`to_form='molsysmt.MolSys'` after importing the form helpers. This adds **1,156
form package/submodule entries** in each worker, taking **3.258–3.408 seconds**.
The observed whole-registry scan takes **3.255–3.405 seconds**, nested inside that
validation. Do not sum these overlapping times or describe this isolated probe as
an unprofiled complete client workflow. It instruments the scan with a small
timer wrapper and provides diagnostic attribution, not an optimization result.

The maintained measurement tool separates two workloads:

```bash
python devtools/scripts/benchmark_form_registry_startup.py --mode conversion --trials 3
python devtools/scripts/benchmark_form_registry_startup.py --mode validation --trials 3
```

Conversion mode times root import, the first public PDB conversion, repeated PDB
conversion and conversion of the prepared public MolSys separately. Validation
mode instruments the scan and validates the target first; its subsequent file
conversion is already warmed and is explicitly named accordingly. Each trial is
a new interpreter. Timings exclude later parity checks and provenance collection.
Neither mode computes contacts or measures a complete ANM workflow.

The tool checks 13 molecular attributes through public `compare` outside timed
regions, including atom IDs/order, groups, connectivity/orders, formal charges,
coordinates, box and time. It verifies unchanged fixture bytes and records all
raw samples, the input/tool/native hashes, host/Python and actual editable source
identities independently of distribution versions. PID values are informative;
PID namespaces can reuse their visible numbers for independent workers.

These initial measurements precede optimization. A later source prototype is
measured below; no universal speedup, memory saving or installed-candidate
qualification is established. Public comparison on one PDB does not qualify
every form or scientific consumer.

The [retained receipt](../../devtools/data/form_registry_startup_20261010.json)
contains the initial diagnostic and three samples per maintained mode. On this
host, conversion-mode medians are **3.793 s** for the cold public conversion,
**0.514 s** for repeated file conversion and **0.0316 s** for prepared conversion;
the separately timed root import is **0.508 s**. Prepared conversion presupposes
the original conversion and retains normal public validation. It is not a PDB
workflow completed in 0.0316 s.

Maintained validation mode has a **3.342 s** target-validation median and **0.443 s**
subsequent warmed conversion median. It adds 1,163 form module entries during
validation and 1,166 by conversion, starting the counter before the form helpers
are imported. The initial isolated diagnostic imported those helpers first and
counted 1,156; these counters have different boundaries, not different results.
The receipt retains the complete raw scan traces; cumulative/nested durations
must not be added. No concurrent local pytest run was used during retained
maintained-tool measurement; other host load was not controlled.

## What was refuted

- Metadata does not need a new MolSysMT catalog: `form.json` and `catalogue`
  already provide it, with declaration-consistency guards.
- Changing only `digest_to_form` cannot eliminate cold startup because the first
  module lookup independently triggers the same scan.
- Calling `catalogue.module_of` everywhere without reconciling availability and
  registry registrations would create divergent loading/registration paths.
- Manipulating DepDigest's private `_initialized` flag or using base-dict access
  to bypass discovery could silently lose forms and diagnostics.
- Skipping public digestion or dropping PDB bond inference changes the workflow
  rather than solving the measured startup mechanism. PDB inference is #304's
  separate scientific theme.

## Scope and exclusions

MolSysMT owns form declarations, alias validation, converter dispatch and
scientific parity. DepDigest owns the reusable loader extension. This work does
not authorize a new default conversion engine, copied dependency tables, a new
public MolSysMT registry API, provider publication or a changed release artifact.
The existing dependency floor and frozen candidates stay unchanged until an
admitted provider version and qualified consumer adoption exist. An open
performance proposal is not by itself a demonstrated functional release blocker.

## Acceptance criteria

1. Agree a public DepDigest interface that supports declared identity lookup and
   loads only the requested plugin, retaining its default/legacy behavior.
2. Define declared versus available versus successfully loaded identities,
   dependency visibility, configuration freshness, registration/override/removal,
   deterministic ordering and uncatalogued-plugin fallback. Handle conflicting
   identities, mismatched declarations and failed loads with truthful diagnostics.
3. Add a provider sentinel guard whose unrelated plugin fails on import; indexed
   lookup and metadata discovery must never touch it.
4. Adopt the owner interface in MolSysMT's validation and dispatch, without losing
   case normalization, tolerance aliases, optional-dependency checks, dynamic
   registrations or explicit form enumeration.
5. Verify cold public conversions avoid unrelated adapter imports, while full
   discovery still reaches every declared/registered form. Exercise failures and
   configuration overrides rather than only positive counts.
6. Compare raw first/repeated/prepared measurements on identical bytes and sources,
   then qualify form enumeration/converters and scientific consumers across the
   required interpreters. Record evidence separately from speed estimates.

## Dependencies and risks

The initial capability in uibcdf/depdigest#34 is publicly admitted in DepDigest
0.14.0; adapter-only inspection from uibcdf/depdigest#36 is admitted in 0.15.0.
The cold concurrent-loading correction in uibcdf/depdigest#39 is publicly
admitted in 0.15.1. The consumer now requires that floor and uses its exact
released source pin. Reconcile the existing catalog's
module cache with provider registrations; do not assume that clearing a registry
unloads Python modules. Configuration overrides are public through DepDigest,
and current compatibility guards explicitly exercise filtered discovery.
Follow-up adoption may affect many dispatchers; its scope must be measured before
admission during stabilization.

## Provenance

Linux x86_64, Python 3.14.7, 2026-10-10, existing shared Suite development
environment. Input: bundled `molsysmt/data/pdb/181l.pdb`, 1,441 atoms,
SHA-256 `77018feaaa65bb22dea47c784e8c059b0ccc09cd6dc7442b79cce83f3170985f`.
DepDigest actual source `ba670098a5b773e7f1570adc47b890d063bd5627`, clean;
distribution metadata `0.12.0+13.g104661a`. Other exact versions and sources are
retained in the benchmark receipt. Editable distribution metadata is not evidence
that a published package has those source changes.

The host exposes 20 logical CPUs. Retained native SHA-256:
`76f5dd6c8ee8c97428d6727bd80df5468fcf3e8f68838d9798c7e3ccd150a79c`.
The runtime source remained unchanged; its recorded dirty state consists of this
measurement tool, tests and documentation. The receipt retains the final tool hash.

## Preparation checkpoint — 2026-10-10

Three tool guards pass on Linux/Python 3.14.7: actual fresh workers and untouched
fixture bytes for both measurement modes, distinct cold/warmed field names and
public molecular parity, and invalid-input rejection without a success record.
The initial tool check found and corrected aggregation of list-valued diagnostic
scan traces as scalar timing medians. These guards protect measurement integrity;
they do not assert that the outstanding registry optimization is implemented.
No MolSysMT or DepDigest runtime source, public signature or dependency floor has
changed. The provider request and adoption criteria remain open.

Ruff checks/formatting, whitespace validation and all fourteen fast development
gates pass for this preparation checkpoint. The runtime scientific-evidence and
installed-package matrices are neither executed nor replaced by these checks.

## Published-provider adoption review — 2026-10-13

The maintainer authorized continuing consumer adoption after DepDigest 0.14.0
was published. Provider source `1b746ece24587e920e49ea20f2bfebde7c3efc24` is
imported in the shared Python 3.14.7 development environment. Its registry/loader
runtime files match the admitted source `affd73ef04070a9bf492173c0db615292a73e5d1`.
The provider worktree has unrelated pending documentation/tests, preserved
read-only. Its editable distribution metadata remains
`0.12.0+13.g104661a`; this is source review, not installed-version admission.

**Reproduced compatibility limitation:** with CuPy absent and
`show_all_capabilities=True`, the declared identity is visible and a native
MolSys lookup succeeds. Requesting the CuPy adapter through `DeclaredRegistry`
raises `KeyError` caused by the missing engine. The same adapter can be imported
through the existing route and exposes its form type and conversion declarations
without importing or executing CuPy. The published strict gate is working as
specified, but differs from the existing host metadata-inspection contract.

`msm.supported.forms()` and full capability/converter introspection require
adapter metadata. The existing form.json supplies identity/type/class/extension,
not all callable attribute and converter metadata. Dropping failed entries would
silently remove advertised capabilities. Bypassing provider private checks,
subclassing its loader or introducing a second consumer registry was rejected.

The owner proposal is uibcdf/depdigest#36, linked to coordination under
uibcdf/molsyssuite#115. It requests an explicit opt-in adapter-only loading
policy, retaining the strict default, current visibility filtering, true import
errors, identity checks and failure/retry semantics. Importability must remain
separate from optional-engine execution, which stays guarded by dep_digest.
The exact API, tests and public admission belong to DepDigest.

Consumer compatibility controls are in
`tests/test_form_inspection_visibility.py`: fresh interpreters simulate absent
RDKit, verify both public visibility modes and ensure that displayed metadata
never enables execution of the absent engine. The initial four-case compatibility
and dependency-architecture selection passes on Python 3.14.7. These protect an existing
contract; they do not implement the selective loader or establish a speedup.

MolSysMT runtime sources, dependency floors, controlled CI pins and frozen
artifacts remain unchanged. Source adoption will resume after an admitted
provider contract can preserve all-capability inspection, indexed native lookup,
configuration freshness, registrations and converter/scientific parity together.

### Executed consumer preparation evidence — 2026-10-13

Seven focused cases pass on Python 3.14.7 with twelve pytest workers and
pytest-receptor: the two new visibility/execution guards, existing dependency
architecture and fresh-worker benchmark integrity controls. The benchmark
controls run under test load and their timing samples are not retained as a
performance comparison. Ruff checks and formatting and the developer-guide
validator pass. This evidence protects current compatibility and measurement
integrity; it does not qualify an indexed runtime adoption. The front-matter
guard protects the retained inspection contract, not a completed optimization.

## Published 0.15 review and prepared adoption — 2026-10-13

DepDigest #36 is closed and 0.15.0 is published under uibcdf/depdigest#37. The
older #36 blocking statements above are preparation history. A local prototype
uses the published adapter policy and temporarily aligns dependency floors and
the controlled-source pin with 0.15.0. That provisional requirement is insufficient
for the concurrency case below and is not adopted. The existing provider checkout
69f152b22 is clean and its depdigest runtime has no diff from the admitted 0.15.0
tag 01d83c7b1. Distribution metadata is stale and retained separately from source
evidence. All other checkout state from the suite inventory is preserved read-only.

The prepared design lets the catalogue supply identity declarations and own
index/extension semantics. DepDigest owns the module cache, configuration
visibility, errors, refresh and explicit discovery. Catalogue lookup delegates
to that registry instead of a competing cache. Manual identities are considered
after built-in detection misses; true load failures propagate. The dependency
guard uses public refresh rather than private initialization flags. No provider
private API is used by the prepared runtime.

### Concurrent first load and provider handoff

Two fresh threads requesting the same unloaded gzip adapter produce one module
and one KeyError reporting recursive loading with unmodified 0.15.0. The provider
documents no concurrent synchronization; this is a missing consumer capability,
not a claim that it violated a promised thread-safety contract. Warming every
adapter, a consumer registry subclass and silent error suppression are rejected.

A temporary provider copy adds a reentrant lock around one registry's public
lookup. Both overlapping-load guards fail on the original provider and pass with
the proposal; genuine same-thread recursion remains rejected. The existing
declared-registry suite plus these guards passes 55 tests. This only tests
overlapping lookup: concurrent mutation/discovery and arbitrary cycles between
multiple registries are excluded, and the provider must review the lock tradeoff.

The maintainer chose provider-team delivery. The complete patch and self-contained
guards are delivered in [uibcdf/depdigest#39](https://github.com/uibcdf/depdigest/issues/39#issuecomment-6152148420).
The provider checkout, refs and artifacts are untouched. Coordination remains
linked to uibcdf/molsyssuite#115. MolSysMT adoption waits for a fixed admitted
version; >=0.15.0 alone is not a sufficient requirement.

### Same-input measurements and bounded validation

The [preparation receipt](../../devtools/data/form_registry_adoption_preparation_20261013.json)
retains three fresh-process samples for each stage, using the unchanged benchmark
tool and 181L bytes on Linux/Python 3.14.7, with 20 logical CPUs. No concurrent
local pytest workload ran during measurement; other host load was uncontrolled.
The baseline is clean MolSysMT c35252d89. The prepared consumer uses a temporary
copy of provider 69f152b22, whose runtime matches admitted tag 01d83c7b1, plus the
unadmitted concurrency patch. Exact patch and registry hashes are in the receipt.
Stale editable distribution metadata does not identify the running source.

| Conversion-mode observation | Existing runtime | Final prepared source |
|---|---:|---:|
| Root import median | 0.508 s | 0.526 s |
| First public PDB conversion median | 3.838 s | 0.944 s |
| Repeated PDB conversion median | 0.519 s | 0.289 s |
| First prepared-MolSys conversion median | 0.0316 s | 0.335 s |
| Form module entries added by first conversion | 1,170 | 38 |

The initial indexed prototype still loaded 596 module entries and took 3.320 s.
A separate lookup trace identifies the remaining sweep: convert asks is_item
about the declared destination name, which tries every text/file detector to
reject it. The final preparation rejects declared form names directly in that
predicate, preserving the name-versus-item distinction. Its additional change is
included in the retained consumer patch, not enabled in the runtime.

Selective loading shifts some cost to the first later use of an adapter. In
particular the first prepared-MolSys conversion is slower in this sequence;
the observed cold-file improvement is not a promise that every operation improves.
Validation-mode diagnostics, before the final predicate fix, add seven module
entries during target validation and observe no full-registry scan. Those timing
boundaries differ from conversion mode and are not summed or mixed.

Each trial compares thirteen molecular attributes across its cold, repeated and
prepared outputs outside timing. This is within-trial parity, not an independent
scientific oracle or a cross-implementation result fingerprint. The retained
native SHA-256 identifies unchanged compiled-extension bytes. The tool labels a
module outside a Git checkout as installed; the receipt explicitly corrects that
label for the temporary provider copy. No installed artifact is qualified here.

459 tests pass on the final prepared consumer plus proposed provider correction,
using twelve workers and pytest-receptor. The selection covers visibility with
absent engines, configuration overrides, detection/form rosters, compressed and
plain PDB input, atom correspondences, attribution and symmetry-corrected RMSD.
Existing legacy-H5MSM, NumPy ABI, external placeholder-box and cross-chain-bond
warnings remain. This does not qualify all forms or supported interpreters.

### Retained runtime and next admission steps

The [consumer preparation patch](../../devtools/data/form_registry_adoption_preparation_20261013.patch)
is retained for review. It is not enabled and deliberately excludes provisional
dependency-floor and source-pin changes. Before replaying it, review against the
then-current sources and select the actually admitted fixed provider version.
The provider patch and guards remain available in its owning issue.

MolSysMT keeps LazyRegistry, its released dependency floors and controlled source
pins. No frozen release candidate, tag or publication changes. Remaining work:
admit the corrected provider; replay and review the consumer design; add direct
consumer guards for overrides/removal, failed-load retry and an unrelated failing
adapter sentinel; repeat the source comparison and required compatibility matrix.
The existing front-matter guard protects inspection compatibility, not completion
of the optimization.

### Provider response — 2026-10-13

The provider [reports integration](https://github.com/uibcdf/depdigest/issues/39#issuecomment-6152905375)
of the reviewed per-registry lock in c90edca1ae5d3a2665f8da70f224248d07fd1377.
Its stronger event-controlled guards observe actual lock contention rather than
depending on a scheduling delay. The owning scope covers overlapping value
requests, including different identities, on one registry; mutation, discovery,
retry, refresh and configuration changes require external exclusive coordination.
Initializers must not wait for another thread that needs the same registry, and
arbitrary cross-registry/import/thread cycles remain excluded.

The [candidate update](https://github.com/uibcdf/depdigest/issues/39#issuecomment-6153320557)
identifies source e2757031aa59fe5639672e3c7ab2f979db2dd6f4 for proposed patch
0.15.1. The provider reports 300 source tests with five unavailable-workspace
skips and eight completed Linux/Windows source-matrix cells; four macOS cells
were still queued at that checkpoint. Installed qualification and public
admission were pending. These are upstream-reported candidate observations,
not independently executed MolSysMT evidence or proof of a published dependency.

No consumer change follows from source integration alone. Keep #382 blocked
by #39 until the fixed public version and its admitted identity are delivered;
then review the retained consumer patch and run the outstanding consumer guards
against the actual admitted provider. The original local prototype measurements
do not qualify that forthcoming version.

## Admitted-provider consumer adoption — 2026-10-13

The owner closes uibcdf/depdigest#39 with published 0.15.1, annotated tag
13cc73780a7cb645546ae3f396177f98b86a8792 and independent public-file admission.
The imported provider runtime has no diff from that tag; its pending evidence
files are preserved read-only. The Suite inventory is refreshed and all dirty
or behind sibling states are retained without checkout mutations.

MolSysMT now supplies its declarations to DeclaredRegistry(load_policy='adapter'),
requires depdigest>=0.15.1 across pyproject, both recipes and all runtime-bearing
floor declarations, and pins the exact public provider commit in controlled
sources. The integration guide is copied unchanged from that public tag. The
catalogue's competing module cache is removed. Current visibility, manual
registrations, overrides/removal and failure causes flow through the owning
registry. Public refresh replaces legacy private initialization manipulation.

The normalizer resolves registered names and tolerated native spellings before
item detection. The added sentinel first exposed an unnecessary detector sweep
for molsysmt.structure; resolving that existing alias early fixes it without
changing its destination. Unindexed identities still use explicit discovery or
registration, then fallback detection with the normal host support-tier admission.

### Direct consumer guards

`tests/form/test_declared_registry_integration.py` uses fresh interpreters for
canonical, uppercase and tolerated targets with unrelated adapters that raise
on import. A successful conversion alone cannot satisfy this guard: any attempt
to import the sentinel adapters is rejected even if a loader suppresses its error.
Other cases verify that catalogue lookup and public detection honor overrides,
removal and admitted manual identities; an injected real import failure retains
its exact cause through catalogue and public dispatch, stays cached, and succeeds
only after explicit retry. Cold concurrent public gzip conversions retain input
bytes and independent mutable outputs. Finally two atom-selection cases compare
thirteen actual molecular attributes with the legacy loader on the same host
source, including an explicit nonmonotonic selection. They do not certify every
converter or constitute an independent chemical oracle.

Existing absent-engine inspection/execution-refusal and configuration controls
remain. Twelve bounded integration/visibility/configuration cases pass separately
on Python 3.12.12 and 3.13.14 using existing environments; no package installation
or new environment is performed. Python 3.12 loads Pytest Receptor from its source.
The 3.14 focused conversion/correspondence selection passes 459 cases, and the
added normalization/visibility selection passes 18. Root full-suite execution and
its discovered baseline failures are recorded below and in the receipt.

### Same-input source measurements

The [adoption receipt](../../devtools/data/form_registry_adoption_20261013.json)
retains raw three-trial before/after samples using identical 181L/tool bytes,
Python 3.14.7, the same shared host and admitted provider runtime. The baseline
is 9ae0f8102 before consumer mutation. No concurrent local pytest workload runs
during measurement; other host load is uncontrolled, and root-import medians
also differ. These are bounded observations, not a causally isolated or universal
speedup, memory/RSS measurement, complete ElastNetMT workflow or installed result.

| Observation | Existing runtime median | Adopted runtime median |
|---|---:|---:|
| Root import | 0.684 s | 0.507 s |
| First public PDB conversion | 5.052 s | 0.896 s |
| Repeated file conversion | 0.366 s | 0.281 s |
| First prepared-MolSys conversion | 0.0418 s | 0.329 s |
| Form module entries added by first conversion | 1,170 | 38 |

The first later native-adapter use retains a deferred initialization cost; not
all operations improve in this sequence. Raw software metadata and actual source
identities remain separate. The unchanged native hash identifies extension bytes,
not molecular results. User Guide Foundations/Toolbox, course Module 01 and the
normative forms guide reflect selective loading and optional-engine boundaries.
Both edited notebooks retain every original code cell and stored output and
validate against their declared schemas.

### Full-suite baseline failure audit

The first complete Python 3.14 run executes 14,069 cases with twelve workers,
loadfile distribution and pytest-receptor: 14,062 pass, two skip and five fail.
The four CRD+PSF failures reproduce after restoring the five changed loader/
normalization modules from the baseline and belong to uibcdf/molsysmt#388. Its
adapter flag repair retains the metadata pipe and does not relax the classifier.
The fifth is a stale uppercase download-ID assertion: the existing normalizer
and its dedicated tests specify lowercase. Only that auxiliary assertion is
corrected; the 304 atoms, 20 groups and 38 NMR structures remain checked.
The same five baseline failures are reproduced and prepared runtime modules are
restored byte for byte. Ninety nearby regressions pass after the bounded repairs.
A final whole-suite rerun provides the settled result below.

The final configured suite passes **14,067 cases**, with **two omissions and
zero failures/errors**, in 417.08 seconds on Python 3.14.7, twelve workers and
loadfile distribution. It includes the configured basic-API doctests. The two
omissions are absent CuPy and an invalid-input control inapplicable when installed
RDKit recognizes CCO as SMILES. Existing warning populations remain explicit in
the local receptor log. The receipt records the JUnit digest and complete count
summary. The fourteen final fast gates, Ruff, dependency audit and course/schema
checks pass. This source result does not qualify an installed artifact or another
Python/platform cell.

### Remaining qualification boundary

The provider block is removed; local source adoption is separate from release
admission. Local Python 3.11 runtime qualification is not executed: inspected
existing environments lack the required runtime/test stack. The other-minor runs
are bounded cases, not complete suites. The required supported-interpreter/platform
source matrix, independent scientific-consumer campaigns and installed MolSysMT/
Viewer pair remain part of the paused #334 qualification. Do not replace frozen
files/refs, resume publication, or close this proposal as fully qualified from
local startup timings. No new hosted matrix, package, tag or Release is issued.
