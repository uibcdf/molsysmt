"""MolSysMT H-Bonds panel — compute and render hydrogen bonds."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = { n_hbonds: null, status: "idle", error: null };

  el.innerHTML = `
    <div class="msmt-panel">
      <div class="msmt-section-title">Hydrogen Bonds (Baker-Hubbard)</div>
      <div class="msmt-row">
        <button class="msmt-btn msmt-btn--primary" id="hb-compute">Compute H-Bonds</button>
        <button class="msmt-btn" id="hb-clear">Clear</button>
      </div>
      <div class="msmt-result" id="hb-result"></div>
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

  model.on("msg:custom", (msg) => {
    if (msg?.type === "state") applyState(msg.state);
  });

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
        self.push_state({"n_hbonds": None, "status": "idle", "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "compute_hbonds":
            if runtime.molecular_system is None:
                self.push_state({"status": "error", "error": "No molecular system attached."})
                return
            self.push_state({"status": "running"})
            try:
                import molsysmt as msm
                import numpy as np

                ms = runtime.molecular_system
                atoms_per_structure, _distances = msm.hbonds.get_buch_hbonds(ms)
                runtime.hbonds_result = atoms_per_structure

                # Build per-structure list of [donor, acceptor] pairs
                structures = []
                total = 0
                for frame_atoms in atoms_per_structure:
                    if frame_atoms is None or len(frame_atoms) == 0:
                        structures.append(None)
                    else:
                        arr = np.asarray(frame_atoms)
                        pairs = [[int(arr[i, 0]), int(arr[i, 2])] for i in range(len(arr))]
                        structures.append(pairs)
                        total += len(pairs)

                tag = "msmt-hbonds"
                view.shapes.links.add_hbonds(structures=structures, tag=tag)
                runtime.hbonds_tag = tag
                record_event(view, "panel_hbonds", n_hbonds=total)
                self.push_state({"n_hbonds": total, "status": "done", "error": None})
            except Exception as exc:
                self.push_state({"status": "error", "error": str(exc)})

        elif action_id == "clear_hbonds":
            try:
                if runtime.hbonds_tag:
                    view.shapes.remove(runtime.hbonds_tag)
                    runtime.hbonds_tag = None
                self.push_state({"n_hbonds": None, "status": "idle", "error": None})
            except Exception as exc:
                self.push_state({"status": "error", "error": str(exc)})
