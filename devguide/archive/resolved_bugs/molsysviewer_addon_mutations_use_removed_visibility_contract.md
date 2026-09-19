---
summary: MolSysViewer addon mutations use the removed atom-visibility contract.
issue: uibcdf/molsysmt#207
status: resolved
opened: 2026-09-19
closed: 2026-09-19
severity: high
verification: reproduced
area: [basic]
guard: tests/molsysviewer_molsysmt/test_foundation.py
normative:
blocked_by: []
supersedes: []
---

# MolSysViewer addon mutations use the removed atom-visibility contract

**Reported:** 2026-09-19, by the MolSysViewer development team and reproduced in
the complete local MolSysMT test suite.
**Status:** Resolved; the four mutation paths use the current MolSysViewer edit
contract and are protected by real-view integration tests.

## What

All four live-view operations in `view.addons.molsysmt.basic` fail against current
MolSysViewer. `add()` and `remove()` read the removed
`view.visible_atom_indices` attribute. `set()` and `append_structures()` do the
same and also pass the removed `visible_atom_indices` keyword to
`view.apply_system_edit(...)`.

```bash
$ python -m pytest --receptor=llm -n 12
4 failed, 10206 passed, 11 skipped in 313.62s
```

The four failures all reduce to these obsolete calls, including the build and
context-action tests which reach `add()` and `remove()` through real user flows.

## How

`molsysviewer_molsysmt/runtime.py` retained MolSysViewer's old global atom-mask
contract after MolSysViewer replaced it with viewer-owned whole and region scene
state. Current `MolSysView.apply_system_edit()` performs that state reconciliation
itself. The addon must pass only edit information that MolSysViewer cannot infer:
the old-to-new atom map for removal and the append-block metadata for addition.
Attribute edits and structure appends require no optional arguments.

## Why

MolSysViewer is a hard MolSysMT dependency and this breaks every mutation exposed
by the addon's basic facade. It also breaks higher-level build panels and context
actions that delegate to that facade, so the failure is not confined to a legacy
or private entry point.

## What is measured and what is assumed

Measured before the repair: the complete local suite produced 4 failures, 10,206
passes, and 11 skips with the command shown above. A focused addon and
unit-policy run produced 4 failures and 117 passes.

Measured after the repair: the focused addon and unit-policy run produced 122
passes, and the complete local suite produced 10,211 passes and 11 skips:

```bash
$ python -m pytest --receptor=llm tests/molsysviewer_molsysmt tests/cross_repo/test_unit_policy_authority.py -q
PASS exit=0 | 122 passed | 28.98s | 1 warnings
$ python -m pytest --receptor=llm -n 12
PASS exit=0 | 10211 passed, 11 skipped | 303.72s | 156 warnings
```

Measured: all four failures reproduce with MolSysMT `5cdba1696` and MolSysViewer
`6972c119`.

Assumed: no downstream client intentionally depends on the addon's attempt to
restore the removed, unserialized global visibility mask. Current MolSysViewer
documents whole and region scene state as the replacement contract.

## What was refuted

Mapping the old value to `visible_structure_indices` is not valid: structures and
atoms are different axes and the current edit primitive has no such parameter.
Restoring a compatibility `visible_atom_indices` attribute in MolSysViewer would
preserve a removed state model instead of adapting the client. Dropping every
optional edit argument is also wrong because atom removal still needs its index
map and atom addition still needs load-block accounting.

## Scope and exclusions

This repair covers the four basic-facade mutation paths and their direct
MolSysViewer contract. It does not change MolSysViewer, create a new visibility
layer, or redesign unrelated addon panels.

## Acceptance criteria

- `add()`, `remove()`, `set()`, and `append_structures()` work with current
  MolSysViewer.
- Executable tests verify the exact current `apply_system_edit()` arguments for
  all four paths and their resulting molecular systems.
- Addition retains append-block metadata and removal retains atom-index remapping.
- The focused addon suite and the complete MolSysMT suite pass locally.

All criteria were met on 2026-09-19. The guard file exercises each mutation on
a real `MolSysView`, asserts the exact edit arguments, and checks the resulting
molecular system.

## Dependencies and risks

The repair targets the current MolSysViewer main-line API. Its tests intentionally
exercise a real `MolSysView`, so future host-contract drift will fail at the
integration boundary rather than being hidden behind a mock.

## Provenance

Linux host; Python 3.13; MolSysMT `5cdba1696`; MolSysViewer `6972c119`;
2026-09-19.
