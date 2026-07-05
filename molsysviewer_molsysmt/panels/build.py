"""MolSysMT Build panel — fix missing atoms, bioassembly, mutate, solvate."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..access import has_system
from ..adapters.build import run_build_operation
from ..diagnostics import panel_error_state
from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = {
    last_op: null,
    log: [],
    update_mode: null,
    n_added: null,
    mutation_warning: null,
    status: "idle",
    error: null
  };

  el.innerHTML = `
    <div class="msmt-panel">
      <div data-molsysviewer-addon-section="molsysmt:build-preparation">
        <div class="msmt-section-title">Structure Preparation</div>
        <button class="msmt-btn msmt-btn--primary" id="bd-hydrogens">Add Missing Hydrogens</button>
        <button class="msmt-btn msmt-btn--primary" id="bd-bonds">Add Missing Bonds</button>
        <button class="msmt-btn msmt-btn--primary" id="bd-bioassembly">Make Bioassembly</button>
      </div>

      <div data-molsysviewer-addon-section="molsysmt:build-solvation">
        <div class="msmt-section-title">Solvation</div>
        <button class="msmt-btn" id="bd-solvate">Solvate (water box)</button>
      </div>

      <div class="msmt-log" id="bd-log"></div>
      <div class="msmt-status" id="bd-status"></div>
    </div>
  `;

  const hydrogenBtn    = el.querySelector("#bd-hydrogens");
  const bondsBtn       = el.querySelector("#bd-bonds");
  const bioassemblyBtn = el.querySelector("#bd-bioassembly");
  const solvateBtn     = el.querySelector("#bd-solvate");
  const logEl          = el.querySelector("#bd-log");
  const statusEl       = el.querySelector("#bd-status");

  function setButtons(disabled) {
    hydrogenBtn.disabled = disabled;
    bondsBtn.disabled = disabled;
    bioassemblyBtn.disabled = disabled;
    solvateBtn.disabled = disabled;
  }

  function applyState(s) {
    state = { ...state, ...s };
    if (state.log && state.log.length) {
      logEl.innerHTML = state.log.map(l => `<div class="msmt-log-entry">• ${l}</div>`).join("");
    }
    if (state.status === "running") {
      statusEl.textContent = "Working…"; statusEl.className = "msmt-status msmt-status--busy";
      setButtons(true);
    } else if (state.status === "done") {
      const detail = state.mutation_warning ? ` ${state.mutation_warning}` : "";
      statusEl.textContent = state.last_op ? `Done: ${state.last_op}.${detail}` : `Done.${detail}`;
      statusEl.className = "msmt-status msmt-status--ok";
      setButtons(false);
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error; statusEl.className = "msmt-status msmt-status--error";
      setButtons(false);
    } else {
      statusEl.textContent = ""; statusEl.className = "msmt-status"; setButtons(false);
    }
  }

  hydrogenBtn.addEventListener("click",    () => { model.send({ type: "action", id: "add_hydrogens",  payload: {} }); });
  bondsBtn.addEventListener("click",       () => {
    if (!window.confirm("Adding missing bonds may replace the loaded view and reset overlays. Continue?")) return;
    model.send({ type: "action", id: "add_bonds", payload: {} });
  });
  bioassemblyBtn.addEventListener("click", () => {
    if (!window.confirm("Bioassembly may replace the loaded view and reset overlays. Continue?")) return;
    model.send({ type: "action", id: "bioassembly", payload: {} });
  });
  solvateBtn.addEventListener("click",     () => { model.send({ type: "action", id: "solvate",        payload: {} }); });

  function syncModelState() {
    const updates = {};
    Object.keys(state).forEach((key) => {
      const value = model.get(key);
      if (value !== undefined) updates[key] = value;
    });
    applyState(updates);
  }

  Object.keys(state).forEach((key) => {
    model.on(`change:${key}`, (_model, value) => applyState({ [key]: value }));
  });
  syncModelState();


  applyState(state);
}
"""

_CSS = """
.msmt-panel { display: flex; flex-direction: column; gap: 8px; padding: 8px; font-size: 13px; font-family: sans-serif; }
.msmt-section-title { font-size: 11px; font-weight: 700; text-transform: uppercase; opacity: 0.6; margin-top: 4px; }
.msmt-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; background: #eee; width: 100%; text-align: left; }
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-log { font-size: 11px; font-family: monospace; max-height: 80px; overflow-y: auto; background: #f8f8f8; border-radius: 3px; padding: 4px; }
.msmt-log-entry { margin-bottom: 2px; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""


class MolSysMTBuildPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        runtime = ensure_runtime(view)
        self.set_state({
            "last_op": runtime.last_build_op,
            "log": list(runtime.build_log),
            "update_mode": None,
            "n_added": None,
            "mutation_warning": None,
            "status": "idle",
            "error": None,
        })

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if not has_system(view):
            self.set_state({"status": "error", "error": "No molecular system attached."})
            return

        self.set_state({"status": "running"})
        try:
            if action_id in {"add_hydrogens", "add_bonds", "bioassembly", "solvate"}:
                result = run_build_operation(view, action_id)
                runtime.last_build_op = result.operation
                runtime.build_log.append(result.log_message)
                if result.mode == "append":
                    # Overlay-preserving: appends the new atoms and reconciles
                    # regions/selections/colors instead of resetting the viewer.
                    view.add(result.added_system)
                    mutation_warning = "Appended atoms; viewer overlays preserved."
                elif result.mode == "replace":
                    # Restructured system: a full (destructive) reload.
                    view.load(result.molecular_system, mode="replace")
                    mutation_warning = "Replaced system; viewer overlays reset."
                else:
                    mutation_warning = "No structural changes detected."
                # "noop": nothing changed, nothing to apply.
                record_event(view, "panel_build", op=result.operation, mode=result.mode)
                self.set_state({
                    "last_op": result.label,
                    "log": list(runtime.build_log),
                    "update_mode": result.mode,
                    "n_added": result.n_added,
                    "mutation_warning": mutation_warning,
                    "status": "done",
                    "error": None,
                })

        except Exception as exc:
            self.set_state(panel_error_state(view, panel="build", action=action_id, exc=exc))
