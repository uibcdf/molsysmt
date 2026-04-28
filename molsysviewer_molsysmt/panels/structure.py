"""MolSysMT Structure panel — contacts, RMSD, RMSF, PCA."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

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
      <div class="msmt-section-title">Contacts</div>
      <div class="msmt-row">
        <label class="msmt-label">Threshold (Å)</label>
        <input class="msmt-input" id="st-threshold" type="number" value="12" min="1" max="30" />
      </div>
      <button class="msmt-btn msmt-btn--primary" id="st-contacts">Compute Contacts</button>
      <div class="msmt-result" id="st-contacts-result"></div>

      <div class="msmt-section-title">RMSD / RMSF</div>
      <div class="msmt-row msmt-row--gap">
        <button class="msmt-btn" id="st-rmsd">Compute RMSD</button>
        <button class="msmt-btn" id="st-rmsf">Compute RMSF</button>
      </div>
      <div class="msmt-result" id="st-rmsd-result"></div>

      <div class="msmt-section-title">PCA</div>
      <button class="msmt-btn msmt-btn--primary" id="st-pca">Run PCA → Vectors</button>
      <div class="msmt-result" id="st-pca-result"></div>

      <div class="msmt-status" id="st-status"></div>
    </div>
  `;

  const thresholdEl      = el.querySelector("#st-threshold");
  const contactsBtn      = el.querySelector("#st-contacts");
  const rmsdBtn          = el.querySelector("#st-rmsd");
  const rmsfBtn          = el.querySelector("#st-rmsf");
  const pcaBtn           = el.querySelector("#st-pca");
  const contactsResultEl = el.querySelector("#st-contacts-result");
  const rmsdResultEl     = el.querySelector("#st-rmsd-result");
  const pcaResultEl      = el.querySelector("#st-pca-result");
  const statusEl         = el.querySelector("#st-status");

  function applyState(s) {
    state = { ...state, ...s };
    if (state.contacts_n !== null) contactsResultEl.textContent = `Contacts: ${state.contacts_n}`;
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
  rmsdBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_rmsd", payload: {} });
  });
  rmsfBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_rmsf", payload: {} });
  });
  pcaBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "compute_pca", payload: {} });
  });

  model.on("msg:custom", (msg) => {
    if (msg?.type === "state") applyState(msg.state);
  });

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
        self.push_state({
            "contacts_n": None, "rmsd": None, "rmsf_mean": None,
            "pca_variance": None, "status": "idle", "error": None,
        })

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

            if action_id == "compute_contacts":
                threshold_ang = payload.get("threshold_angstroms", 12.0)
                contacts = msm.structure.get_contacts(ms, threshold=f"{threshold_ang} angstroms")
                runtime.contacts_result = contacts
                n_contacts = int(np.asarray(contacts).sum()) // 2
                record_event(view, "panel_contacts", n_contacts=n_contacts)
                self.push_state({"contacts_n": n_contacts, "status": "done", "error": None})

            elif action_id == "compute_rmsd":
                rmsd = msm.structure.get_rmsd(ms)
                runtime.rmsd_result = rmsd
                rmsd_arr = np.asarray(rmsd).flatten()
                mean_rmsd = float(rmsd_arr.mean()) if len(rmsd_arr) else 0.0
                record_event(view, "panel_rmsd", mean_rmsd=mean_rmsd)
                self.push_state({"rmsd": mean_rmsd, "status": "done", "error": None})

            elif action_id == "compute_rmsf":
                rmsf = msm.structure.get_rmsf(ms)
                runtime.rmsf_result = rmsf
                rmsf_arr = np.asarray(rmsf).flatten()
                mean_rmsf = float(rmsf_arr.mean()) if len(rmsf_arr) else 0.0
                record_event(view, "panel_rmsf", mean_rmsf=mean_rmsf)
                self.push_state({"rmsf_mean": mean_rmsf, "status": "done", "error": None})

            elif action_id == "compute_pca":
                principal_components, variances = msm.structure.principal_component_analysis(ms)
                runtime.pca_result = (principal_components, variances)
                variances_arr = np.asarray(variances).flatten()
                pc1_variance = float(variances_arr[0]) if len(variances_arr) else 0.0
                # Show PC1 vectors as displacement arrows
                origins = None
                pc1 = np.asarray(principal_components[0]) if hasattr(principal_components, "__len__") else np.asarray(principal_components)
                view.shapes.add_displacement_vectors(
                    origins=None,
                    vectors=pc1,
                    atom_indices=list(range(len(pc1))),
                    tag="msmt-pca-pc1",
                )
                record_event(view, "panel_pca", pc1_variance=pc1_variance)
                self.push_state({"pca_variance": pc1_variance, "status": "done", "error": None})

        except Exception as exc:
            self.push_state({"status": "error", "error": str(exc)})
