"""MolSysMT PBC panel — wrap, unwrap, and MIC operations."""

from __future__ import annotations

from typing import Any

from molsysviewer import AddonPanelWidget

from ..access import has_system
from ..adapters.pbc import pbc_status as get_pbc_status
from ..adapters.pbc import transform_pbc
from ..diagnostics import panel_error_state
from ..runtime import ensure_runtime, record_event


_ESM = """
export function render({ model, el }) {
  let state = {
    pbc_status: null,
    last_op: null,
    update_mode: null,
    mutation_warning: null,
    status: "idle",
    error: null
  };

  el.innerHTML = `
    <div class="msmt-panel">
      <div data-molsysviewer-addon-section="molsysmt:pbc-status">
        <div class="msmt-row">
          <span class="msmt-label">PBC status</span>
          <span id="pbc-status-badge" class="msmt-badge">unknown</span>
        </div>
        <button class="msmt-btn" id="pbc-check">Check PBC</button>
      </div>

      <div data-molsysviewer-addon-section="molsysmt:pbc-wrapping">
        <div class="msmt-section-title">Wrapping</div>
        <button class="msmt-btn msmt-btn--primary" id="pbc-wrap">Wrap to PBC</button>
        <button class="msmt-btn msmt-btn--primary" id="pbc-mic">Wrap to MIC</button>
        <button class="msmt-btn" id="pbc-unwrap">Unwrap</button>
        <div class="msmt-note">Updates coordinates in place and preserves viewer overlays.</div>
      </div>

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
      const detail = state.mutation_warning ? ` ${state.mutation_warning}` : "";
      opStatusEl.textContent = state.last_op ? `Done: ${state.last_op}.${detail}` : `Done.${detail}`;
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
        if has_system(view):
            try:
                pbc_status = get_pbc_status(view).has_pbc
            except Exception:
                pass
        runtime.pbc_status = pbc_status
        self.set_state({
            "pbc_status": pbc_status,
            "last_op": None,
            "update_mode": None,
            "mutation_warning": None,
            "status": "idle",
            "error": None,
        })

    def handle_action(self, view: Any, action_id: str, payload: dict) -> None:
        runtime = ensure_runtime(view)

        if action_id == "check_pbc":
            if not has_system(view):
                self.set_state({"status": "error", "error": "No molecular system attached."})
                return
            try:
                pbc_status = get_pbc_status(view).has_pbc
                runtime.pbc_status = pbc_status
                self.set_state({"pbc_status": pbc_status, "status": "done", "error": None})
            except Exception as exc:
                self.set_state(panel_error_state(view, panel="pbc", action=action_id, exc=exc))
            return

        if not has_system(view):
            self.set_state({"status": "error", "error": "No molecular system attached."})
            return

        self.set_state({"status": "running"})
        try:
            if action_id == "wrap_pbc":
                result = transform_pbc(view, "wrap_pbc")
                view.set_coordinates(result.coordinates)
                record_event(view, "panel_pbc", op="wrap_to_pbc")
                self.set_state({
                    "last_op": "wrap to PBC",
                    "update_mode": "coordinates",
                    "mutation_warning": "Coordinates updated in place; viewer overlays preserved.",
                    "status": "done",
                    "error": None,
                })

            elif action_id == "wrap_mic":
                result = transform_pbc(view, "wrap_mic")
                view.set_coordinates(result.coordinates)
                record_event(view, "panel_pbc", op="wrap_to_mic")
                self.set_state({
                    "last_op": "wrap to MIC",
                    "update_mode": "coordinates",
                    "mutation_warning": "Coordinates updated in place; viewer overlays preserved.",
                    "status": "done",
                    "error": None,
                })

            elif action_id == "unwrap_pbc":
                result = transform_pbc(view, "unwrap_pbc")
                view.set_coordinates(result.coordinates)
                record_event(view, "panel_pbc", op="unwrap")
                self.set_state({
                    "last_op": "unwrap",
                    "update_mode": "coordinates",
                    "mutation_warning": "Coordinates updated in place; viewer overlays preserved.",
                    "status": "done",
                    "error": None,
                })

        except Exception as exc:
            self.set_state(panel_error_state(view, panel="pbc", action=action_id, exc=exc))
