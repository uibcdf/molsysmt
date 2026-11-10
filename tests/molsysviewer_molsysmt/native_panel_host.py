"""Shared native Qt test controls; optional GUI imports remain runtime-only."""

import json
import time


class NativePanelHost:
    def __init__(self, system, output, *, phase=lambda: "native panel"):
        import molsysviewer.standalone_qt as qt

        qt._qt_shell_state_path = lambda: output / "shell-state.json"
        runtime = qt.create_standalone_qt0_window(
            system,
            output_filename=str(output / "shell.html"),
            discover_addons=True,
            apply_project_config=False,
        )
        self.app, self.window, self.web = (
            runtime[k] for k in ("app", "window", "webview")
        )
        self.view = self.web._molsysviewer_view
        self.bridge = self.web._molsysviewer_qt_bridge
        self.phase = phase
        self.window.show()

    def wait(self, predicate, timeout=30):
        until = time.monotonic() + timeout
        while time.monotonic() < until:
            self.app.processEvents()
            if predicate():
                return
            time.sleep(0.01)
        raise AssertionError(
            f"{self.phase()}: timed out; bridge failures={self.bridge.failed_deliveries}"
        )

    def evaluate(self, script, target=None):
        answer = []
        (self.web if target is None else target).page().runJavaScript(
            "JSON.stringify(" + script + ")", answer.append
        )
        self.wait(lambda: bool(answer))
        return (
            json.loads(answer[0])
            if isinstance(answer[0], str) and answer[0]
            else answer[0]
        )

    def idle(self, target_bridge=None):
        bridge = self.bridge if target_bridge is None else target_bridge
        self.wait(lambda: bridge.ready and not bridge.queue and bridge.inflight is None)

    def click(self, selector):
        self.wait(
            lambda: self.evaluate(
                f"(() => {{const e=document.querySelector({json.dumps(selector)});return !!e&&!e.disabled&&e.getClientRects().length>0;}})()"
            )
        )
        assert self.evaluate(
            f"(() => {{const e=document.querySelector({json.dumps(selector)});if(!e)return false;e.click();return true;}})()"
        ), selector

    def fill(self, key, value):
        selector = ".msm-system [data-" + key + "]"
        self.wait(
            lambda: self.evaluate(
                f"(() => {{const e=document.querySelector({json.dumps(selector)});return !!e&&!e.disabled&&e.getClientRects().length>0;}})()"
            )
        )
        assert self.evaluate(
            f'(() => {{const e=document.querySelector({json.dumps(selector)});if(!e)return false;e.value={json.dumps(value)};e.dispatchEvent(new Event("input",{{bubbles:true}}));e.dispatchEvent(new Event("change",{{bubbles:true}}));return true;}})()'
        ), key

    def visible(self, selector):
        return self.evaluate(
            f"(() => {{const e=document.querySelector({json.dumps(selector)});return !!e&&e.getClientRects().length>0;}})()"
        )

    def received(self, target, target_web=None, target_bridge=None):
        import numpy as np

        from molsysmt import pyunitwizard as puw

        positions = "(() => {const s=window.__molsysviewerDocsController?.getStructureData();if(!s)return null;const result=[];for(const u of s.units)for(const a of u.elements){const source=u.model.sourceData.kind==='mol-viewer:molsysmt'?u.model.atomicHierarchy.atomSourceIndex.value(a):a;result[source]=Array.from(u.conformation.position(a,[0,0,0]));}return result;})()"
        self.idle(target_bridge)
        expected = puw.get_value(
            target.molsys.structures.coordinates, to_unit="angstrom"
        )[0]
        self.wait(
            lambda: (
                (raw := self.evaluate(positions, target_web)) is not None
                and np.asarray(raw).shape == expected.shape
                and np.allclose(np.asarray(raw), expected, atol=1e-4, rtol=0)
            )
        )

    def open_panel(self, name):
        if not self.visible('[data-molsysviewer-addon-workspace-tab="molsysmt"]'):
            self.click('[title="Panel mode (N / W)"]')
        if not self.visible('[data-molsysviewer-addon-workspace-tab="molsysmt"]'):
            self.click(
                '[data-molsysviewer-panel-stack-option="addons"], [data-molsysviewer-panel-stack-current="addons"]'
            )
        self.click('[data-molsysviewer-addon-workspace-tab="molsysmt"]')
        self.click('[data-molsysviewer-addon-panel-tab="' + name + '"]')
        self.wait(
            lambda: self.visible(
                "[data-geometry-heading]" if name == "geometry" else ".msm-" + name
            )
        )
