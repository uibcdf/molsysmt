"""MolSysMT System panel widget — loaded system summary with inspect trigger."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = {
    n_atoms: null,
    n_residues: null,
    n_chains: null,
    n_frames: null,
    status: "idle",
    error: null,
  };

  el.innerHTML = `
    <div class="msmt-panel">
      <div class="msmt-summary" id="msmt-summary">
        <span class="msmt-empty">No molecular system loaded.</span>
      </div>
      <button class="msmt-btn msmt-btn--primary" id="msmt-inspect">Inspect</button>
      <div class="msmt-status" id="msmt-status"></div>
    </div>
  `;

  const summaryEl = el.querySelector("#msmt-summary");
  const inspectBtn = el.querySelector("#msmt-inspect");
  const statusEl  = el.querySelector("#msmt-status");

  function buildSummaryHtml(s) {
    if (s.n_atoms === null && s.n_residues === null) {
      return '<span class="msmt-empty">No molecular system loaded.</span>';
    }
    const rows = [];
    if (s.n_atoms    !== null) rows.push(["Atoms",    s.n_atoms]);
    if (s.n_residues !== null) rows.push(["Residues", s.n_residues]);
    if (s.n_chains   !== null) rows.push(["Chains",   s.n_chains]);
    if (s.n_frames   !== null) rows.push(["Frames",   s.n_frames]);
    return rows.map(([label, val]) =>
      `<div class="msmt-row"><span class="msmt-label">${label}</span><span class="msmt-value">${val}</span></div>`
    ).join("");
  }

  function applyState(s) {
    state = { ...state, ...s };
    summaryEl.innerHTML = buildSummaryHtml(state);

    inspectBtn.disabled = state.status === "inspecting";
    inspectBtn.textContent = state.status === "inspecting" ? "Inspecting…" : "Inspect";

    if (state.status === "done") {
      statusEl.textContent = "Done.";
      statusEl.className = "msmt-status msmt-status--ok";
    } else if (state.status === "error" && state.error) {
      statusEl.textContent = "Error: " + state.error;
      statusEl.className = "msmt-status msmt-status--error";
    } else if (state.status === "inspecting") {
      statusEl.textContent = "Inspecting…";
      statusEl.className = "msmt-status msmt-status--busy";
    } else {
      statusEl.textContent = "";
      statusEl.className = "msmt-status";
    }
  }

  inspectBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "inspect", payload: {} });
  });

  model.on("msg:custom", (msg) => {
    if (msg?.type === "state") applyState(msg.state);
  });

  model.send({ type: "query", id: "viewer.context" });
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
.msmt-summary {
  min-height: 36px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.msmt-empty {
  font-size: 11px;
  opacity: 0.5;
  font-style: italic;
}
.msmt-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}
.msmt-label {
  opacity: 0.8;
}
.msmt-value {
  font-weight: 600;
  font-family: monospace;
}
.msmt-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}
.msmt-btn--primary {
  background: #3a7bd5;
  color: #fff;
}
.msmt-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.msmt-status {
  font-size: 11px;
  min-height: 16px;
}
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""


class MolSysMTSystemPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        runtime = ensure_runtime(view)
        self.push_state(self._build_state(runtime))

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "inspect":
            if runtime.molecular_system is None:
                self.push_state({**self._build_state(runtime), "status": "error", "error": "No molecular system attached."})
                return
            self.push_state({**self._build_state(runtime), "status": "inspecting"})
            try:
                self._refresh_counts(runtime)
                record_event(view, "panel_inspect", n_atoms=runtime.n_atoms)
                self.push_state({**self._build_state(runtime), "status": "done"})
            except Exception as exc:
                self.push_state({**self._build_state(runtime), "status": "error", "error": str(exc)})

    @staticmethod
    def _refresh_counts(runtime: Any) -> None:
        import molsysmt as msm

        ms = runtime.molecular_system
        runtime.n_atoms      = msm.get(ms, n_atoms=True)
        runtime.n_residues   = msm.get(ms, element="group", n_groups=True)
        runtime.n_chains     = msm.get(ms, element="chain", n_chains=True)
        runtime.n_frames     = msm.get(ms, element="system", n_structures=True)

    @staticmethod
    def _build_state(runtime: Any) -> dict:
        return {
            "n_atoms":    runtime.n_atoms,
            "n_residues": runtime.n_residues,
            "n_chains":   runtime.n_chains,
            "n_frames":   runtime.n_frames,
            "status": "idle",
            "error": None,
        }
