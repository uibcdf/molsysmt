---
summary: Molecular task panels lose rejected-operation diagnostics during automatic synchronization refresh.
issue: uibcdf/molsysmt#603
status: partial
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [molsysviewer, gui]
guard: tests/molsysviewer_molsysmt/test_geometry_panel.py::test_missing_mass_unit_policy_rejects_before_write_and_can_be_retried
normative:
blocked_by: []
supersedes: []
---

# Molecular task rejection diagnostic lifetime

## What

Automatic synchronized context refresh can erase a legitimate rejected-operation
message in the tools addon. Geometry stays at an updating/empty status even though
the native call has already failed and the molecular system remains unchanged.
System has the same done-only late-reply protocol. This differs from #590's
successful removal completion; both are delivered through PR #543.

## How

Actual JupyterLab/Chromium receiving, Viewer `49dba88ae992088259a6f0891b59dfc8730f5183`,
addon `1e7a4273b905ca020815658f23ba645d40817226` plus the Center task, Python 3.14:
request Center of mass under an explicit partial pm/ps/radians policy lacking a
mass standard. This intentionally exercises native unit validation, not a mass
algorithm defect. The real comm observation records error request 3 (revision 0,
synchronized, “No standard units…”), then empty select replies 4 and 5. The
browser's assertion sees “Molecular data are updating.” Coordinates and target
revision are unchanged. Local sanitized receipt: `/tmp/msv-center-error-repro-20261106/full-failure.json`.
The Jupyter debugger page error is also present in the plain baseline; the
asserted defect concerns the panel's actual state messages and visible status.

## Why

A silent rejection leaves users unable to correct their input and can suggest
that an operation is still running. Keep a bounded display diagnostic across
refreshes of the same task, input, target, revision and structure context.
Clear it on new user work/context or unmount, without retaining exception objects,
molecular arrays or reusable review tokens. Old replies must not override a new
user draft. No scientific replay, fallback units or native validation changes.

## Acceptance

Real native rejection preserves coordinates and synchronization. Shared System
and Geometry tests check refresh retention and expiry on new review, Back,
changed draft/parameters/task, frame, revision and remount. Actual Jupyter comms
must leave the diagnostic visible after a newer synchronized refresh and clear it
on a new user choice. Existing successful completion/results receiving must pass.
Source contribution remains distinct from owner integration, hosted exact-head,
installed packages and postponed human acceptance.


## Source correction and receiving — 2026-11-06

PR #543 now keeps a bounded diagnostic scoped to weak target identity, revision,
sync state, displayed structure and exact task inputs. New actions/context and
unmount expire it. The frontend accepts only current-request replies for the
current draft, so a late completion/error cannot override a newer intent.
No native computation, standard unit or exception propagation contract changes.

114 shared System/Geometry cases pass; 172 native/route/reporting controls pass
separately. Five actual Jupyter scenarios pass in 233.70 s: System (6 steps),
independent results (7), Translate (7), Center (7), and rejection lifetime (5).
The last observes the actual error comm followed by a newer synchronized refresh,
checks visible text and unchanged native data/revision, then changes the user
choice and obtains a fresh review. Source receipt:
[Center receiving](../../devtools/data/molsysviewer_tools_center_receiving_20261106.json).
Owner integration and exact-head hosted qualification remain pending; the issue
stays open rather than declaring the contribution already integrated.
