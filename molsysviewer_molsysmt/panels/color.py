"""MolSysMT Color panel — color atoms by physchem properties, RMSF, or SS."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_PROPERTIES = [
    ("charge",                  "group", "Charge"),
    ("hydrophobicity",          "group", "Hydrophobicity"),
    ("sasa",                    "group", "SASA"),
    ("mass",                    "group", "Mass"),
    ("polarity",                "group", "Polarity"),
    ("buried_fraction",         "group", "Buried fraction"),
    ("transmembrane_tendency",  "group", "Transmembrane tendency"),
    ("atomic_radius",           "atom",  "Atomic radius"),
    ("rmsf",                    "atom",  "RMSF"),
    ("secondary_structure",     "group", "Secondary structure"),
    ("b_factor",                "atom",  "B-factor"),
]

_PALETTES = ["viridis", "plasma", "inferno", "coolwarm", "RdYlBu", "spectral"]


_ESM = """
export function render({ model, el }) {
  const props = """ + str([[p[0], p[2]] for p in _PROPERTIES]) + """;
  const palettes = """ + str(_PALETTES) + """;

  let state = { status: "idle", error: null, property: null };

  el.innerHTML = `
    <div class="msmt-panel">
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

_PROPERTY_ELEMENT = {p[0]: p[1] for p in _PROPERTIES}


class MolSysMTColorPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.push_state({"status": "idle", "property": None, "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "apply_color":
            if runtime.molecular_system is None:
                self.push_state({"status": "error", "error": "No molecular system attached."})
                return
            prop = payload.get("property", "charge")
            palette = payload.get("palette", "viridis")
            self.push_state({"status": "running"})
            try:
                values = _compute_property(runtime.molecular_system, prop)
                element = _PROPERTY_ELEMENT.get(prop, "group")
                view.whole.set_color_by_values(values, element=element, palette=palette)
                runtime.last_color_property = prop
                runtime.last_color_element = element
                runtime.last_color_palette = palette
                record_event(view, "panel_color", property=prop)
                self.push_state({"status": "done", "property": prop, "error": None})
            except Exception as exc:
                self.push_state({"status": "error", "error": str(exc)})

        elif action_id == "reset_colors":
            try:
                view.whole.reset_colors()
                self.push_state({"status": "idle", "property": None, "error": None})
            except Exception as exc:
                self.push_state({"status": "error", "error": str(exc)})


def _compute_property(ms: Any, prop: str):
    import molsysmt as msm
    import numpy as np

    if prop == "charge":
        return msm.physchem.get_charge(ms)
    if prop == "hydrophobicity":
        return msm.physchem.get_hydrophobicity(ms)
    if prop == "sasa":
        return msm.physchem.get_sasa(ms)
    if prop == "mass":
        return msm.physchem.get_mass(ms)
    if prop == "polarity":
        return msm.physchem.get_polarity(ms)
    if prop == "buried_fraction":
        return msm.physchem.get_buried_fraction(ms)
    if prop == "transmembrane_tendency":
        return msm.physchem.get_transmembrane_tendency(ms)
    if prop == "atomic_radius":
        return msm.physchem.get_atomic_radius(ms)
    if prop == "rmsf":
        rmsf = msm.structure.get_rmsf(ms)
        return np.asarray(rmsf).flatten()
    if prop == "secondary_structure":
        ss = msm.structure.get_secondary_structure(ms)
        ss_arr = np.asarray(ss).flatten()
        mapping = {"H": 2.0, "E": 1.0, "C": 0.0}
        return np.array([mapping.get(str(s), 0.0) for s in ss_arr])
    if prop == "b_factor":
        return msm.get(ms, b_factor=True)
    raise ValueError(f"Unknown property: {prop!r}")
