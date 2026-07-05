"""MolSysMT Basic panel — inspect and select through MolSysMT basic verbs."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..access import has_system
from ..adapters.system import system_counts
from ..diagnostics import panel_error_state
from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = {
    n_atoms: null,
    n_residues: null,
    n_chains: null,
    n_frames: null,
    n_selected: null,
    element: "atom",
    status: "idle",
    error: null,
  };

  el.innerHTML = `
    <div class="msmt-panel">
      <div data-molsysviewer-addon-section="molsysmt:basic-inspect">
        <div class="msmt-summary" id="basic-summary">
          <span class="msmt-empty">No molecular system loaded.</span>
        </div>
        <button class="msmt-btn msmt-btn--primary" id="basic-inspect">Inspect</button>
      </div>
      <div data-molsysviewer-addon-section="molsysmt:basic-select">
        <div class="msmt-row">
          <label class="msmt-label">Selection</label>
          <input class="msmt-input" id="basic-query" type="text" value="all" />
        </div>
        <div class="msmt-row">
          <label class="msmt-label">Element</label>
          <select class="msmt-select" id="basic-element">
            <option value="atom">atom</option>
            <option value="group">group</option>
            <option value="chain">chain</option>
            <option value="molecule">molecule</option>
          </select>
        </div>
        <div class="msmt-row msmt-row--gap">
          <button class="msmt-btn msmt-btn--primary" id="basic-select">Select</button>
          <button class="msmt-btn" id="basic-clear">Clear</button>
        </div>
        <div class="msmt-result" id="basic-result"></div>
      </div>
      <div class="msmt-status" id="basic-status"></div>
    </div>
  `;

  const summaryEl = el.querySelector("#basic-summary");
  const inspectBtn = el.querySelector("#basic-inspect");
  const queryEl = el.querySelector("#basic-query");
  const elementEl = el.querySelector("#basic-element");
  const selectBtn = el.querySelector("#basic-select");
  const clearBtn = el.querySelector("#basic-clear");
  const resultEl = el.querySelector("#basic-result");
  const statusEl = el.querySelector("#basic-status");

  function summaryHtml(s) {
    if (s.n_atoms === null && s.n_residues === null) {
      return '<span class="msmt-empty">No molecular system loaded.</span>';
    }
    const rows = [];
    if (s.n_atoms !== null) rows.push(["Atoms", s.n_atoms]);
    if (s.n_residues !== null) rows.push(["Residues", s.n_residues]);
    if (s.n_chains !== null) rows.push(["Chains", s.n_chains]);
    if (s.n_frames !== null) rows.push(["Frames", s.n_frames]);
    return rows.map(([label, val]) =>
      `<div class="msmt-row"><span class="msmt-label">${label}</span><span class="msmt-value">${val}</span></div>`
    ).join("");
  }

  function applyState(s) {
    state = { ...state, ...s };
    summaryEl.innerHTML = summaryHtml(state);
    resultEl.textContent = state.n_selected !== null ? `Selected: ${state.n_selected} ${state.element}(s)` : "";
    const busy = state.status === "inspecting" || state.status === "running";
    inspectBtn.disabled = busy;
    selectBtn.disabled = busy;
    if (state.status === "done") {
      statusEl.textContent = "Done.";
      statusEl.className = "msmt-status msmt-status--ok";
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error;
      statusEl.className = "msmt-status msmt-status--error";
    } else if (busy) {
      statusEl.textContent = "Running...";
      statusEl.className = "msmt-status msmt-status--busy";
    } else {
      statusEl.textContent = "";
      statusEl.className = "msmt-status";
    }
  }

  inspectBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "inspect", payload: {} });
  });
  selectBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "run_selection", payload: {
      selection: queryEl.value,
      element: elementEl.value,
    }});
  });
  clearBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "clear_selection", payload: {} });
  });

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
.msmt-summary { min-height: 36px; display: flex; flex-direction: column; gap: 2px; }
.msmt-empty { font-size: 11px; opacity: 0.5; font-style: italic; }
.msmt-row { display: flex; align-items: center; justify-content: space-between; font-size: 12px; gap: 6px; }
.msmt-row--gap { margin-top: 4px; }
.msmt-label { opacity: 0.8; white-space: nowrap; }
.msmt-value { font-weight: 600; font-family: monospace; }
.msmt-input, .msmt-select { flex: 1; border: 1px solid #ccc; border-radius: 3px; padding: 3px 6px; font-size: 12px; background: #fff; }
.msmt-result { font-size: 12px; font-weight: 600; min-height: 16px; }
.msmt-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; background: #eee; }
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy { opacity: 0.7; }
"""


class MolSysMTBasicPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        runtime = ensure_runtime(view)
        self.set_state(self._build_state(runtime))

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "inspect":
            if not has_system(view):
                self.set_state({**self._build_state(runtime), "status": "error", "error": "No molecular system attached."})
                return
            self.set_state({**self._build_state(runtime), "status": "inspecting"})
            try:
                counts = system_counts(view)
                runtime.n_atoms = counts["n_atoms"]
                runtime.n_residues = counts["n_residues"]
                runtime.n_chains = counts["n_chains"]
                runtime.n_frames = counts["n_frames"]
                record_event(view, "panel_inspect", n_atoms=runtime.n_atoms)
                self.set_state({**self._build_state(runtime), "status": "done"})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="basic", action=action_id, exc=exc))

        elif action_id == "run_selection":
            if not has_system(view):
                self.set_state({**self._build_state(runtime), "status": "error", "error": "No molecular system attached."})
                return
            selection = payload.get("selection", "all")
            element = payload.get("element", "atom")
            self.set_state({**self._build_state(runtime), "status": "running"})
            try:
                result = runtime.show.select(selection=selection, element=element)
                self.set_state({
                    **self._build_state(runtime),
                    "n_selected": result.n_selected,
                    "element": element,
                    "status": "done",
                })
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="basic", action=action_id, exc=exc))

        elif action_id == "clear_selection":
            try:
                runtime.show.clear_selection()
                self.set_state({**self._build_state(runtime), "n_selected": None, "status": "idle"})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="basic", action=action_id, exc=exc))

    @staticmethod
    def _build_state(runtime: Any) -> dict:
        return {
            "n_atoms": runtime.n_atoms,
            "n_residues": runtime.n_residues,
            "n_chains": runtime.n_chains,
            "n_frames": runtime.n_frames,
            "n_selected": None,
            "element": runtime.last_selection_element,
            "status": "idle",
            "error": None,
        }
