"""MolSysMT Build panel — fix missing atoms, bioassembly, mutate, solvate."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = { last_op: null, log: [], status: "idle", error: null };

  el.innerHTML = `
    <div class="msmt-panel">
      <div class="msmt-section-title">Structure Preparation</div>
      <button class="msmt-btn msmt-btn--primary" id="bd-hydrogens">Add Missing Hydrogens</button>
      <button class="msmt-btn msmt-btn--primary" id="bd-bonds">Add Missing Bonds</button>
      <button class="msmt-btn msmt-btn--primary" id="bd-bioassembly">Make Bioassembly</button>

      <div class="msmt-section-title">Solvation</div>
      <button class="msmt-btn" id="bd-solvate">Solvate (water box)</button>

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
      statusEl.textContent = state.last_op ? `Done: ${state.last_op}.` : "Done.";
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
  bondsBtn.addEventListener("click",       () => { model.send({ type: "action", id: "add_bonds",      payload: {} }); });
  bioassemblyBtn.addEventListener("click", () => { model.send({ type: "action", id: "bioassembly",    payload: {} }); });
  solvateBtn.addEventListener("click",     () => { model.send({ type: "action", id: "solvate",        payload: {} }); });

  model.on("msg:custom", (msg) => { if (msg?.type === "state") applyState(msg.state); });

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
        self.push_state({
            "last_op": runtime.last_build_op,
            "log": list(runtime.build_log),
            "status": "idle",
            "error": None,
        })

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if runtime.molecular_system is None:
            self.push_state({"status": "error", "error": "No molecular system attached."})
            return

        self.push_state({"status": "running"})
        try:
            import molsysmt as msm
            ms = runtime.molecular_system

            if action_id == "add_hydrogens":
                new_ms = msm.build.add_missing_hydrogens(ms)
                runtime.molecular_system = new_ms
                runtime.last_build_op = "add_missing_hydrogens"
                runtime.build_log.append("Added missing hydrogens.")
                view.load(new_ms, mode="replace")
                record_event(view, "panel_build", op="add_hydrogens")
                self.push_state({"last_op": "add hydrogens", "log": list(runtime.build_log), "status": "done", "error": None})

            elif action_id == "add_bonds":
                new_ms = msm.build.add_missing_bonds(ms)
                runtime.molecular_system = new_ms
                runtime.last_build_op = "add_missing_bonds"
                runtime.build_log.append("Added missing bonds.")
                view.load(new_ms, mode="replace")
                record_event(view, "panel_build", op="add_bonds")
                self.push_state({"last_op": "add bonds", "log": list(runtime.build_log), "status": "done", "error": None})

            elif action_id == "bioassembly":
                new_ms = msm.build.make_bioassembly(ms)
                runtime.molecular_system = new_ms
                runtime.last_build_op = "make_bioassembly"
                runtime.build_log.append("Biological assembly expanded.")
                view.load(new_ms, mode="replace")
                record_event(view, "panel_build", op="bioassembly")
                self.push_state({"last_op": "make bioassembly", "log": list(runtime.build_log), "status": "done", "error": None})

            elif action_id == "solvate":
                new_ms = msm.build.solvate(ms)
                runtime.molecular_system = new_ms
                runtime.last_build_op = "solvate"
                runtime.build_log.append("System solvated.")
                view.load(new_ms, mode="replace")
                record_event(view, "panel_build", op="solvate")
                self.push_state({"last_op": "solvate", "log": list(runtime.build_log), "status": "done", "error": None})

        except Exception as exc:
            self.push_state({"status": "error", "error": str(exc)})
