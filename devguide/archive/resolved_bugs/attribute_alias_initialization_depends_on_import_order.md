---
summary: Attribute-alias initialization depends on cold native import order.
issue: uibcdf/molsysmt#535
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: reproduced
area: [argdigest, attribute, tests]
guard: tests/attribute/test_alias_bootstrap.py
normative:
blocked_by: []
supersedes: []
---

# Cold native declaration imports lose an attribute-alias table

**Reported:** MolSysViewer metadata-facade receiving under
uibcdf/molsysviewer#264 and uibcdf/molsysmt#421.
**Status:** consumer declaration-bootstrap cycle repaired; focused, combined and
hosted native/addon receiving pass. Overall candidate qualification remains separate.

## What

Two fresh processes on source 27c6bd3c0b4adfc1b7c3b635b9f30bcf6ffa0cab
call `msm.get(None, atom_names=True, atom_name=False)` after different imports.
Importing the private `attribute_synonyms.TABLES` declaration first yields
UnknownArgumentError. Importing public `attribute.get_argument_aliases` first
yields the intended ArgumentConsistencyError for two names of one argument.
This reproduces the incoming isolated native-test failure; it does not establish
that every ordinary public import order fails.

## How

The normalization declaration imports the public attribute package, whose
initializer also imports a decorated bond-requirement helper. This can initiate
ArgDigest discovery while the declaration module is partially initialized.
The initial cached-partial-discovery hypothesis is now qualified by the
fresh-process regressions and consumer correction below. This does not establish
a separate provider defect or require patching ArgDigest in this repository.

## Why

A broad test run can prime the registry and conceal the missing collision check.
Changing the expected exception, preloading the package or manually translating
keywords in MolSysViewer would not repair the initialization contract.

## Acceptance and boundaries

Add fresh-process coverage for both orders, alias/canonical collisions and
ordinary accepted aliases. Diagnose declaration bootstrap versus shared provider
discovery before choosing the owner of a repair. Keep validation, scope and
function-contract lookup intact. Report a reproduced shared-provider defect to
ArgDigest through its owning issue/contribution route if needed. No provider-source
correction, new dependency floor or consumer workaround belongs to this repair.

## Ownership and correction — 2026-11-03

MolSysMT's alias declarations imported its public attribute package, which also
initializes decorated query helpers. That reentered declaration discovery before
the original normalization module had assigned `TABLES`. A fresh process then
retained incomplete normalization. This is a consumer bootstrap cycle; no claim
of a separate ArgDigest defect or change to that provider is needed for this fix.

The plain attribute catalog moves, byte-for-byte, to the internal
`attribute_catalog` module. Its SHA-256 remains
`f9d7c3257e6d180e4f73c5d845b9b952af4d303237e60aa48d93531a6ab03f84`.
The original public catalog path reexports the same mutable collections and
retains the builder's exact signature and registration behavior. One plain
internal provider constructs defensive copies of the semantic alias contract;
the public `get_argument_aliases()` retains its path, signature and documentation.
Normalization, domain and native-query declarations use the shared data without
importing decorated public helpers. No aliases, scopes or admission rules change.

Deferring public function exports was rejected because it would change package
initialization and same-named function/module behavior. Preloading, clearing the
provider cache or expecting UnknownArgumentError would conceal the incomplete
contract. No lazy-export replacement, registry reset, duplicate store, new
dependency floor or provider source patch is introduced.

## Regression evidence and limits

Eight fresh-process import orders initially produce **two failures / six passes**,
exit 1, 8.08 s: normalization-first imports lose the alias/canonical collision.
An earlier harness omitted `element='atom'` in an accepted atom-name query;
that unrelated unsupported system-level query is corrected before the accepted
red run. The original two-order reproduction remains separately recorded.

After repair, all eight orders and seven existing alias tests pass: **15 tests**,
exit 0, 8.59 s. Coverage is then extended to domain-first initialization, unknown
keyword rejection and registration through the original builder facade. All
nine orders exercise global and element aliases on universal and native get,
collision precedence and public helper callability in unprimed subprocesses.
Processes are independent and no pytest collection state primes their registries.

The combined selection also covers public get/select, native-domain separation
and existing argument digesters: **1,320 passes**, zero skips/failures, exit 0,
63.67 s, 32 warnings. Public signature, docstring and course checks pass. This
is local Linux/Python 3.14.7 source evidence, not a new public package or platform
matrix. Final receiving adds the builder-facade control after that combined run;
its final exact-source evidence is recorded before closure. Raw logs and canonical
receptor streams remain in ignored `.pytest_cache/stabilization-534-535/`.

Final combined receiving includes the original builder-facade registration control
in all nine subprocess orders: **3,866 passes**, zero skips/failures, exit 0,
203.04 s and 745 visible warnings. Receptor evidence is complete and agrees with
JUnit. All 14 fast gates and full Ruff lint/format pass. The signature guard rejects
removing the builder definition even when reexported; retaining its exact wrapper
signature restores the original public source entry point without a gate waiver.
Its registration reaches the same catalog and fresh public alias contract.
The new fresh-process controls are included in both aligned routine smoke commands.

Published source **13f72af2c9630bf768e03b59e2c973d5c6def4f4** contains the repair
and final controls. [Routine CI 41694657220](https://github.com/uibcdf/molsysmt/actions/runs/41694657220)
is cancelled with no executed scientific-job steps when the #503 checkpoint
supersedes it. Its five administrative workflow successes are retained without
claiming the absent scientific execution.

Current source **839709e4adeb754adbb5a9eea0a5eb2fa21d795c** retains this exact
bootstrap correction and guards and adds the independent CIP metadata repair.
[Routine CI 41698204284](https://github.com/uibcdf/molsysmt/actions/runs/41698204284)
completes successfully: **4,530 native passes / 16 optional skips** and
**2,449 addon passes / four optional skips**, each exit 0. All nine cold-process
orders execute, including domain-first loading, accepted global/element aliases,
collision/unknown-keyword rejection and the preserved builder entry point.
Ackredit accounts for 14 native and four addon skips, while unyt and astropy
account for one native skip each; none of the new bootstrap controls is omitted.
The tiers retain 590 and 1,539 warnings. The Conda inventory identifies Python
3.14.10, NumPy 2.5.4 and Pandas 3.1.0; Viewer is fixed to
ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352. GH Run Receptor's final watch exits 0
and agrees with native job 126134233921.

All five applicable source workflows pass: routine smoke 41698204284, devguide
41698204237, Ruff 41698204479, suite policy 41698205147 and publication governance
41698205100. The scoped defect closes on its executed native/addon receiving;
this does not certify a new package, full matrix or installed pair. The cancelled
predecessor remains cancelled. No provider patch, public preload or registry
reset is needed.

## Provenance

2026-11-03, Linux, existing Python 3.14.7 development environment. Both subprocess
probes exit normally after reporting the distinct exception classes. No extra
environment, module-registry priming or native rebuild is used for this probe.
The bounded local receipt is retained under the ignored
`.pytest_cache/stabilization-520-533/534-535-triage.json`.
