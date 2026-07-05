"""MolSysMT H-Bonds panel — compute and render hydrogen bonds."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..access import has_system
from ..diagnostics import panel_error_state
from ..runtime import ensure_runtime


_ESM = """
export function render({ model, el }) {
  let state = { n_hbonds: null, status: "idle", error: null };

  el.innerHTML = `
    <div class="msmt-panel">
      <div data-molsysviewer-addon-section="molsysmt:hbonds-buch">
        <div class="msmt-section-title">Hydrogen Bonds (Buch)</div>
        <div class="msmt-row">
          <button class="msmt-btn msmt-btn--primary" id="hb-compute">Compute H-Bonds</button>
          <button class="msmt-btn" id="hb-clear">Clear</button>
        </div>
        <div class="msmt-result" id="hb-result"></div>
      </div>
      <div class="msmt-status" id="hb-status"></div>
    </div>
  `;

  const computeBtn = el.querySelector("#hb-compute");
  const clearBtn   = el.querySelector("#hb-clear");
  const resultEl   = el.querySelector("#hb-result");
  const statusEl   = el.querySelector("#hb-status");

  function applyState(s) {
    state = { ...state, ...s };
    if (state.n_hbonds !== null) {
      resultEl.textContent = `H-bonds rendered: ${state.n_hbonds}`;
    } else {
      resultEl.textContent = "";
    }
    if (state.status === "running") {
      statusEl.textContent = "Computing…";
      statusEl.className = "msmt-status msmt-status--busy";
      computeBtn.disabled = true;
    } else if (state.status === "done") {
      statusEl.textContent = "Done.";
      statusEl.className = "msmt-status msmt-status--ok";
      computeBtn.disabled = false;
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error;
      statusEl.className = "msmt-status msmt-status--error";
      computeBtn.disabled = false;
    } else {
      statusEl.textContent = "";
      statusEl.className = "msmt-status";
      computeBtn.disabled = false;
    }
  }

  computeBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_hbonds", payload: {} });
  });
  clearBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "clear_hbonds", payload: {} });
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
.msmt-section-title { font-size: 11px; font-weight: 700; text-transform: uppercase; opacity: 0.6; }
.msmt-row { display: flex; gap: 6px; }
.msmt-result { font-size: 12px; font-weight: 600; min-height: 16px; }
.msmt-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; background: #eee; }
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""


class MolSysMTHBondsPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.set_state({"n_hbonds": None, "status": "idle", "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "compute_hbonds":
            if not has_system(view):
                self.set_state({"status": "error", "error": "No molecular system attached."})
                return
            self.set_state({"status": "running"})
            try:
                result = runtime.show.hbonds()
                self.set_state({"n_hbonds": result.n_hbonds, "status": "done", "error": None})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="hbonds", action=action_id, exc=exc))

        elif action_id == "clear_hbonds":
            try:
                runtime.show.clear_hbonds()
                self.set_state({"n_hbonds": None, "status": "idle", "error": None})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="hbonds", action=action_id, exc=exc))
