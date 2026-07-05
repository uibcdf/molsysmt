"""MolSysMT Structure panel — contacts, RMSD, RMSF, PCA."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..access import has_system
from ..adapters.structure import pca
from ..adapters.structure import rmsd
from ..adapters.structure import rmsf
from ..diagnostics import panel_error_state
from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = {
    contacts_n: null,
    rmsd: null,
    rmsf_mean: null,
    pca_variance: null,
    status: "idle",
    error: null,
  };

  el.innerHTML = `
    <div class="msmt-panel">
      <div data-molsysviewer-addon-section="molsysmt:structure-contacts">
        <div class="msmt-section-title">Contacts</div>
        <div class="msmt-row">
          <label class="msmt-label">Threshold (Å)</label>
          <input class="msmt-input" id="st-threshold" type="number" value="12" min="1" max="30" />
        </div>
        <div class="msmt-row msmt-row--gap">
          <button class="msmt-btn msmt-btn--primary" id="st-contacts">Compute Contacts</button>
          <button class="msmt-btn" id="st-clear-contacts">Clear</button>
        </div>
        <div class="msmt-result" id="st-contacts-result"></div>
      </div>

      <div data-molsysviewer-addon-section="molsysmt:structure-rms">
        <div class="msmt-section-title">RMSD / RMSF</div>
        <div class="msmt-row msmt-row--gap">
          <button class="msmt-btn" id="st-rmsd">Compute RMSD</button>
          <button class="msmt-btn" id="st-rmsf">Compute RMSF</button>
        </div>
        <div class="msmt-result" id="st-rmsd-result"></div>
      </div>

      <div data-molsysviewer-addon-section="molsysmt:structure-pca">
        <div class="msmt-section-title">PCA</div>
        <button class="msmt-btn msmt-btn--primary" id="st-pca">Run PCA → Vectors</button>
        <div class="msmt-result" id="st-pca-result"></div>
      </div>

      <div class="msmt-status" id="st-status"></div>
    </div>
  `;

  const thresholdEl      = el.querySelector("#st-threshold");
  const contactsBtn      = el.querySelector("#st-contacts");
  const clearContactsBtn = el.querySelector("#st-clear-contacts");
  const rmsdBtn          = el.querySelector("#st-rmsd");
  const rmsfBtn          = el.querySelector("#st-rmsf");
  const pcaBtn           = el.querySelector("#st-pca");
  const contactsResultEl = el.querySelector("#st-contacts-result");
  const rmsdResultEl     = el.querySelector("#st-rmsd-result");
  const pcaResultEl      = el.querySelector("#st-pca-result");
  const statusEl         = el.querySelector("#st-status");

  function applyState(s) {
    state = { ...state, ...s };
    contactsResultEl.textContent = state.contacts_n !== null ? `Contacts: ${state.contacts_n}` : "";
    if (state.rmsd !== null) rmsdResultEl.textContent = `RMSD: ${state.rmsd.toFixed(3)} nm  |  mean RMSF: ${state.rmsf_mean !== null ? state.rmsf_mean.toFixed(3) : "—"} nm`;
    if (state.pca_variance !== null) pcaResultEl.textContent = `PC1 variance: ${(state.pca_variance * 100).toFixed(1)}%`;

    if (state.status === "running") {
      statusEl.textContent = "Computing…";
      statusEl.className = "msmt-status msmt-status--busy";
    } else if (state.status === "done") {
      statusEl.textContent = "Done.";
      statusEl.className = "msmt-status msmt-status--ok";
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error;
      statusEl.className = "msmt-status msmt-status--error";
    } else {
      statusEl.textContent = "";
      statusEl.className = "msmt-status";
    }
  }

  contactsBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_contacts", payload: { threshold_angstroms: parseFloat(thresholdEl.value) } });
  });
  clearContactsBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "clear_contacts", payload: {} });
  });
  rmsdBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_rmsd", payload: {} });
  });
  rmsfBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_rmsf", payload: {} });
  });
  pcaBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_pca", payload: {} });
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
.msmt-row { display: flex; align-items: center; justify-content: space-between; font-size: 12px; gap: 6px; }
.msmt-row--gap { margin-top: 2px; }
.msmt-label { opacity: 0.8; white-space: nowrap; }
.msmt-input { width: 60px; border: 1px solid #ccc; border-radius: 3px; padding: 3px 6px; font-size: 12px; }
.msmt-result { font-size: 12px; font-weight: 600; min-height: 16px; }
.msmt-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; background: #eee; }
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""


class MolSysMTStructurePanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.set_state({
            "contacts_n": None, "rmsd": None, "rmsf_mean": None,
            "pca_variance": None, "status": "idle", "error": None,
        })

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "clear_contacts":
            try:
                runtime.show.clear_contacts()
                self.set_state({"contacts_n": None, "status": "idle", "error": None})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="structure", action=action_id, exc=exc))
            return

        if not has_system(view):
            self.set_state({"status": "error", "error": "No molecular system attached."})
            return

        self.set_state({"status": "running"})
        try:
            if action_id == "compute_contacts":
                threshold_ang = payload.get("threshold_angstroms", 12.0)
                result = runtime.show.contacts(threshold=f"{threshold_ang} angstroms")
                self.set_state({
                    "contacts_n": result.n_contacts,
                    "status": "done",
                    "error": None,
                })

            elif action_id == "compute_rmsd":
                result = rmsd(view)
                runtime.rmsd_result = result.values
                record_event(view, "panel_rmsd", mean_rmsd=result.mean)
                self.set_state({"rmsd": result.mean, "status": "done", "error": None})

            elif action_id == "compute_rmsf":
                result = rmsf(view)
                runtime.rmsf_result = result.values
                record_event(view, "panel_rmsf", mean_rmsf=result.mean)
                self.set_state({"rmsf_mean": result.mean, "status": "done", "error": None})

            elif action_id == "compute_pca":
                result = pca(view)
                runtime.pca_result = (result.principal_components, result.variances)
                view.shapes.add_displacement_vectors(
                    origins=None,
                    vectors=result.pc1_vectors,
                    atom_indices=result.atom_indices,
                    tag="msmt-pca-pc1",
                )
                record_event(view, "panel_pca", pc1_variance=result.pc1_variance)
                self.set_state({"pca_variance": result.pc1_variance, "status": "done", "error": None})

        except Exception as exc:
            self.set_state(panel_error_state(view, panel="structure", action=action_id, exc=exc))
