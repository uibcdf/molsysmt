# A cross-repo test reads a MolSysViewer attribute that no longer exists

**Reported:** 2026-08-07, found by a full-suite run. **Status:** resolved and archived on 2026-08-07. Fixed by option 1 below: both tests now
assert through a public surface instead of a private attribute of another library.

**Severity:** low for the library, medium for the gate. Two tests fail, so the suite is
not clean, and a red suite stops detecting real regressions.

## Symptom

```
tests/molsysviewer_molsysmt/test_foundation.py::test_basic_facade_set_uses_apply_system_edit_on_real_view
tests/molsysviewer_molsysmt/test_foundation.py::test_basic_facade_append_structures_uses_apply_system_edit_on_real_view

AttributeError: 'MolSysView' object has no attribute '_message_history'.
Did you mean: '_shape_history'?
```

Both tests do:

```python
payload_msg = next(msg for msg in view._message_history
                   if msg.get("op") == "load_molsys_payload")
```

## Cause

MolSysViewer no longer keeps a general message history on the view. `molsysviewer/viewer/core.py`
holds `_shape_history`, which tracks shapes rather than every message, and message
bookkeeping moved to `molsysviewer/scene_history.py` with an undo/redo model. The change
landed in the viewer's static-scene and reconnect canonicalization work (`2b504d77`,
`06131cae`, `8956bd62`).

`_shape_history` is **not** a rename of `_message_history`; it is a narrower structure.
Substituting the name would make the tests pass while asserting something else.

## Affected public behavior

None. This is test-only breakage from a private attribute of another library changing
under a test that reached into it.

## Likely fix

Decide what the assertion should observe now. The test wants to confirm that a
`load_molsys_payload` message carried the edited system. Two candidates:

1. Assert through a public surface of MolSysViewer, so the test stops depending on a
   private attribute that is free to change.
2. If a message history is still needed for testing, ask MolSysViewer for a supported
   way to observe it.

Option 1 is preferable: reaching into `_message_history` is what made this fragile.

## Acceptance tests

The two named tests pass, asserting through a surface MolSysViewer supports, and no
MolSysMT test reads an underscore-prefixed attribute of a `MolSysView`.


---

## Resolution

The two tests already intercepted `view.apply_system_edit` and recorded
`(new_molsys, kwargs)`; they asserted on `kwargs` and then ignored `new_molsys`, reaching
into `view._message_history` instead to inspect the message the viewer built from it.

That was the mistake, and the viewer's refactor only exposed it. **What the facade owes
the viewer is an edited molecular system handed to `apply_system_edit`.** Whether the
viewer then serialises it into a `load_molsys_payload` message is the viewer's own
business, and a MolSysMT test had no reason to know. Asserting on the recorded system
tests the contract that actually belongs to this side of the boundary:

```python
edited_molsys = calls[0][0]
assert msm.get(edited_molsys, element="atom", group_name=True)[:5] == ["ACE2"] * 5
```

and, for the append case, `msm.get(edited_molsys, n_structures=True) == 2`.

The substitution `_message_history` -> `_shape_history` was deliberately **not** made:
`_shape_history` tracks shapes rather than every message, so the tests would have passed
while asserting something else.

115 cross-repo tests pass, and the MolSysMT suite is clean again — which matters beyond
this report, since a suite with known failures stops detecting new ones and blocks the
F5 exact-commit gate.
