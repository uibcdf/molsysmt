"""MolSysMT Select panel — run MolSysMT selections and highlight in viewer."""

from __future__ import annotations

from typing import Any

import numpy as np

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = {
    n_selected: null,
    element: "atom",
    status: "idle",
    error: null,
  };

  el.innerHTML = `
    <div class="msmt-panel">
      <div class="msmt-row">
        <label class="msmt-label">Selection</label>
        <input class="msmt-input" id="sel-query" type="text" placeholder="backbone" value="all" />
      </div>
      <div class="msmt-row">
        <label class="msmt-label">Element</label>
        <select class="msmt-select" id="sel-element">
          <option value="atom">atom</option>
          <option value="group">group (residue)</option>
          <option value="chain">chain</option>
          <option value="molecule">molecule</option>
        </select>
      </div>
      <div class="msmt-row msmt-row--gap">
        <button class="msmt-btn msmt-btn--primary" id="sel-run">Select & Highlight</button>
        <button class="msmt-btn" id="sel-reset">Reset Colors</button>
      </div>
      <div class="msmt-result" id="sel-result"></div>
      <div class="msmt-status" id="sel-status"></div>
    </div>
  `;

  const queryEl   = el.querySelector("#sel-query");
  const elementEl = el.querySelector("#sel-element");
  const runBtn    = el.querySelector("#sel-run");
  const resetBtn  = el.querySelector("#sel-reset");
  const resultEl  = el.querySelector("#sel-result");
  const statusEl  = el.querySelector("#sel-status");

  function applyState(s) {
    state = { ...state, ...s };

    if (state.n_selected !== null) {
      resultEl.textContent = `Selected: ${state.n_selected} ${state.element}(s)`;
    } else {
      resultEl.textContent = "";
    }

    if (state.status === "running") {
      statusEl.textContent = "Running…";
      statusEl.className = "msmt-status msmt-status--busy";
      runBtn.disabled = true;
    } else if (state.status === "done") {
      statusEl.textContent = "Done.";
      statusEl.className = "msmt-status msmt-status--ok";
      runBtn.disabled = false;
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error;
      statusEl.className = "msmt-status msmt-status--error";
      runBtn.disabled = false;
    } else {
      statusEl.textContent = "";
      statusEl.className = "msmt-status";
      runBtn.disabled = false;
    }
  }

  runBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "run_selection", payload: {
      selection: queryEl.value,
      element: elementEl.value,
    }});
  });

  resetBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "reset_colors", payload: {} });
  });

  model.on("msg:custom", (msg) => {
    if (msg?.type === "state") applyState(msg.state);
  });

  applyState(state);
}
"""

_CSS = """
.msmt-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px;
  font-size: 13px;
  font-family: sans-serif;
}
.msmt-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  gap: 6px;
}
.msmt-row--gap { margin-top: 4px; }
.msmt-label { opacity: 0.8; white-space: nowrap; }
.msmt-input, .msmt-select {
  flex: 1;
  border: 1px solid #ccc;
  border-radius: 3px;
  padding: 3px 6px;
  font-size: 12px;
  background: #fff;
}
.msmt-result { font-size: 12px; font-weight: 600; min-height: 16px; }
.msmt-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  background: #eee;
}
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""


class MolSysMTSelectPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.push_state({"n_selected": None, "element": "atom", "status": "idle", "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "run_selection":
            if runtime.molecular_system is None:
                self.push_state({"status": "error", "error": "No molecular system attached."})
                return
            selection = payload.get("selection", "all")
            element = payload.get("element", "atom")
            self.push_state({"status": "running"})
            try:
                import molsysmt as msm

                indices = msm.select(runtime.molecular_system, selection=selection, element=element)
                indices_list = list(map(int, np.asarray(indices).flatten()))
                runtime.last_selection = selection
                runtime.last_selection_element = element
                runtime.last_selection_indices = indices_list

                n_total = msm.get(runtime.molecular_system, **{f"n_{element}s": True}) if element != "group" else \
                          msm.get(runtime.molecular_system, element="group", n_groups=True)
                values = np.zeros(int(n_total), dtype=float)
                values[indices_list] = 1.0
                view.whole.set_color_by_values(
                    values, element=element, palette=["#cccccc", "#e74c3c"]
                )
                record_event(view, "panel_select", n_selected=len(indices_list), element=element)
                self.push_state({
                    "n_selected": len(indices_list),
                    "element": element,
                    "status": "done",
                    "error": None,
                })
            except Exception as exc:
                self.push_state({"status": "error", "error": str(exc)})

        elif action_id == "reset_colors":
            try:
                view.whole.reset_colors()
                self.push_state({"status": "idle", "error": None})
            except Exception as exc:
                self.push_state({"status": "error", "error": str(exc)})
