---
summary: Actual-Jupyter receiving assumes a global Node executable
issue: uibcdf/molsysmt#767
status: resolved
opened: 2026-11-15
closed: 2026-11-15
severity: high
verification: measured
area: [tests, ci]
guard: tests/molsysviewer_molsysmt/test_jupyter_node_selection.py
normative:
blocked_by: []
supersedes: []
---

# Jupyter receiving assumes a global Node executable

**Reported:** MolSysViewer's original source diagnostic under its #315/#354/#399.
**Status:** resolved in source; causal, wrapper and adjacent diagnostic controls received.

## What

The opt-in pytest guard fails before starting Jupyter because the launcher
selects /usr/bin/node even when the qualified Conda Node is available on PATH.
The owner reproduces the same failure with the real launcher, a controlled
custom-prefix executable and a stop before the server boundary:

```bash
python -m pytest --receptor=llm -n0 tests/molsysviewer_molsysmt/test_jupyter_node_selection.py::test_path_node_is_used_and_recorded_without_a_global_node
```

The original one-case receiving fails with FileNotFoundError. The first correction selection passes 56 cases. The final wrapper/version
and adjacent diagnostic cohort passes 94 cases without skips. A genuine local
Node v24.21.0 version probe and owned-prefix alias resolution also pass; this
is not qualification of that Node version for the consumer's full GUI profile.

## How

The parser hardcodes --node=/usr/bin/node. Its later --version probe and
browser entry both use that value. The pytest wrappers do not pass a CLI
choice, so a valid environment PATH is ignored. This is launcher preparation,
not a failure of a molecular calculation, notebook cycle, Studio save or the
historical MolSysViewer #354 cause.

## Why

The shared receiver must work in the selected Conda/custom-prefix environment,
without global installation or filesystem changes. The required current
consumer guard cannot reach even one cycle with the old default.

## Resolution

Resolve in order: explicit --node, MOLSYSVIEWER_NODE for inherited pytest
wrappers, then node on PATH. Preserve the chosen executable without fallback
when an explicit choice is wrong. Missing/nonexecutable selections fail before
creating output files. The selected version probe is finite (ten seconds),
rejects non-Node output and fails before starting a server; the existing node
version field remains and new node_runtime metadata records selection,
requested name, actual resolved path and version. Both the version probe and
JavaScript entry use that same resolved executable.

Helpers remain private in the receiving script; no molecular/public API,
ArgDigest/DepDigest boundary, environment installation or native code changes.
Tests use controlled filesystem entries and protocol stubs, plus a real Python
binary rejection and a separately recorded actual Node version probe. They do
not claim a browser/kernel/scientific cycle. Existing deadline, ownership and
cleanup assertions remain; unit fixtures make executable selection explicit.

## Acceptance and limits

The original custom-prefix control must fail before the fix and pass after it.
Cover PATH selection without a global Node, CLI/environment priority, spaces,
name/path choices, empty/missing/unusable programs, probe errors/timeouts and
invalid version output. Drive the actual prolonged pytest wrapper to the
selected launcher boundary without starting Jupyter, and preserve metadata,
deadlines and cleanup guards. Actual GUI/hosted one-cycle receiving remains
the consumer's separately authorized work; no full matrix or final artifact
acceptance is inferred.

## Provenance

2026-11-15, existing Linux/Python 3.14.7, parent 08442cb14. The bounded owner
regressions use one CPU/two GiB, no own swap and a monitored 6.5-GiB host
reserve. The original remote attempt remains failed. Commands, native exits,
source fingerprints and selected-executable observations are retained in the
receiving record when completed.

## Receiving record

The [receipt](../../../devtools/data/jupyter_node_selection_receiving_767_20261115.json)
retains the failed original baseline, both positive cohorts, actual selected
binary/version, source fingerprints, limits and cleanup. The isolated custom-
prefix alias is removed; no global link or environment installation occurs.
The public opt-in consumer cycle remains unexecuted here; its previously failed
remote attempt is not rewritten as passing by these source controls.
