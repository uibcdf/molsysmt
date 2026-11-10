"""Actual native Qt Geometry UI receiving, without replacing its transport."""


def main():
    import json
    import sys
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
    from tests.molsysviewer_molsysmt.native_panel_host import NativePanelHost

    checks = []
    phase = "initialization"
    host = NativePanelHost(base, out, phase=lambda: phase)
    app, window, web = host.app, host.window, host.web
    view, bridge = host.view, host.bridge
    wait, evaluate = host.wait, host.evaluate
    click, fill, visible, received = host.click, host.fill, host.visible, host.received

    try:
        wait(lambda: bridge.ready)
        received(view)
        host.open_panel("geometry")
        fill("task", "minimize")
        wait(
            lambda: evaluate(
                "(() => {const e=document.querySelector('[data-geometry-heading]');const task=document.querySelector('.msm-system [data-task]');return e?.textContent.includes('Minimize potential energy')&&!!task&&!task.disabled;})()"
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
