---
summary: PDBFixer file and text constructors bypass optional dependency guards
issue: uibcdf/molsysmt#625
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: medium
verification: reproduced
area: [form, deps]
guard: tests/form/pdbfixer_PDBFixer/test_dependency_boundaries.py
normative:
blocked_by: []
supersedes: []
---

# Guarding optional PDBFixer constructor routes

**Reported:** 2026-11-06 during the #524 optional-provider audit under #334.
**Status:** Implemented and locally received; public delivery and board closeout follow.

## What

With PDBFixer unavailable, public `msm.convert(pdb_file, to_form="pdbfixer.PDBFixer")`
and the equivalent raw-PDB-text conversion raise ModuleNotFoundError from an
actual import. Direct calls, including trusted digestion bypass, behave the same.
The native MolSys constructor route instead correctly raises the catalog-backed
LibraryNotFoundError. Native file/text conversion continues to return the
fixture's 304 atoms and 20 groups without PDBFixer.

## How

The file and string constructor adapters lazily import the optional provider,
but omit its execution-time DepDigest guard. Adapter loading is not availability
validation. Reuse `@dep_digest("pdbfixer")` at both constructor boundaries;
do not catch arbitrary import exceptions or invent a replacement checker.

## Why

Clients relying on MolSysMT's typed installation diagnostics receive a raw import
error on otherwise equivalent inputs. Keep availability, input validation and
provider execution distinct: an absent optional engine must fail before import,
while an installed engine's unrelated transitive failure must retain its cause.

## Evidence and exclusions

The plain-Python probe models absence through actual DepDigest discovery plus
an import blocker, retaining native-only and already guarded native controls.
The ignored receipt is `524-pdbfixer-absence-probe.json`. It restores discovery,
imports and availability caches; it does not uninstall or replace a package.
This is not a transitive-closure, provider-version or scientific qualification.
No native parser, preparation method, automatic fallback or public signature is changed.

## Acceptance criteria

- Both public file/text conversions and direct constructor calls raise the existing
  LibraryNotFoundError before a provider import when PDBFixer is absent.
- Trusted digestion bypass does not bypass dependency availability.
- Native-only conversion remains usable and unrelated import failures are not
  relabeled as missing PDBFixer.
- Present-provider construction, focused guards and affected documentation pass.
- Publish and independently receive the source, record and addressable guard
  before board closure. The broader #524 provider review remains separate.

## Provenance

Linux x86_64, development Python 3.14.7; original source add779264 with an installed
PDBFixer 1.12.0 availability model. No environment or native backend was modified.

## Resolution — 2026-11-06

Source `80590ef769cf9336b9f4fd45f452b453f1fe72c0`.

Both constructors retain ArgDigest and now use the existing DepDigest guard
before their lazy provider imports. The maintained guard exercises public and
direct file/text calls with both digestion policies: absence raises the catalog
LibraryNotFoundError without importing PDBFixer; unrelated ImportError and
ModuleNotFoundError retain their original exception identity. Native-only
conversion keeps all 38 structures and 304 atoms without the optional provider.

The ordinary Python 3.14 receiving keeps the default SMonitor pytest bridge
and passes all 26 boundary cases, present-provider contract tests and both
constructor doctests. These are included in a 1,062-case joint selection with
1,060 passes and two invalid new legacy-dictionary fixture labels; after
correcting only that fixture, all four of its cases pass. No production change
was made to satisfy those fixture errors. The original agent attempts
unnecessarily disabled the SMonitor bridge; they remain attempts, not ordinary-
bridge qualification. An initial 38-vs-one-structure fixture error and a Path-vs-
str constructor doctest error are retained explicitly in the receipt.

The form overview documents absence and transitive-import behavior. Course and
Cookbook review found no contradictory example. Notebook code, outputs, cell
IDs, order and metadata are preserved. This repairs dependency diagnostics;
it does not qualify the provider's version floor or scientific preparation.

The shared [receiving receipt](../../../devtools/data/openmm_runtime_receiving_524_20261106.json)
retains commands, native exits, actual artifacts/import origins, original failed
attempts and documentation preservation. No shared environment or native backend
is replaced; no installed MolSysMT artifact, Viewer pair or release is qualified.
