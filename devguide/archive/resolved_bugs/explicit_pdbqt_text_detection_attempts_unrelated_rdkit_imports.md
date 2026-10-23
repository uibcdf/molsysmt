---
summary: Explicit PDBQT text detection attempts unrelated RDKit imports
issue: uibcdf/molsysmt#426
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/conversion_truth/test_declared_docking_edges.py::test_docking_routes_do_not_attempt_optional_engine_imports
normative:
blocked_by: []
supersedes: []
---

# Explicit PDBQT text detection attempts unrelated RDKit imports

**Reported:** 2026-10-22, during the SDF/PDBQT execution profile for uibcdf/molsysmt#181.
**Status:** Resolved; generic prefix routing and loader-isolation guards pass.

## What

A native PDBQT text result declares `pdbqt_text:`, but `get_form` sweeps unrelated
string detectors before reaching its adapter. The SMILES detector attempts to
import RDKit. A loader sentinel retaining normal availability lookup observes
that actual import attempt during `file:pdbqt -> string:pdbqt_text` validation.

```bash
python -m pytest tests/conversion_truth/test_declared_docking_edges.py::test_docking_routes_do_not_attempt_optional_engine_imports --receptor=llm
```

The original implementation completes when the sentinel raises ImportError,
but still fails the final no-attempt assertion. Success under a caught import
error does not prove that an unrelated engine was never reached. A broken
installed engine could also fail recognition of unrelated molecular text.

## How

After the existing extension lookup, consult a bounded prefix index derived
from declared string form names. A candidate is always confirmed through the
real registry-backed detector, retaining visibility, overrides and original
failure causes. If confirmation fails, retain the established string/file
fallback. No plugin implements a second dispatch policy, no prefix is accepted
without confirmation and no payload is split or copied to inspect its prefix.

The owning changes are in `basic/get_form.py` and the internal form catalogue.
No SDF/PDBQT parser, chemical assignment or public signature changes.

## Why

An explicitly declared native text form should not load a toolkit used only to
interpret a different representation. This affects dependency isolation and
cold startup, not only a single docking output. The general selective-loading
context remains uibcdf/molsysmt#382; this report owns the concrete tagged-text bug.

## What is measured and what is assumed

The sentinel records real module creation attempts, allows metadata-only
find_spec queries and starts with no selected engine loaded. It then exercises
all 38 SDF/PDBQT witnesses through direct and public routes and checks both
attempts and sys.modules. The blocked engine names are RDKit, MDAnalysis,
MDTraj, OpenMM and Vina. No performance or memory improvement is quantified.

## What was refuted

The first sentinel rejected find_spec itself. That was too strong: checking
availability without loading a provider is allowed. The corrected sentinel
only rejects module creation, and still reproduces the RDKit path through
`string_smiles.is_form`. A format parser dependency is not the cause.

## Scope and exclusions

Retain file-extension priority, adapter confirmation, fallback for unprefixed
strings and dynamic registry behavior. Recognition is not syntax validation:
PDBQT's detector deliberately accepts a declared prefix before parsing. This
change does not certify unprefixed arbitrary text, every optional dependency,
all plugin identities, or scientific chemistry.

## Acceptance criteria

- `tests/basic/test_get_form_prefixes.py` checks selective detection, rejected
  candidate fallback, detector errors, extension priority and bounded inspection.
- The engine sentinel exercises every docking-profile witness without an
  attempted import or loaded selected engine.
- Existing get_form, catalogue and registry integration regressions pass.

## Provenance

Linux x86_64, Python 3.14.7, source baseline
b35a293269884ce6387e60266f3038785603a097, 2026-10-22.

## Resolution and verification

`basic.get_form` retains extension priority, then asks the declared prefix's
registry-backed detector before a general text sweep. The private catalogue
matches bounded prefixes with startswith and does not split payloads. A rejected
candidate retains the old fallback; actual detector errors retain their cause.
The issue guard would fail if an unrelated engine were attempted even when its
ImportError was swallowed and the conversion eventually succeeded.

The complete regression passes **1,015 tests**, zero failures/skips, in
52.00 seconds using 12 workers and Pytest Receptor. It includes all declared
form recognition witnesses, registry override/removal/manual registration,
real SDF/PDBQT inputs and external-reader comparisons. One public get_form
doctest passes; the two affected notebooks execute successfully. This is source
evidence, not an installed-candidate or full scientific certification.

The [receipt](../../../devtools/data/conversion_execution_docking_20261022.json)
retains commands, versions, warnings and scope. No scientific method changes or
Ackredit boundary is introduced. The format parsers and public signatures are
unchanged; the generic dispatch repair is reusable by tagged text consumers.
