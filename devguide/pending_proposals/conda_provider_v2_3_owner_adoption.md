---
summary: Review Conda provider v2.3.0 adoption for the owned publisher.
issue: uibcdf/molsysmt#544
status: partial
opened: 2026-11-03
closed:
verification: measured
area: [ci, packaging]
guard: devtools/tests/test_conda_release_workflows.py
normative:
blocked_by: []
supersedes: []
---

# Owned Conda provider v2.3.0 adoption

## What

Receive the reviewed immutable provider
`87c70b1443d5f22d738ee3ddf812bdbe0152f6c2` (v2.3.0) for the existing
MolSysMT local native publisher. Central delivery is
`95f693be10c9205ab9b912cb53453710a207bf45`, coordinated under
uibcdf/molsyssuite#87. This is an owner source review; publication, promotion,
release version selection and package replacement are not requested.

## How and why

The inherited source has two root action calls in the publisher, a third in
the upload-disabled ABI3 experiment, and a separate promotion action at v2.2.2.
Review all four active call sites against the exact provider source and pin
them together. The central noarch workflow is not an appropriate replacement
for the native/ABI3 platform profile. Historical workflow backups and producer
receipts retain their original references.

The provider retains the accepted inputs and outputs. Its build operation now
uses the active Conda executable even if shell activation keeps a base manager
function. Both `.conda` and `.tar.bz2` archives are discovered. A requested
conversion rejects `.conda` before conversion or removal; conversion requires
`.tar.bz2` and is not cross-compilation of native extensions. MolSysMT uses
native host builds with `.conda`, without any conversion selectors, so its
format and ABI3 recipe remain applicable.

Promotion retains exact package coordinates, SHA-256, staging/main labels,
independent read-only lookup and a bounded receipt. Its stricter distribution
inventory checks reject duplicate, incomplete or contradictory identities.
MolSysMT's explicit package/version/subdir/filename and lowercase digest inputs
meet this contract. The installed-pair gate remains before promotion and the
independent public verifier remains after it.

## Scope and unchanged contracts

- Four native platforms and one ABI3 file per platform; no noarch migration or
  platform conversion.
- Existing active build environments, Rust/recipe settings, candidate selection,
  staged/direct routing and version/build arguments.
- Existing producer `built_paths`, `evidence_path` and `evidence_artifact_name`
  outputs, attempt/matrix identity and failure-path receipt retention.
- Existing staging qualification before promotion; digest-bound bytes, release
  checks and independent public receiving after promotion.
- No force/overwrite addition, retry bypass, secret change, package rebuild or
  activation of a suspended release route.
- No runtime API, optional engine, scientific criterion, dependency floor or
  synchronized support-guide change.

## Acceptance and evidence

Inspect the immutable root action, promotion action, shared coordinate helpers
and relevant provider tests. Exercise the provider's adopted operations against
offline fixtures without registry credentials or writes. Execute the local
publication/ABI3/route guards, dependency and publication-contract checks, Ruff
and developer-guide validation. Keep fixture evidence separate from real
builds, installed scientific qualification and registry publication.

Record the exact reviewed consumer/provider source, four affected operations,
source hashes, executed commands and results. Confirm owner review and adopted
commit on #544 after integration, then close it in the maintainer's ordered
sequence. Earlier source preparation does not close #544 before #428.

## Provenance and remaining work

Review begins from consumer `3f6a5f4ec` with the existing Linux/Python 3.14
development interpreter. Provider source is read from the immutable published
commit through an isolated snapshot; its active checkout remains untouched.
The main worktree's four human autosummary edits are preserved.

## Executed owner source review — 2026-11-06

The four active calls now use the immutable v2.3.0 source: staging build/upload,
direct release build/upload, the upload-disabled ABI3 experiment and exact-file
promotion. For each call, an independent inspection compares actual supplied
inputs with the exact provider declaration and required fields. It confirms
that all conversion selectors remain off, native `.conda` output remains
selected and producer/receipt outputs still exist. Parsing and comparing all
three affected workflows with the source base, after accounting for only the
four provider-reference replacements, proves their other semantics unchanged.
This includes triggers, platform fan-out, runtime environments, gate order,
candidate/digest bindings, recipe arguments and evidence retention.

**Contract-tested:** 54 local publication, ABI3, route, dependency and
artifact-validation cases pass in 3.46 s with four workers, Pytest Receptor and
no omissions. The existing direct-route tests still refuse occupied or
uncertain registry coordinates and the promotion guard checks that installed
qualification precedes the exact label operation. Their pin expectations now
name the reviewed immutable provider; other assertions are retained.

The exact provider snapshot passes **29 adopted-operation tests in 4.38 s**,
without omissions, using the existing Python 3.14.7 interpreter and cached
Anaconda client 1.14.1 payload. No environment is created and no package is
installed. The selection exercises active/base Conda executable resolution,
build/conversion failure propagation, `.conda` discovery without conversion,
rejection before unsupported conversion, digest-bound simulated label changes,
exact-upload failure/no-retry behavior, login-shell client selection and producer
event inventories. Its registry and Conda transports are fixtures: these are
not real compilation, installed-package or public-promotion observations.
Withdrawal is outside scope and is not selected.
The native JUnit suite header counts 35 passes while serializing the same 29
method cases counted by the receptor; six executed unittest subtest contexts
account for the difference. The receipt preserves both counts and the unchanged
XML digest rather than forcing them to agree.

The actual already-called publication checker at
`2a63a15d67d2e72724b6349e89f9f026b25e860f` passes. The already-called
`policy-v1.5.9` checker, resolved to
`3116b7d9f1fa9ba4d09b81a8f24a22b749805f9f`, also passes with its existing
guide-content delegation. These checks execute from frozen snapshots; the
active MolSysSuite checkout, which is behind its remote, is not updated or
used as a substitute policy. The dependency-contract audit, developer-guide
and index validation, whole-checkout Ruff lint and formatting also pass
(4,437 formatted Python files). The initial selected format check found one
line-break correction in an updated assertion; the final whole-checkout checks
pass after that correction.

The [receiving receipt](../../devtools/data/conda_provider_owner_receiving_544_20261106.json)
retains source hashes, exact operations, input names, commands, results and
administrative limits. ArgDigest, DepDigest, SMonitor, PyUnitWizard and Ackredit
applicability is recorded without adding unused runtime machinery to workflow
metadata. No provider checkout, historical receipt, staged/public archive,
release route or synchronized guide is modified.

Remaining: integrate the reviewed owner source after the earlier ordered work,
publish the final **Review completed** adoption reference and close #544 in
order. Source review does not authorize a build, registry write or promotion,
and those future operations retain their exact-candidate gates.
