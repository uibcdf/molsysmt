"""MolSysMT Mechanics panel — forces, potential energy, minimization."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..access import has_system
from ..adapters.molecular_mechanics import compute_forces
from ..adapters.molecular_mechanics import minimize_energy
from ..adapters.molecular_mechanics import potential_energy
from ..diagnostics import panel_error_state
from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = {
    energy: null,
    n_vectors: null,
    update_mode: null,
    mutation_warning: null,
    status: "idle",
    error: null
  };

  el.innerHTML = `
    <div class="msmt-panel">
      <div data-molsysviewer-addon-section="molsysmt:mechanics-forces">
        <div class="msmt-section-title">Forces</div>
        <div class="msmt-row msmt-row--gap">
          <button class="msmt-btn msmt-btn--primary" id="mec-forces">Compute Forces → Vectors</button>
          <button class="msmt-btn" id="mec-clear">Clear</button>
        </div>
        <div class="msmt-result" id="mec-forces-result"></div>
      </div>

      <div data-molsysviewer-addon-section="molsysmt:mechanics-energy">
        <div class="msmt-section-title">Energy</div>
        <div class="msmt-row">
          <label class="msmt-label">Platform</label>
          <select class="msmt-select" id="mec-platform">
            <option value="CPU">CPU</option>
            <option value="Reference">Reference</option>
            <option value="CUDA">CUDA</option>
            <option value="OpenCL">OpenCL</option>
          </select>
        </div>
        <button class="msmt-btn" id="mec-energy">Compute Potential Energy</button>
        <div class="msmt-result" id="mec-energy-result"></div>
      </div>

      <div data-molsysviewer-addon-section="molsysmt:mechanics-minimization">
        <div class="msmt-section-title">Minimization</div>
        <button class="msmt-btn msmt-btn--warn" id="mec-minimize">Energy Minimize → Update Coordinates</button>
      </div>

      <div class="msmt-status" id="mec-status"></div>
    </div>
  `;

  const platformEl    = el.querySelector("#mec-platform");
  const forcesBtn     = el.querySelector("#mec-forces");
  const clearBtn      = el.querySelector("#mec-clear");
  const energyBtn     = el.querySelector("#mec-energy");
  const minimizeBtn   = el.querySelector("#mec-minimize");
  const forcesResEl   = el.querySelector("#mec-forces-result");
  const energyResEl   = el.querySelector("#mec-energy-result");
  const statusEl      = el.querySelector("#mec-status");

  function setButtons(disabled) {
    forcesBtn.disabled = disabled;
    energyBtn.disabled = disabled;
    minimizeBtn.disabled = disabled;
  }

  function applyState(s) {
    state = { ...state, ...s };
    if (state.n_vectors !== null) forcesResEl.textContent = `Force vectors: ${state.n_vectors}`;
    if (state.energy !== null) energyResEl.textContent = `E = ${state.energy.toFixed(3)} kJ/mol`;
    if (state.status === "running") {
      statusEl.textContent = "Computing…"; statusEl.className = "msmt-status msmt-status--busy";
      setButtons(true);
    } else if (state.status === "done") {
      const detail = state.mutation_warning ? ` ${state.mutation_warning}` : "";
      statusEl.textContent = `Done.${detail}`; statusEl.className = "msmt-status msmt-status--ok";
      setButtons(false);
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error; statusEl.className = "msmt-status msmt-status--error";
      setButtons(false);
    } else {
      statusEl.textContent = ""; statusEl.className = "msmt-status"; setButtons(false);
    }
  }

  forcesBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_forces", payload: {} });
  });
  clearBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "clear_forces", payload: {} });
  });
  energyBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_energy", payload: { platform: platformEl.value } });
  });
  minimizeBtn.addEventListener("click", () => {
    if (!window.confirm("Energy minimization updates coordinates in place. Continue?")) return;
    model.send({ type: "action", id: "minimize_energy", payload: { platform: platformEl.value } });
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
.msmt-section-title { font-size: 11px; font-weight: 700; text-transform: uppercase; opacity: 0.6; margin-top: 4px; }
.msmt-row { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
.msmt-row--gap { margin-top: 2px; }
.msmt-label { opacity: 0.8; white-space: nowrap; }
.msmt-select { flex: 1; border: 1px solid #ccc; border-radius: 3px; padding: 3px 6px; font-size: 12px; }
.msmt-result { font-size: 12px; font-weight: 600; min-height: 16px; }
.msmt-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; background: #eee; }
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn--warn { background: #e67e22; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""

_FORCES_TAG = "msmt-mechanics-forces"
_SUPPORTED_PLATFORMS = {"CPU", "Reference", "CUDA", "OpenCL"}


def _platform_from_payload(payload: dict) -> str:
    if "forcefield" in payload:
        raise ValueError("Unsupported molecular-mechanics argument: 'forcefield'")
    platform = payload.get("platform", "CPU")
    if platform not in _SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported OpenMM platform: {platform!r}")
    return platform


class MolSysMTMechanicsPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.set_state({
            "energy": None,
            "n_vectors": None,
            "update_mode": None,
            "mutation_warning": None,
            "status": "idle",
            "error": None,
        })

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "clear_forces":
            try:
                if runtime.forces_tag:
                    view.shapes.clear(tag=runtime.forces_tag)
                    runtime.forces_tag = None
                self.set_state({"n_vectors": None, "status": "idle", "error": None})
            except Exception as exc:
                self.set_state({"status": "error", "error": str(exc)})
            return

        if not has_system(view):
            self.set_state({"status": "error", "error": "No molecular system attached."})
            return

        self.set_state({"status": "running"})
        try:
            platform = _platform_from_payload(payload)

            if action_id == "compute_forces":
                result = compute_forces(view)
                runtime.forces_result = result.forces
                view.shapes.add_displacement_vectors(
                    origins=None,
                    vectors=result.vectors,
                    atom_indices=result.atom_indices,
                    tag=_FORCES_TAG,
                )
                runtime.forces_tag = _FORCES_TAG
                record_event(view, "panel_forces", n_vectors=result.n_vectors)
                self.set_state({"n_vectors": result.n_vectors, "status": "done", "error": None})

            elif action_id == "compute_energy":
                result = potential_energy(view, platform=platform)
                runtime.energy_result = result.energy
                record_event(view, "panel_energy", energy=result.value)
                self.set_state({"energy": result.value, "status": "done", "error": None})

            elif action_id == "minimize_energy":
                result = minimize_energy(view, platform=platform)
                view.set_coordinates(result.coordinates)
                record_event(view, "panel_minimize")
                self.set_state({
                    "update_mode": "coordinates",
                    "mutation_warning": "Coordinates updated in place; viewer overlays preserved.",
                    "status": "done",
                    "error": None,
                })

        except Exception as exc:
            self.set_state(panel_error_state(view, panel="molecular_mechanics", action=action_id, exc=exc))
