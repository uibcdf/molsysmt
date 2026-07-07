# Proposal: Non-blocking execution for heavy addon operations

**Scope:** `molsysviewer_molsysmt` (the addon shipped from the `molsysmt` repo),
with a small touch point in the MolSysViewer panel-widget base if needed.
Follow-up to the addon telemetry work (the slow-signal instrumentation is the
*diagnostic*; this is the *fix*).

## Pending validation: slow-signal end-to-end (ops / manual)

The addon's `@signal` slow-signal instrumentation is verified analytically and via
console output, but there is no automated test (SMonitor's slow-signal buffer needs
a configured handler). Confirm end-to-end by running with a SMonitor handler and
`SMONITOR_SLOW_SIGNAL_MS` set, on a large system. Opportunistic; carried over from
the (now-removed) MolSysViewer editing-move handoff note.

## Summary

Heavy addon panel operations — energy minimization, contacts, hydrogen bonds,
build (solvate / add hydrogens), PBC transforms, structure analyses — run
**synchronously in the Jupyter kernel thread**. On a large system they freeze the
notebook and the viewer, with no feedback. This proposal makes those operations
**non-blocking above an `n_atoms` threshold**: run the compute on a worker
thread, show progress in the panel, apply the result back on the main thread, and
allow cancellation.

## Problem

The panel action path is fully synchronous. `MolSysMTMechanicsPanel.handle_action`
is representative:

```python
self.set_state({"status": "running"})          # (1) queue a "running" state
result = minimize_energy(view, platform=...)    # (2) BLOCKS the kernel thread
view.set_coordinates(result.coordinates)        # (3) apply result + send messages
self.set_state({"status": "done", ...})         # (4) queue "done"
```

Two concrete failures on large systems:

1. **The kernel freezes.** Step (2) blocks the single kernel thread; the notebook
   is unresponsive and the viewer cannot even repaint until `handle_action`
   returns.
2. **The "running" spinner never shows.** `set_state` (see *Grounding*) writes to
   the `view.widget.addon_states` traitlet. Traitlet/comm updates flush to the
   frontend only when control returns to the kernel event loop — but step (2)
   holds that thread. So the state set in (1) does not reach the UI until *after*
   the compute finishes. The user sees a frozen cell, then a sudden "done".

The telemetry work already added `SMONITOR-SIGNAL-SLOW` signals that *report*
this after the fact; they do not fix the blocking.

## Grounding (verified 2026-07-06)

- Every panel dispatches from `handle_action(self, view, action_id, payload)`
  (the base `AddonPanelWidget.handle_action`, `molsysviewer/addons.py`), executed
  on the kernel's main thread when a panel button message arrives.
- `AddonPanelWidget.set_state(updates)` merges into the
  `view.widget.addon_states` traitlet (`addons.py:95-104`); `push_state` /
  `send` push comm messages to the panel JS. All of this depends on the event
  loop being free to flush.
- The heavy compute lives in adapter functions that take `view` and return a
  result the panel then applies: `minimize_energy` (→ `view.set_coordinates`),
  `run_build_operation` (→ `runtime.basic.add` / `view.load`), `contact_pairs`,
  `buch_hbond_links`, `transform_pbc`, `rmsd`/`rmsf`/`pca` (→ shapes / panel
  state).
- Result application mutates viewer-owned state (regions, colors, shapes,
  `apply_system_edit`, message history) — **not thread-safe**.
- Threading precedent exists but is unrelated: `core.py` runs a
  `threading.Thread(daemon=True)` for the headless-export HTTP server
  (`core.py:2037`), with no callback into kernel/UI state.

## Design

Split each heavy action into **compute (off-thread)** and **apply (main thread)**,
gated by system size.

### 1. Size gate

An addon-local `n_atoms` threshold decides sync vs async per operation:

```python
if n_atoms >= ASYNC_ATOM_THRESHOLD:   # addon-owned config, e.g. 20_000
    run_async(...)
else:
    run_sync(...)                     # today's path, unchanged
```

This threshold is **addon-local and per-operation**; it is *not* the global
`SMONITOR_SLOW_SIGNAL_MS` (that knob was intentionally dropped as an addon
concern). Small systems keep the current simple synchronous path.

### 2. Compute on a worker thread

Run the pure adapter compute (`minimize_energy`, `contact_pairs`, …) in a
`threading.Thread` / a single-worker executor. MolSysMT's heavy kernels are
largely native/Numba and release the GIL, so a worker thread genuinely unblocks
the kernel event loop (so the "running" spinner and progress now flush).

### 3. Progress + state to the panel

While computing, the worker reports progress by updating panel state. Because
comm/traitlet writes should originate where the event loop can flush them,
schedule UI updates on the kernel's IOloop rather than writing traitlets straight
from the worker:

```python
loop = asyncio.get_event_loop()  # or IPython kernel loop
loop.call_soon_threadsafe(lambda: self.set_state({"progress": pct}))
```

Fine-grained progress may not be available from every MolSysMT verb; the MVP can
show an indeterminate spinner (start/stop) and upgrade to real percentages where
the verb exposes callbacks.

### 4. Apply the result on the main thread

The result application (`set_coordinates`, `apply_system_edit`,
`runtime.basic.add`, `view.shapes.*`) **must run on the main thread**, because it
mutates non-thread-safe viewer state and emits ordered frontend messages. The
worker only produces the result object; a main-thread callback applies it and
sets the final `done` state.

### 5. Cancellation

A per-panel cancel token lets the user abort a long run. MolSysMT verbs that
cannot be interrupted mid-call limit cancellation to "ignore the result when it
returns"; verbs that support a callback can check the token and stop early.

### 6. Errors

Keep the existing funnel: failures go through `panel_error_state` /
`emit_panel_exception` (already `context_extra`-shaped), just invoked from the
main-thread completion callback.

## Graduated scope

- **MVP (low risk, high value):** indeterminate spinner that actually renders —
  worker-thread compute + main-thread apply, no real percentage, no cancel.
  Solves the freeze and the invisible-spinner bug.
- **v2:** cancellation token.
- **v3:** true progress percentages where the verb supports callbacks; automatic
  async gating tuned per operation.

## Risks and hard parts

- **Thread-safety of viewer state** — enforced by the compute/apply split; apply
  is main-thread only. Needs a clear rule and review of each adapter's result
  application.
- **Comm from threads** — use `call_soon_threadsafe` (or the kernel's scheduling)
  rather than writing traitlets directly from the worker.
- **GIL / true parallelism** — depends on the MolSysMT verb releasing the GIL;
  verify per operation. Pure-Python verbs will still block somewhat.
- **Kernel lifecycle** — daemon threads must not outlive the cell/kernel in a way
  that corrupts state; guard against applying a result after the view/widget is
  gone.
- **Re-entrancy** — disable the panel's action buttons while a run is in flight;
  decide policy for overlapping actions.
- **Message ordering** — the async result's frontend messages must not interleave
  incorrectly with other viewer messages; apply on the main thread preserves
  order.

## Testing and verification

- Unit: the size gate chooses sync vs async by `n_atoms`; the apply callback runs
  on the main thread; errors still route through `panel_error_state`.
- Behavioral: a fake slow adapter confirms the panel reaches `running` (and the
  state is observable) *before* completion, and `done`/`error` afterwards.
- Cancellation: an aborted run leaves the viewer state unchanged.
- Full addon suite stays green; small-system paths are byte-for-byte the current
  synchronous behavior.

## Open questions

- Default `ASYNC_ATOM_THRESHOLD`, and per-operation overrides (minimization is
  heavy at far fewer atoms than a contact map).
- Worker model: a plain `threading.Thread` per action, or a shared single-worker
  executor per view (serializes heavy ops, simpler state reasoning)?
- Where does the async plumbing live — entirely in the addon panels, or does the
  MolSysViewer `AddonPanelWidget` base grow a reusable
  `run_off_thread(compute, apply)` helper so other addons benefit?
- Should the sync path also gain the (now-rendering) spinner for consistency, or
  stay minimal?

## Acceptance criteria

- Heavy panel operations above the threshold run without freezing the kernel; the
  panel shows a live running indicator during the compute.
- Results are applied on the main thread with viewer overlays reconciled exactly
  as in the synchronous path.
- Failures still produce `context_extra` diagnostics and panel error state.
- Small-system operations are unchanged.
