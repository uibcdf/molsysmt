---
summary: Receive public ArgDigest 0.17.0 and assess opt-in contract ownership.
issue: uibcdf/molsysmt#428
status: partial
opened: 2026-10-22
closed:
verification: measured
area: [deps, digestion, native]
guard: tests/native/test_inherited_constructors.py
normative:
blocked_by: []
supersedes: []
---

# Public ArgDigest 0.17.0 receiving

## What

Qualify the published ArgDigest 0.17.0 artifact with MolSysMT and assess whether
explicit contract ownership should replace the existing constructor context
introduced for inherited native constructors. Provider delivery and shared
coordination belong to uibcdf/argdigest#40 and uibcdf/molsyssuite#123.

## How

Download public Conda files, verify their SHA-256 and import their unmodified
`site-packages` payloads ahead of editable support-library checkouts, using the
existing development interpreter. Record imported origins and actual versions.
This is an isolated package-payload receiving run, not a Conda solver result,
an installation of the final MolSysMT/Viewer pair or an additional environment.

Exercise native constructors, inheritance, separately decorated overrides,
mixins, alias normalization, unknown-keyword refusal and relevant molecular
queries. Study explicit ownership separately; do not change global ownership
or remove constructor context merely because the new option is available.

## Why

The ordinary development environment resolves editable sibling checkouts.
Passing tests there does not establish compatibility with the published file.
The constructor context currently changes only caller-sensitive count values;
`DigestConfig.contract_owner` selects aliases, standardizers, function/domain
contracts and value digester lookup together. They are not identical changes.

## What is measured and what is assumed

Receiving starts from MolSysMT `fc2936bf9efd198f02f1d195107e5a5e6f62d13b`.
The three pre-existing generated API-stub edits are preserved and are outside
the executable receiving scope. No installed-candidate qualification is assumed.

## What was refuted

An editable version string is insufficient provenance. Adoption of the new
option is not necessary for an already working constructor contract. A global
definition-owner setting would also change ordinary methods and mixins and
therefore requires evidence beyond successful constructor calls.

## Scope and exclusions

This issue owns MolSysMT receiving and its adoption/defer decision. Provider
code, synchronized guide distribution, public dependency floors and release
artifacts remain unchanged unless an independently justified requirement arises.
Guide distribution belongs to uibcdf/molsyssuite#125. Exact final-candidate
qualification and publication remain under uibcdf/molsysmt#334.

## Acceptance criteria

Record exact public files/digests, imports, consumer source, executed commands
and results. Verify inherited/default/explicit counts and genuine refusal paths;
assess override and mixin ownership, and preserve ordinary query semantics.
Document adoption or deferral and retain a durable executable receiving guard.

## Provenance

Linux, Python 3.14.7, existing development interpreter; receiving performed
2026-10-25. The receipt below records the actual public and editable providers.

## Source receiving result — 2026-10-25

**Contract-tested:** the public ArgDigest 0.17.0 `py_0`, SMonitor 0.21.0 `py_2`
and DepDigest 0.15.1 `py_0` Conda payloads pass **1,636 tests in 32.12 seconds**,
using 12 workers and pytest-receptor. No failures or omissions; 98 warnings are
retained (legacy H5MSM, pandas downcasting, deliberately unknown atom names,
incompatible/dropped/off-axis structural attributes and an external dummy box).
The command is:

```bash
# PUBLIC_PAYLOAD_PATH names the three extracted artifact site-packages directories.
PYTHONPATH="$PUBLIC_PAYLOAD_PATH" python -m pytest tests/native \
  tests/_private/argdigest tests/basic/get tests/basic/compare \
  tests/cross_repo/test_smonitor_contracts.py --receptor=llm -n 12
```

The [receiving receipt](../../devtools/data/argdigest_0_17_receiving_20261025.json)
records exact public URLs, independently verified digests, package versions,
actual import origins expressed relative to their owning root, source/guard
identity and JUnit digests. The same final constructor/ownership guard selection
passes 114 cases in 5.22 seconds with the ordinary editable development providers.
That second run is compatibility evidence for the recorded checkouts, not proof
of an older published ArgDigest release: the editable distribution metadata is
stale and its source already exposes the ownership option.

Two draft assertions initially assumed `MolSys.n_atoms` and ndarray-only index
results; the native contract uses `MolSys.topology.n_atoms` or `get(n_atoms=True)`
and can return index lists. A draft mixin also used a method named `read` while
expecting the registered `get` contract. Correcting those test assumptions did
not change production code. An intermediate broader command selected a nonexistent
`tests/basic/info` directory and exited with no tests; the final command above
uses real paths and exercises info through the native-query suite.

Ruff lint/format and developer-guide/index validation pass. All fourteen fast
release gates pass with the same public provider payloads. These inexpensive
checks do not establish full-suite or installed-candidate qualification.

## Ownership decision

Retain `native_constructor` and the current ArgDigest minimum `>=0.13.0`.
Do not enable `contract_owner` globally or remove existing constructor context.
The optional capability is received for study, not required by production code.

The new
[ownership study](../../tests/_private/argdigest/test_contract_ownership_receiving.py)
demonstrates that definition/exact ownership can replace count context on the
three base constructors. Removing context without choosing an owner reproduces
the inherited-count refusal. Independently decorated overrides have their own
definitions and need their own logical ownership declaration; definition mode
does not automatically inherit the base's contract. A mixin assembled under a
runtime query owner can require that runtime key: definition mode changes its
count semantics. Real `basic.get` candidates verify aliases, a standardizer,
function/domain admission and count-value refusal together; unknown constructor
keywords also retain the runtime child diagnostic identity.

The existing context already solves the count problem without changing those
other lookup stages or raising a public dependency floor. No current defect or
measured performance gain justifies a broader pre-1.0 migration. The study is
explicitly skipped when the provider does not expose the optional field; normal
constructor/query guards remain active on every supported provider.

## Remaining acceptance

This report remains **partial**: the exact public payloads were executed from
temporary directories in the existing interpreter. No Conda installation or
clean dependency solve was performed, and MolSysMT itself remains a source
consumer. Therefore this is not the clean installed receiving required by
uibcdf/molsysmt#428 / uibcdf/molsyssuite#123, and does not close either issue.
Finish that evidence through the normal clean installed route, retaining exact
provider identities and actual import origins; it can accompany final candidate
qualification under uibcdf/molsysmt#334. Other platform/interpreter cells and the
MolSysMT/Viewer installed pair remain separate obligations. No provider patch,
guide edit, release, staging upload or dependency-floor change was made.
