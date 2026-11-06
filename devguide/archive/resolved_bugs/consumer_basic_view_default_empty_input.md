---
summary: basic.view rejects its default None input before empty visualization.
issue: uibcdf/molsysmt#578
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [basic, view, argdigest, molsysviewer]
guard: tests/basic/view/test_empty_view_contract.py::test_default_or_explicit_none_creates_empty_workspace
normative:
blocked_by: []
supersedes: []
---

# Default empty input in basic.view

**Status:** open; native contract/digestion discrepancy, separate from the
loaded-primary addon visualization bridge.

## What

`msm.basic.view()` rejects its declared default `molecular_system=None` during normal argument digestion. The same native call with `skip_digestion=True` creates an empty MolSysViewer view.

Please clarify and implement a consistent public empty-input contract. This is reproduced without the MolSysViewer addon; no backend fallback or validation bypass should be added by a consumer.

## How

Published native source `27ccb1b6d640b7e2087a86dea06f6e666dc73fe1`, Linux/Python 3.14.7, with the source MolSysViewer host installed:

```python
import molsysmt as msm

msm.basic.view()
# ArgumentError: Error in argument 'molecular_system' with value 'None'.

empty = msm.basic.view(skip_digestion=True)
assert empty.molsys is None
empty.close()
```

The public `basic.view` signature declares `molecular_system=None`, the docstring lists that default, and the body explicitly skips source selection when the value is None before dispatching to the selected backend. Its MolSysViewer adapter delegates to `new_view`, which can construct an empty workspace.

The normal call fails in `digest_molecular_system` / `_private/molecular_system_validation.py` before backend creation. The observed behavior identifies a contract/digestion inconsistency; it does not establish that every backend supports empty input.

## Why

A native default call behaves differently from its apparent empty-workspace route. Users should not have to disable argument validation to use a valid default. If None is not supported, the public default/help must instead make the required input and failure clear.

Consumer relationship: #421 / PR #543 and uibcdf/molsysviewer#264. The expert bound `basic.view` mirror requires a loaded current primary and can be received independently. It does not silently forward a trusted/bypassed call to compensate for this discrepancy. Ordinary `molsysviewer.new_view()` remains the explicit empty-workspace API.

## Acceptance criteria

- Decide and document whether default/explicit None creates an empty visualization, with any backend-specific limits stated.
- If supported, align normal digestion with the exact public caller rather than broadly accepting None for unrelated scientific functions.
- Add native pytest controls for omitted/explicit None, ordinary loaded inputs, invalid selectors/structure indices, unavailable backends and empty-selector semantics.
- Retain lazy optional-backend imports, native diagnostics and source ownership. Do not require actual browser rendering to test the Python return/lifetime boundary.
- Keep normal and trusted-call behavior consistent for admitted valid inputs; do not recommend `skip_digestion=True` as an end-user workaround.

Record through the existing PR: `devguide/pending_bugs/basic_view_rejects_default_empty_input.md`.


## Scope

The native reproduction uses the recorded source and existing source host.
Other visualization backends and browser rendering were not qualified. The
consumer keeps its loaded-primary admission and does not bypass native digestion.
The native owner decides the supported default and selector/backend semantics.

## Consumer receiving resolution — 2026-11-05

Native owner source 8c2661293 includes the published repair. Receiving retains
this original consumer reproduction alongside the independent owner's report;
neither is deleted or overwritten. The native guard named above passes within
the 362-case directed receiving gate. Addon selection/ownership boundaries are
kept separate from this native correction. See the paired owner report in this
directory for the scientific implementation and detailed native coverage.
