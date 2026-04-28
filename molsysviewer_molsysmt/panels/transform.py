"""MolSysMT Transform panel — center, RMSD-fit, align principal axes → reload."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = { last_op: null, status: "idle", error: null };

  el.innerHTML = `
    <div class="msmt-panel">
      <div class="msmt-section-title">Centering & Alignment</div>
      <button class="msmt-btn msmt-btn--primary" id="tr-center">Center Structure</button>
      <button class="msmt-btn msmt-btn--primary" id="tr-fit">RMSD Fit (to frame 0)</button>
      <button class="msmt-btn msmt-btn--primary" id="tr-axes">Align Principal Axes</button>
      <div class="msmt-note">Each operation reloads the viewer with the transformed system.</div>
      <div class="msmt-status" id="tr-status"></div>
    </div>
  `;

  const centerBtn = el.querySelector("#tr-center");
  const fitBtn    = el.querySelector("#tr-fit");
  const axesBtn   = el.querySelector("#tr-axes");
  const statusEl  = el.querySelector("#tr-status");

  function setButtons(disabled) {
    centerBtn.disabled = disabled;
    fitBtn.disabled = disabled;
    axesBtn.disabled = disabled;
  }

  function applyState(s) {
    state = { ...state, ...s };
    if (state.status === "running") {
      statusEl.textContent = "Transforming…";
      statusEl.className = "msmt-status msmt-status--busy";
      setButtons(true);
    } else if (state.status === "done") {
      statusEl.textContent = state.last_op ? `Done: ${state.last_op}.` : "Done.";
      statusEl.className = "msmt-status msmt-status--ok";
      setButtons(false);
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error;
      statusEl.className = "msmt-status msmt-status--error";
      setButtons(false);
    } else {
      statusEl.textContent = "";
      statusEl.className = "msmt-status";
      setButtons(false);
    }
  }

  centerBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "center_structure", payload: {} });
  });
  fitBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "fit_structure", payload: {} });
  });
  axesBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "align_axes", payload: {} });
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
.msmt-note { font-size: 11px; opacity: 0.6; font-style: italic; }
.msmt-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; background: #eee; width: 100%; text-align: left; }
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""


class MolSysMTTransformPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        self.push_state({"last_op": None, "status": "idle", "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if runtime.molecular_system is None:
            self.push_state({"status": "error", "error": "No molecular system attached."})
            return

        self.push_state({"status": "running"})
        try:
            import molsysmt as msm
            ms = runtime.molecular_system

            if action_id == "center_structure":
                new_ms = msm.structure.center(ms, in_place=False)
                runtime.molecular_system = new_ms
                view.load(new_ms, mode="replace")
                record_event(view, "panel_transform", op="center")
                self.push_state({"last_op": "center", "status": "done", "error": None})

            elif action_id == "fit_structure":
                new_ms = msm.structure.least_rmsd_fit(ms, in_place=False)
                runtime.molecular_system = new_ms
                view.load(new_ms, mode="replace")
                record_event(view, "panel_transform", op="fit")
                self.push_state({"last_op": "RMSD fit", "status": "done", "error": None})

            elif action_id == "align_axes":
                new_ms = msm.structure.align_principal_axes(ms, in_place=False)
                runtime.molecular_system = new_ms
                view.load(new_ms, mode="replace")
                record_event(view, "panel_transform", op="align_axes")
                self.push_state({"last_op": "align principal axes", "status": "done", "error": None})

        except Exception as exc:
            self.push_state({"status": "error", "error": str(exc)})
