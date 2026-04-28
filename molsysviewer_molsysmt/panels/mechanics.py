"""MolSysMT Mechanics panel — forces, potential energy, minimization."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = { energy: null, n_vectors: null, status: "idle", error: null };

  el.innerHTML = `
    <div class="msmt-panel">
      <div class="msmt-section-title">Forces</div>
      <div class="msmt-row">
        <label class="msmt-label">Force field</label>
        <select class="msmt-select" id="mec-ff">
          <option value="AMBER14">AMBER14</option>
          <option value="CHARMM36">CHARMM36</option>
        </select>
      </div>
      <div class="msmt-row msmt-row--gap">
        <button class="msmt-btn msmt-btn--primary" id="mec-forces">Compute Forces → Vectors</button>
        <button class="msmt-btn" id="mec-clear">Clear</button>
      </div>
      <div class="msmt-result" id="mec-forces-result"></div>

      <div class="msmt-section-title">Energy</div>
      <button class="msmt-btn" id="mec-energy">Compute Potential Energy</button>
      <div class="msmt-result" id="mec-energy-result"></div>

      <div class="msmt-section-title">Minimization</div>
      <button class="msmt-btn msmt-btn--warn" id="mec-minimize">Energy Minimize → Reload</button>

      <div class="msmt-status" id="mec-status"></div>
    </div>
  `;

  const ffEl          = el.querySelector("#mec-ff");
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
      statusEl.textContent = "Done."; statusEl.className = "msmt-status msmt-status--ok";
      setButtons(false);
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error; statusEl.className = "msmt-status msmt-status--error";
      setButtons(false);
    } else {
      statusEl.textContent = ""; statusEl.className = "msmt-status"; setButtons(false);
    }
  }

  forcesBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_forces", payload: { forcefield: ffEl.value } });
  });
  clearBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "clear_forces", payload: {} });
  });
  energyBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_energy", payload: { forcefield: ffEl.value } });
  });
  minimizeBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "minimize_energy", payload: { forcefield: ffEl.value } });
  });

  model.on("msg:custom", (msg) => { if (msg?.type === "state") applyState(msg.state); });

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


class MolSysMTMechanicsPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.push_state({"energy": None, "n_vectors": None, "status": "idle", "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if runtime.molecular_system is None:
            self.push_state({"status": "error", "error": "No molecular system attached."})
            return

        self.push_state({"status": "running"})
        try:
            import molsysmt as msm
            import numpy as np
            ms = runtime.molecular_system
            ff = payload.get("forcefield", "AMBER14")

            if action_id == "compute_forces":
                forces = msm.molecular_mechanics.get_forces(ms, forcefield=ff)
                runtime.forces_result = forces
                forces_arr = np.asarray(forces)
                if forces_arr.ndim == 3:
                    forces_arr = forces_arr[0]  # first frame
                view.shapes.add_displacement_vectors(
                    origins=None, vectors=forces_arr,
                    atom_indices=list(range(len(forces_arr))),
                    tag=_FORCES_TAG,
                )
                runtime.forces_tag = _FORCES_TAG
                record_event(view, "panel_forces", n_vectors=len(forces_arr))
                self.push_state({"n_vectors": len(forces_arr), "status": "done", "error": None})

            elif action_id == "clear_forces":
                if runtime.forces_tag:
                    view.shapes.remove(runtime.forces_tag)
                    runtime.forces_tag = None
                self.push_state({"n_vectors": None, "status": "idle", "error": None})

            elif action_id == "compute_energy":
                energy = msm.molecular_mechanics.get_potential_energy(ms, forcefield=ff)
                runtime.energy_result = energy
                energy_val = float(np.asarray(energy).flatten()[0])
                record_event(view, "panel_energy", energy=energy_val)
                self.push_state({"energy": energy_val, "status": "done", "error": None})

            elif action_id == "minimize_energy":
                new_ms = msm.molecular_mechanics.potential_energy_minimization(ms, forcefield=ff)
                runtime.molecular_system = new_ms
                view.load(new_ms, mode="replace")
                record_event(view, "panel_minimize")
                self.push_state({"status": "done", "error": None})

        except Exception as exc:
            self.push_state({"status": "error", "error": str(exc)})
