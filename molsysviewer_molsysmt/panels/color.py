"""MolSysMT Color panel — color atoms by robust scalar properties."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..access import has_system
from ..diagnostics import panel_error_state
from ..runtime import ensure_runtime


_PROPERTIES = [
    ("charge",                  "group", "Charge"),
    ("mass",                    "group", "Mass"),
    ("atomic_radius",           "atom",  "Atomic radius"),
]

_PALETTES = ["viridis", "plasma", "inferno", "coolwarm", "RdYlBu", "spectral"]


_ESM = """
export function render({ model, el }) {
  const props = """ + str([[p[0], p[2]] for p in _PROPERTIES]) + """;
  const palettes = """ + str(_PALETTES) + """;

  let state = { status: "idle", error: null, property: null };

  el.innerHTML = `
    <div class="msmt-panel">
      <div data-molsysviewer-addon-section="molsysmt:physchem-color">
        <div class="msmt-row">
          <label class="msmt-label">Property</label>
          <select class="msmt-select" id="col-prop">
            ${props.map(([v, l]) => `<option value="${v}">${l}</option>`).join("")}
          </select>
        </div>
        <div class="msmt-row">
          <label class="msmt-label">Palette</label>
          <select class="msmt-select" id="col-palette">
            ${palettes.map(p => `<option value="${p}">${p}</option>`).join("")}
          </select>
        </div>
        <div class="msmt-row msmt-row--gap">
          <button class="msmt-btn msmt-btn--primary" id="col-apply">Apply Color</button>
          <button class="msmt-btn" id="col-reset">Reset</button>
        </div>
      </div>
      <div class="msmt-status" id="col-status"></div>
    </div>
  `;

  const propEl    = el.querySelector("#col-prop");
  const paletteEl = el.querySelector("#col-palette");
  const applyBtn  = el.querySelector("#col-apply");
  const resetBtn  = el.querySelector("#col-reset");
  const statusEl  = el.querySelector("#col-status");

  function applyState(s) {
    state = { ...state, ...s };
    if (state.status === "running") {
      statusEl.textContent = "Computing…";
      statusEl.className = "msmt-status msmt-status--busy";
      applyBtn.disabled = true;
    } else if (state.status === "done") {
      statusEl.textContent = state.property ? `Colored by ${state.property}.` : "Done.";
      statusEl.className = "msmt-status msmt-status--ok";
      applyBtn.disabled = false;
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error;
      statusEl.className = "msmt-status msmt-status--error";
      applyBtn.disabled = false;
    } else {
      statusEl.textContent = "";
      statusEl.className = "msmt-status";
      applyBtn.disabled = false;
    }
  }

  applyBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "apply_color", payload: {
      property: propEl.value,
      palette: paletteEl.value,
    }});
  });

  resetBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "reset_colors", payload: {} });
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
.msmt-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px;
  font-size: 13px;
  font-family: sans-serif;
}
.msmt-row { display: flex; align-items: center; justify-content: space-between; font-size: 12px; gap: 6px; }
.msmt-row--gap { margin-top: 4px; }
.msmt-label { opacity: 0.8; white-space: nowrap; }
.msmt-select {
  flex: 1;
  border: 1px solid #ccc;
  border-radius: 3px;
  padding: 3px 6px;
  font-size: 12px;
  background: #fff;
}
.msmt-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; background: #eee; }
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""

class MolSysMTColorPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.set_state({"status": "idle", "property": None, "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "apply_color":
            if not has_system(view):
                self.set_state({"status": "error", "error": "No molecular system attached."})
                return
            prop = payload.get("property", "charge")
            palette = payload.get("palette", "viridis")
            self.set_state({"status": "running"})
            try:
                result = runtime.show.color_by(prop, palette=palette)
                self.set_state({
                    "status": "done",
                    "property": result.property,
                    "element": result.element,
                    "error": None,
                })
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="physchem", action=action_id, exc=exc))

        elif action_id == "reset_colors":
            try:
                runtime.show.reset_colors()
                self.set_state({"status": "idle", "property": None, "error": None})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="physchem", action=action_id, exc=exc))
