"""MolSysMT Topology panel — bond graph and dihedral quartets."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..access import has_system
from ..adapters.topology import bond_graph_links, dihedral_quartets
from ..diagnostics import panel_error_state
from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = { n_bonds: null, n_dihedrals: null, status: "idle", error: null };

  el.innerHTML = `
    <div class="msmt-panel">
      <div data-molsysviewer-addon-section="molsysmt:topology-bonds">
        <div class="msmt-section-title">Bond Graph</div>
        <div class="msmt-row">
          <button class="msmt-btn msmt-btn--primary" id="tp-bonds">Show Bonds as Links</button>
          <button class="msmt-btn" id="tp-bonds-clear">Clear</button>
        </div>
        <div class="msmt-result" id="tp-bonds-result"></div>
      </div>

      <div data-molsysviewer-addon-section="molsysmt:topology-dihedrals">
        <div class="msmt-section-title">Dihedral Quartets</div>
        <button class="msmt-btn" id="tp-dihedrals">Count Dihedral Quartets</button>
        <div class="msmt-result" id="tp-dih-result"></div>
      </div>

      <div class="msmt-status" id="tp-status"></div>
    </div>
  `;

  const bondsBtn      = el.querySelector("#tp-bonds");
  const bondsClearBtn = el.querySelector("#tp-bonds-clear");
  const dihedralBtn   = el.querySelector("#tp-dihedrals");
  const bondsResultEl = el.querySelector("#tp-bonds-result");
  const dihResultEl   = el.querySelector("#tp-dih-result");
  const statusEl      = el.querySelector("#tp-status");

  function applyState(s) {
    state = { ...state, ...s };
    if (state.n_bonds !== null) bondsResultEl.textContent = `Bonds rendered: ${state.n_bonds}`;
    if (state.n_dihedrals !== null) dihResultEl.textContent = `Dihedral quartets: ${state.n_dihedrals}`;
    if (state.status === "running") {
      statusEl.textContent = "Working…"; statusEl.className = "msmt-status msmt-status--busy";
    } else if (state.status === "done") {
      statusEl.textContent = "Done."; statusEl.className = "msmt-status msmt-status--ok";
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error; statusEl.className = "msmt-status msmt-status--error";
    } else {
      statusEl.textContent = ""; statusEl.className = "msmt-status";
    }
  }

  bondsBtn.addEventListener("click", () => { model.send({ type: "action", id: "show_bonds", payload: {} }); });
  bondsClearBtn.addEventListener("click", () => { model.send({ type: "action", id: "clear_bonds", payload: {} }); });
  dihedralBtn.addEventListener("click", () => { model.send({ type: "action", id: "count_dihedrals", payload: {} }); });

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

_BONDS_TAG = "msmt-topology-bonds"


class MolSysMTTopologyPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.set_state({"n_bonds": None, "n_dihedrals": None, "status": "idle", "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "show_bonds":
            if not has_system(view):
                self.set_state({"status": "error", "error": "No molecular system attached."})
                return
            self.set_state({"status": "running"})
            try:
                result = bond_graph_links(view)
                runtime.bondgraph_result = result.graph
                view.shapes.add_links(atom_pairs=result.atom_pairs, tag=_BONDS_TAG)
                record_event(view, "panel_topology_bonds", n_bonds=result.n_bonds)
                self.set_state({"n_bonds": result.n_bonds, "status": "done", "error": None})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="topology", action=action_id, exc=exc))

        elif action_id == "clear_bonds":
            try:
                view.shapes.clear(tag=_BONDS_TAG)
                self.set_state({"n_bonds": None, "status": "idle", "error": None})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="topology", action=action_id, exc=exc))

        elif action_id == "count_dihedrals":
            if not has_system(view):
                self.set_state({"status": "error", "error": "No molecular system attached."})
                return
            self.set_state({"status": "running"})
            try:
                result = dihedral_quartets(view)
                runtime.dihedral_quartets_result = result.quartets
                record_event(view, "panel_topology_dihedrals", n_dihedrals=result.n_dihedrals)
                self.set_state({"n_dihedrals": result.n_dihedrals, "status": "done", "error": None})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="topology", action=action_id, exc=exc))
