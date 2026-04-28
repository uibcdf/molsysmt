"""MolSysMT PBC panel — wrap, unwrap, and MIC operations."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = { pbc_status: null, last_op: null, status: "idle", error: null };

  el.innerHTML = `
    <div class="msmt-panel">
      <div class="msmt-row">
        <span class="msmt-label">PBC status</span>
        <span id="pbc-status-badge" class="msmt-badge">unknown</span>
      </div>
      <button class="msmt-btn" id="pbc-check">Check PBC</button>

      <div class="msmt-section-title">Wrapping</div>
      <button class="msmt-btn msmt-btn--primary" id="pbc-wrap">Wrap to PBC</button>
      <button class="msmt-btn msmt-btn--primary" id="pbc-mic">Wrap to MIC</button>
      <button class="msmt-btn" id="pbc-unwrap">Unwrap</button>
      <div class="msmt-note">Reloads viewer with transformed coordinates.</div>

      <div class="msmt-status" id="pbc-op-status"></div>
    </div>
  `;

  const badgeEl      = el.querySelector("#pbc-status-badge");
  const checkBtn     = el.querySelector("#pbc-check");
  const wrapBtn      = el.querySelector("#pbc-wrap");
  const micBtn       = el.querySelector("#pbc-mic");
  const unwrapBtn    = el.querySelector("#pbc-unwrap");
  const opStatusEl   = el.querySelector("#pbc-op-status");

  function setButtons(disabled) {
    wrapBtn.disabled = disabled;
    micBtn.disabled = disabled;
    unwrapBtn.disabled = disabled;
    checkBtn.disabled = disabled;
  }

  function applyState(s) {
    state = { ...state, ...s };
    if (state.pbc_status !== null) {
      badgeEl.textContent = state.pbc_status ? "✓ has PBC" : "✗ no PBC";
      badgeEl.className = "msmt-badge " + (state.pbc_status ? "msmt-badge--ok" : "msmt-badge--warn");
    }
    if (state.status === "running") {
      opStatusEl.textContent = "Working…"; opStatusEl.className = "msmt-status msmt-status--busy";
      setButtons(true);
    } else if (state.status === "done") {
      opStatusEl.textContent = state.last_op ? `Done: ${state.last_op}.` : "Done.";
      opStatusEl.className = "msmt-status msmt-status--ok";
      setButtons(false);
    } else if (state.status === "error" && state.error) {
      opStatusEl.textContent = "Error: " + state.error;
      opStatusEl.className = "msmt-status msmt-status--error";
      setButtons(false);
    } else {
      opStatusEl.textContent = ""; opStatusEl.className = "msmt-status";
      setButtons(false);
    }
  }

  checkBtn.addEventListener("click", () => { model.send({ type: "action", id: "check_pbc", payload: {} }); });
  wrapBtn.addEventListener("click",  () => { model.send({ type: "action", id: "wrap_pbc",   payload: {} }); });
  micBtn.addEventListener("click",   () => { model.send({ type: "action", id: "wrap_mic",   payload: {} }); });
  unwrapBtn.addEventListener("click",() => { model.send({ type: "action", id: "unwrap_pbc", payload: {} }); });

  model.on("msg:custom", (msg) => { if (msg?.type === "state") applyState(msg.state); });

  applyState(state);
}
"""

_CSS = """
.msmt-panel { display: flex; flex-direction: column; gap: 8px; padding: 8px; font-size: 13px; font-family: sans-serif; }
.msmt-section-title { font-size: 11px; font-weight: 700; text-transform: uppercase; opacity: 0.6; margin-top: 4px; }
.msmt-row { display: flex; align-items: center; justify-content: space-between; font-size: 12px; }
.msmt-label { opacity: 0.8; }
.msmt-badge { font-size: 11px; font-weight: 700; padding: 1px 6px; border-radius: 8px; background: #eee; }
.msmt-badge--ok   { background: #d4edda; color: #155724; }
.msmt-badge--warn { background: #fff3cd; color: #856404; }
.msmt-note { font-size: 11px; opacity: 0.6; font-style: italic; }
.msmt-btn { padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; background: #eee; width: 100%; text-align: left; }
.msmt-btn--primary { background: #3a7bd5; color: #fff; }
.msmt-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.msmt-status { font-size: 11px; min-height: 16px; }
.msmt-status--ok    { color: #4caf50; }
.msmt-status--error { color: #f44336; }
.msmt-status--busy  { opacity: 0.7; }
"""


class MolSysMTPBCPanel(AddonPanelWidget):
    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        runtime = ensure_runtime(view)
        pbc_status = None
        if runtime.molecular_system is not None:
            try:
                import molsysmt as msm
                pbc_status = bool(msm.pbc.has_pbc(runtime.molecular_system))
            except Exception:
                pass
        runtime.pbc_status = pbc_status
        self.push_state({"pbc_status": pbc_status, "last_op": None, "status": "idle", "error": None})

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "check_pbc":
            if runtime.molecular_system is None:
                self.push_state({"status": "error", "error": "No molecular system attached."})
                return
            try:
                import molsysmt as msm
                pbc_status = bool(msm.pbc.has_pbc(runtime.molecular_system))
                runtime.pbc_status = pbc_status
                self.push_state({"pbc_status": pbc_status, "status": "done", "error": None})
            except Exception as exc:
                self.push_state({"status": "error", "error": str(exc)})
            return

        if runtime.molecular_system is None:
            self.push_state({"status": "error", "error": "No molecular system attached."})
            return

        self.push_state({"status": "running"})
        try:
            import molsysmt as msm
            ms = runtime.molecular_system

            if action_id == "wrap_pbc":
                new_ms = msm.pbc.wrap_to_pbc(ms)
                runtime.molecular_system = new_ms
                view.load(new_ms, mode="replace")
                record_event(view, "panel_pbc", op="wrap_to_pbc")
                self.push_state({"last_op": "wrap to PBC", "status": "done", "error": None})

            elif action_id == "wrap_mic":
                new_ms = msm.pbc.wrap_to_mic(ms)
                runtime.molecular_system = new_ms
                view.load(new_ms, mode="replace")
                record_event(view, "panel_pbc", op="wrap_to_mic")
                self.push_state({"last_op": "wrap to MIC", "status": "done", "error": None})

            elif action_id == "unwrap_pbc":
                new_ms = msm.pbc.unwrap(ms)
                runtime.molecular_system = new_ms
                view.load(new_ms, mode="replace")
                record_event(view, "panel_pbc", op="unwrap")
                self.push_state({"last_op": "unwrap", "status": "done", "error": None})

        except Exception as exc:
            self.push_state({"status": "error", "error": str(exc)})
