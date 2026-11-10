"""Actual native Qt Geometry UI receiving, without replacing its transport."""


def main():
    import json
    import sys
    import time
    from pathlib import Path

    # This child is executed as a file, so select its owning test package
    # before importing the independent OpenMM reference. Viewer also has tests/.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

    import molsysviewer as msv
    import molsysviewer.standalone_qt as qt
    import numpy as np
    from PySide6.QtCore import QCoreApplication, QEvent

    import molsysmt as msm

    out = Path(sys.argv[1])
    out.mkdir(exist_ok=True)
    qt._qt_shell_state_path = lambda: out / "shell-state.json"
    puw = msm.pyunitwizard
    seed = msv.demo["pentalanine"]
    base = msm.extract(seed.molsys, structure_indices=[0])
    xyz = puw.get_value(base.structures.coordinates, to_unit="nm").copy()
    msm.set(
        base,
        coordinates=puw.quantity(xyz, "nm"),
        box=puw.quantity(np.eye(3)[None] * 5, "nm"),
    )
    msm.set(
        base,
        forcefield="AMBER14",
        water_model="TIP3P",
        constraints="hbonds",
        non_bonded_method="no cutoff",
    )
    import openmm

    from tests.molsysviewer_molsysmt.test_minimization_tools import (
        direct_openmm_minimum,
    )

    _, _, expected, _ = direct_openmm_minimum(base, openmm)
    runtime = qt.create_standalone_qt0_window(
        base,
        output_filename=str(out / "shell.html"),
        discover_addons=True,
        apply_project_config=False,
    )
    app, window, web = runtime["app"], runtime["window"], runtime["webview"]
    view, bridge = web._molsysviewer_view, web._molsysviewer_qt_bridge
    checks = []
    phase = "initialization"
    window.show()

    def wait(predicate, timeout=30):
        until = time.monotonic() + timeout
        while time.monotonic() < until:
            app.processEvents()
            if predicate():
                return
            time.sleep(0.01)
        raise AssertionError(
            f"{phase}: timed out; bridge failures={bridge.failed_deliveries}"
        )

    def evaluate(script, target=web):
        answer = []
        target.page().runJavaScript("JSON.stringify(" + script + ")", answer.append)
        wait(lambda: bool(answer))
        return (
            json.loads(answer[0])
            if isinstance(answer[0], str) and answer[0]
            else answer[0]
        )

    def idle(target_bridge=bridge):
        wait(
            lambda: (
                target_bridge.ready
                and not target_bridge.queue
                and target_bridge.inflight is None
            )
        )

    def click(selector):
        wait(
            lambda: evaluate(
                f"(() => {{const e=document.querySelector({json.dumps(selector)});return !!e&&!e.disabled&&e.getClientRects().length>0;}})()"
            )
        )
        assert evaluate(
            f"(() => {{const e=document.querySelector({json.dumps(selector)});if(!e)return false;e.click();return true;}})()"
        ), selector

    def fill(key, value):
        selector = ".msm-system [data-" + key + "]"
        wait(
            lambda: evaluate(
                f"(() => {{const e=document.querySelector({json.dumps(selector)});return !!e&&!e.disabled&&e.getClientRects().length>0;}})()"
            )
        )
        assert evaluate(
            f'(() => {{const e=document.querySelector({json.dumps(selector)});if(!e)return false;e.value={json.dumps(value)};e.dispatchEvent(new Event("input",{{bubbles:true}}));e.dispatchEvent(new Event("change",{{bubbles:true}}));return true;}})()'
        ), key

    def visible(selector):
        return evaluate(
            f"(() => {{const e=document.querySelector({json.dumps(selector)});return !!e&&e.getClientRects().length>0;}})()"
        )

    positions = "(() => {const s=window.__molsysviewerDocsController?.getStructureData();if(!s)return null;const result=[];for(const u of s.units)for(const a of u.elements)result[a]=Array.from(u.conformation.position(a,[0,0,0]));return result;})()"

    def received(target, target_web=web, target_bridge=bridge):
        idle(target_bridge)
        wait(
            lambda: (
                (raw := evaluate(positions, target_web)) is not None
                and np.allclose(
                    np.asarray(raw),
                    puw.get_value(
                        target.molsys.structures.coordinates, to_unit="angstrom"
                    )[0],
                    atol=1e-4,
                    rtol=0,
                )
            )
        )

    try:
        wait(lambda: bridge.ready)
        received(view)
        click('[title="Panel mode (N / W)"]')
        wait(
            lambda: evaluate(
                '!!document.querySelector("[data-molsysviewer-addon-workspace-tab=\\"molsysmt\\"]")'
            )
        )
        if not visible('[data-molsysviewer-addon-workspace-tab="molsysmt"]'):
            click(
                '[data-molsysviewer-panel-stack-option="addons"], [data-molsysviewer-panel-stack-current="addons"]'
            )
        click('[data-molsysviewer-addon-workspace-tab="molsysmt"]')
        click('[data-molsysviewer-addon-panel-tab="geometry"]')
        fill("task", "minimize")
        wait(
            lambda: (
                not evaluate(
                    "document.querySelector('.msm-system [data-task]').disabled"
                )
            )
        )
        fill("effect", "result")
        click(".msm-system [data-preview]")
        wait(lambda: visible(".msm-system [data-review]"))
        assert "AMBER14" in evaluate(
            "document.querySelector('[data-mechanical-model]').innerText"
        )
        np.testing.assert_array_equal(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), xyz
        )
        checks.append(
            "Review exposes stored model and native defaults without changing coordinates"
        )
        click(".msm-system [data-back]")
        wait(lambda: visible(".msm-system [data-preview]"))
        np.testing.assert_array_equal(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), xyz
        )
        checks.append("Back cancels minimization without an edit")
        click(".msm-system [data-preview]")
        click(".msm-system [data-confirm]")
        wait(lambda: visible(".msm-system [data-result]"))
        records = view.addons.manager.presentations.records()
        assert len(records) == 1
        handle = records[0]["id"]
        child = view.addons.manager.presentations.get(handle)
        np.testing.assert_allclose(
            puw.get_value(child.molsys.structures.coordinates, to_unit="nm")[0],
            expected,
            atol=3e-5,
        )
        np.testing.assert_array_equal(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), xyz
        )
        checks.append("Independent result matches direct OpenMM with unchanged source")
        click(".msm-system [data-show-window]")
        child_runtime = view.addons.manager.presentations._records[handle]["runtime"]
        wait(lambda: child_runtime["window"].isVisible())
        child_web = child_runtime["webview"]
        received(child, child_web, child_web._molsysviewer_qt_bridge)
        checks.append(
            "Actual independent Qt window renders native minimized coordinates"
        )
        click(".msm-system [data-new-result]")
        fill("effect", "update")
        click(".msm-system [data-preview]")
        click(".msm-system [data-confirm]")
        wait(lambda: view.addons.molsysmt.get_sync_status()["target_revision"] == 1)
        received(view)
        np.testing.assert_allclose(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[0],
            expected,
            atol=3e-5,
        )
        assert child.molsys is not view.molsys
        checks.append(
            "Reviewed current refinement publishes one coordinate edit without replacing the primary"
        )
        assert len(view.addons.manager.presentations.records()) == 1
        view.addons.manager.presentations.close(handle)
        wait(lambda: child.closed)
        assert not view.closed
        checks.append("Independent result closure preserves the live source")
        web.grab().save(str(out / "refinement.png"))
        (out / "report.json").write_text(
            json.dumps(
                {
                    "checks": checks,
                    "qt_platform": app.platformName(),
                    "scope": "Automated native Qt/WebEngine/Mol* minimization review/cancel, independent/current effects, actual result window and direct OpenMM coordinates. Not human or installed-artifact acceptance.",
                },
                indent=2,
            )
            + "\n"
        )
    finally:
        for handle in list(view.addons.manager.presentations._records):
            view.addons.manager.presentations.close(handle)
        window.close()
        seed.close()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()


if __name__ == "__main__":
    main()
