---
summary: Review temporary-resource ownership and tool lifecycle.
issue: uibcdf/molsysmt#371
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [tests, governance]
guard:
normative: devguide/temporary_resource_operations.md
blocked_by: []
supersedes: []
---

# Temporary-resource owner review

**Reported:** 2026-10-10 by uibcdf/molsyssuite#104.
**Status:** Owner disposition recorded; bounded implementation and retrospective
closeout debt remain explicitly assigned. This is not universal compliance.

## What

Complete the component-owned review beyond the previously repaired Conda helpers,
including development/test/docs/build/qualification operations and retained resources.
The synchronized guide alone does not establish actual cleanup behavior.

## How

The [operating contract](../../temporary_resource_operations.md) records current
ownership, failure handling, caller custody and closeout. The
[dated receipt](../../evidence/temporary_resource_owner_review_20261010.json)
identifies reviewed source bytes, inventory scope, executed cases and dispositions.

Static allocation discovery inventories **57 call sites in 51 Python files**,
supplemented by the Bash LEaP check and workflow/docs/output review. That inventory
enumerates recognizable calls; it is not a gate certifying lifecycle correctness.
Grouped source inspection covers managed contexts, file/reader closure, returned
paths, receipt destinations, child/process lifetime and selected failure boundaries.

Two independently reproduced themes are repaired under uibcdf/molsysmt#372 and
uibcdf/molsysmt#373. Legacy optional-file/native-probe exceptions remain assigned
to dprada/LMMV in uibcdf/molsysmt#374, with interim process-scratch custody,
review date and executed-guard removal conditions. Review occurs on 2026-10-24
or before the next affected invocation.

## Why

Developers need to know who may retire a resource and whether an operation failed.
Tests must protect caller files rather than merely check for a context-manager name.
The component review supplies this disposition without changing shared policy,
rebuilding candidates or invoking a universal scientific/platform matrix.

## What is measured and what is assumed

On original source `70d1400b9514904fbf9b1a5ca126ddf4591e63dc`, the initial
memmap/developer-check selection has **7 failed, 7 passed**; the LEaP runtime
selection has **5 failed, 11 passed**. Both use controlled owned resources.
The repaired resource scope passes **30 cases**. The expanded selected heavy-result,
peptide, LEaP, environment-helper, archive and peptide-doctest scope passes
**278 tests** in twelve workers. Twenty-two warnings concern legacy H5MSM data;
one intentional memory-pressure control warns about its tiny configured budget.
Two strict docstring renders pass without RST warnings; four Python warnings
concern upstream Sphinx deprecations.

Top-level read-only name/uid metadata identifies **1,121 possible local resources**.
Names, uid and directory stat sizes do not establish task ownership or disk usage.
The complete local metadata snapshot is retained for explicit attribution; no
matching path is deleted by that inventory. Ten explicitly created task receipts
were observed at **51,620 bytes** before the review/fast-gate receipts were added;
they remain useful repair and paused-release evidence, with dprada/LMMV as owners.

Retrospective attribution and release closeout remain owned by
uibcdf/molsysmt#334, reviewed on 2026-10-24 or publication resume. Preserve all
unattributed, active, human and other-session resources until individual custody
is established. No bulk prefix/age rule is authorized. The upstream report that
55 registered historical paths are absent is separate evidence; this review does
not identify the actor or certify historical deletion on another host.

## What was refuted

An EXIT trap does not protect a caller when a child writes outside scratch.
Successful cleanup does not establish failure cleanup. Finalization and source
inspection do not replace executed library/platform lifetime evidence. A local
file in a temporary location can be a caller result or required release evidence.

## Scope and exclusions

The owner review, selected repairs and explicit outstanding dispositions are
complete. Complete all-tool/all-platform cleanup, optional legacy bridge behavior,
historical disposal attribution and resumed release qualification are not claimed.
The primary checkout, shared environment and frozen artifacts/refs are preserved.

## Acceptance criteria and resolution

The normative owner contract identifies lifecycle and custody rules; repaired
operations have independent failing-before/passing-after guards. Remaining
implementation exceptions and retained resources have named owners, review dates,
interim procedures and removal conditions. Central coordination receives this
bounded outcome under uibcdf/molsyssuite#104; it stays open for other components.

## Provenance and reproduction

Linux, development Python 3.14.7 / NumPy 2.4.6, 2026-10-10. The receipt holds
hashes of the actual reviewed executable files and guards. Main and its upstream
were clean/aligned at the original source checkpoint before development.

```bash
python -m pytest --receptor=llm -n 12 \
  tests/heavy tests/build/build_peptide tests/third_party/tleap/test_tleap.py \
  devtools/tests/test_tleap_check.py devtools/tests/test_conda_env_helpers.py \
  devtools/tests/test_development_archives.py \
  molsysmt/build/build_peptide.py --doctest-modules
python -m pytest --receptor=llm \
  devtools/tests/test_public_api_docs.py::test_resource_lifecycle_docstrings_render_without_rst_errors
```

User Guide, Cookbook and affected course prose describe the updated behavior;
existing notebook code, execution metadata and saved outputs are unchanged.

Final selected regressions pass 278 cases, both strict docstring renders pass,
and all 14 fast gates pass. Ruff, Bash syntax and parent-signature comparison
also pass. These are local source checks, not installed-package qualification.
