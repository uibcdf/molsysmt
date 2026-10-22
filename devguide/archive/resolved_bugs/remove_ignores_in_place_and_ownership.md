---
summary: Resolve the ignored in_place flag and ownership contract of basic.remove
issue: uibcdf/molsysmt#406
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: high
verification: reproduced
area: [basic, extract, api]
guard: tests/basic/test_remove_ownership.py
normative:
blocked_by: []
supersedes: []
---

# Removal mutation and ownership

**Reported:** 2026-10-22 by MolSysViewer while planning recoverable edits.
**Status:** Resolved in source; installed release qualification remains under #334.

## What

`msm.remove` declares `in_place=True` but never reads the flag. It returns an
extracted result for both values, and unrestricted extraction can alias its
source through `copy_if_all=False`. Users cannot rely on either the advertised
mutation flag or independent no-op removal.

## How

Make `in_place=False` the explicit default, preserving the actual return-new
pattern used by existing examples and preparation consumers. This is an
intentional pre-1.0 signature correction, not a compatibility alias. False
returns an independent extraction, including empty/no-op requests. True updates
a native MolSys or standalone Topology/Structures only after a complete candidate
has been prepared, and returns None like `add`. Reject complementary inputs,
foreign forms, attached standalone domains and output conversion for in-place
requests. Keep extraction/remapping in its existing owner rather than duplicate it.

For file/file-handler input, require an explicit non-file target form or a
distinct destination path, including no-op removal. A path or second handle to
the same file cannot be an independent candidate. Reject source paths and hard
links before conversion; no-op file adapters must not silently return the source.

## Why

MolSysViewer needs independent candidate preparation and reliable edit recovery.
`add` already documents True as mutation/None and False as independent return.
Existing removal callers assign the returned system; silently making the old
default actually mutate would break those callers and their original inputs.

## What is measured and what is assumed

Source inspection at `fd5ca01f6c21268707eb7da83760fd5e5a10b75b` confirms the unused
flag and unrestricted alias route. The new runtime guards reproduce ignored
True and aliased no-op False before the repair. Empty structure-index lists also
exposed a float-dtype empty array in the complement helper; it now avoids indexing
the mask when that array is empty. Non-boolean mutation flags exposed an invalid
`values=` keyword in the shared local argument digester; use its existing
ArgumentError contract's `value=` keyword instead of raising TypeError.
No timing or memory improvement is claimed.

## What was refuted

Keeping an ignored flag would preserve the defect. Implementing mutation under
the old default would change the established return-new workflow. Mutating a
domain attached to MolSys without updating other domains would desynchronize axes.
Generic object-dictionary replacement for foreign forms has no supported contract.

## Scope and exclusions

Repair `basic.remove`; native `.remove` methods keep their existing return-new
contract. No general observer or raw-mutation protection (#407), universal
transaction engine, client cache remapping or new file schema is introduced.
The 1.0 publication pause and frozen historical artifact identities remain intact.

In-place preparation retains the original and selected candidate concurrently;
it is not a zero-allocation edit. Publication adopts prepared native domains with
one authority for chemistry and weak ownership rebound to the existing system.
Old domain handles detach, old analysis/query snapshots remain usable, and client
extension attributes survive without remapping client-derived caches.

MolSysDict 0.1 constraints remain explicit: no analysis/mechanics persistence and
integer-readable structure labels. Silent selected reconstruction was repaired
independently in #410. #409 records stale qualification guards. The version-specific
H5MSM-handler diagnostic opportunity remains separate under #411: native handlers
support 0.3/0.4, while public 0.5 loading remains resident. The initially suspected
working native 0.5 handler was disproved and the issue corrected immediately.

## Acceptance criteria

- Reproduce ignored True and aliased no-op False before the repair.
- Guard both modes for atom, structure, combined, empty/no-op and complete removal.
- Preserve source values/ownership on invalid inputs and candidate-preparation
  failure; keep old domains and analysis/query snapshots detached and usable.
- Check named-analysis remapping, parallel observations, evaluated-empty and
  unevaluated structures, units, state assignments, mechanics and persistence.
- Exercise native partial-domain systems and supported out-of-place foreign forms;
  reject unsupported mutation/conversion requests before publication.
- Update docstrings, Foundations, Toolbox, Cookbook, course and signature waiver;
  deliver settled provider evidence to the reporting client.

## Documentation qualification

- Eleven doctest examples pass across `basic.remove` and the selected-dictionary
  converter. Public docstring validation covers 247 public functions; the two
  intentional signature corrections are recorded in the waiver registry.
- The complete updated removal tutorial and shared Common Core module 18 execute
  successfully on temporary copies through `docs/execute_notebooks.py`. Jupyter's
  local sockets require the authorized unsandboxed route; the first sandboxed
  launch failed before executing notebook code. No auxiliary environment was made.
- All thirteen Python blocks in the sparse-interaction recipe and the complete
  MolSysDict example execute. Existing specialized-path removal calls were reviewed:
  their assigned return-new workflow remains valid under the False default.
- A focused Sphinx build renders the five affected User Guide/course pages and
  the two callable docstrings. HTML content checks confirm the new contract.
  Its 74 warnings include unavailable global references and inherited course
  heading/directive styling in the isolated project; this is not a warning-clean
  whole-site qualification. Temporary execution/build outputs are not release files.

## Provenance

2026-10-22, Linux/Python 3.14.7, existing development environment. Source baseline
`fd5ca01f6c21268707eb7da83760fd5e5a10b75b` plus the recorded changes. Local pytest
uses twelve workers and Pytest Receptor. Source checks do not qualify a new
installed package, platform matrix or release pair.

## Resolution

The corrected False default returns independent candidates; explicit True
publishes a prepared native subset and returns None. The existing return-new
native methods stay unchanged. The private native publisher retains target
identity/extension state and rebinds new domains without exposing mismatched
intermediate axes. Old domain owners detach. Disk-backed no-op aliases, invalid
flags and empty complementary structure indices have explicit safe behavior.

Final focused selection: **125 passed**, no omissions, 10.86 seconds, twelve
workers and Pytest Receptor. This includes removal ownership/failure/partial
domains/persistence, selected dictionary conversion, complementary composition,
heavy-atom failure preservation, sparse replacement and flag validation.

The last broad source run executed **5,479 cases: 5,478 passed**, with one failure
in the old allocation comparison recorded and corrected under #412. Its corrected
guard passes in the final focused selection. Broad passing results remain
applicable to the unchanged production code; do not describe that intermediate
run as an all-green full suite. Its 1,049 visible warnings include legacy H5MSM,
deliberate memory budgets, pandas migration, optional engine notices and existing
composition policies. The exact selection was:

```bash
python -m pytest tests/basic tests/native tests/interactions \
    tests/form/molsysmt_MolSys tests/form/molsysmt_Topology \
    tests/form/molsysmt_Structures tests/form/molsysmt_MolSysDict \
    tests/form/file_h5msm tests/build/solvate tests/build/mutate \
    tests/build/remove_overlapping_molecules tests/build/test_reconcile_protonation.py \
    tests/build/add_missing_heavy_atoms --receptor=llm -n 12
```

Ruff passes for the full package and changed tests. All fourteen fast release
gates pass on the final report set. Source
public-signature validation admits exactly the two explained corrections.

Read-only coordination inspection found MolSysViewer at
`d96b073f23247e25cd42c95af545b6d20e7fa982` with twenty local changes, all preserved.
Its inspected removal helpers use the assigned return-new pattern and require no
behavioral migration for the False default. This is not an executed Viewer
qualification. Delivery belongs in #406 and uibcdf/molsysviewer#259; existing
suite adoption remains under uibcdf/molsyssuite#122. No client source, pin, package,
historical artifact, tag or publication state changes.
