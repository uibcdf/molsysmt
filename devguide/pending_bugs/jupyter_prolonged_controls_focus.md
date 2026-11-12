---
summary: Wait for actual controls focus before keyboard navigation in prolonged Jupyter receiving.
issue: uibcdf/molsysmt#718
status: active
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [testing, jupyter, molsysviewer]
guard: tests/molsysviewer_molsysmt/jupyter_receiving_guard.py::test_actual_jupyter_prolonged_popup_controls
normative:
blocked_by: []
supersedes: []
---

# Prolonged receiver control focus

## What

The keyboard helper returns after pressing Enter on the reveal hotspot, before
the actual asynchronous focus transfer. A subsequent `next.focus()` can be
rejected while the controls reverse their hidden transition. Enter then reaches
the hotspot again and does not emit a trajectory step.

Consumer E2 attempt `513` completes three cycles and times out at the fourth
popup's unchanged structure-1 wait. Its trace does not establish event delivery.
Separate actual-Jupyter diagnostic `515` reproduces the failure on its second
hidden-controls trial: Next lacks focus, Enter targets the hotspot, no Next
click occurs and the structure stays at 1. A separately identified positive
control waits for visible keyboard focus and advances both canvases to 2.

## How

The proposed helper waits for a real focused, visible button in the targeted
controls scope. The prolonged receiver first observes fully hidden popup
controls, then verifies Next focus before activation. All original coordinate,
scientific, popup/session and structure checks remain, with their original
timeouts. No fixed sleep, fake reply, retry or corrective seek is introduced.

The explicit GUI pytest guard runs one complete scientific cycle from hidden
controls, including both popups, session recovery and active native playback.
Missing GUI prerequisites fail when the guard is explicitly selected; the file
remains outside the default scientific collection. The complete thirty-cycle
campaign and owner review remain distinct from that one-cycle result.

Kernel import recording now preserves actual molecular/addon/support module
origins, file hashes and module versions, including the compiled extension.
It does not infer a source commit from distribution metadata or one module.
The separate headless guard checks those recorded files against actual imports.
Consumer uibcdf/molsysviewer#364 owns correction of its outer/inner qualification:
the original diagnostic's outer `aee7aa65` label did not identify its copied
kernel source (`0.23.0+757.g08f0afdb8.dirty`). Original reports remain preserved;
that scope cannot be promoted to exact-provider qualification.

## Why

Receiving must activate the intended native control after the UI is ready,
and attribute observations to the provider the kernel actually imports.
Consumer uibcdf/molsysviewer#315 owns the complete E2 campaign; #354, #305
and #356 retain their distinct frame, hosted-menu and lifetime observations.
This contribution changes testing/diagnostics only. No public API, molecular
algorithm, dependency floor, native backend, package or release is changed.

## Source receiving — 2026-11-12

The current-support repeat passes both explicit guards with PyUnitWizard
`0.29.4+2.g9bb4f5f`; a separate 52-case receiver collection and applicable
Ruff, formatting, Node syntax and developer-guide checks pass. The actual
kernel imports and the unchanged 10,180-input envelope are recorded. Scientific
and addon Python bytes match `aee7aa65` (3,169 Git-owned files); receiver changes
are based on `d9c9d4b75`. The extension retains SHA-256 `4ffb82e4…`.
The copied scientific source has no generated version file and reports
`0+unknown`; identity comes from byte comparison, never that version label.

The earlier two-guard pass uses its original PyUnitWizard 0.28.1 overlay and
keeps that separate scope. Counts overlap. The corrected thirty-cycle attempt
is in progress; it is not yet acceptance. Owner integration, changed-head
hosted/installed qualification and postponed human review remain separate.
