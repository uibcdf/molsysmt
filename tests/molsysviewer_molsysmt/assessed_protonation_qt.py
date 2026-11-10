"""Native Qt receiving of an inspected process-local protonation decision."""


def main():
    import json
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from PySide6.QtCore import QCoreApplication, QEvent

    import molsysmt as msm
    from tests.molsysviewer_molsysmt.native_panel_host import NativePanelHost
    from tests.molsysviewer_molsysmt.protonation_panel_fixture import source_system
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import same

    output = Path(sys.argv[1])
    output.mkdir(exist_ok=True)
    source, keep = source_system()
    before = source.copy()
    expected = msm.extract(source, selection=keep)
    phase = "initialization"
    host = NativePanelHost(source, output, phase=lambda: phase)
    checks = []
    policy = msm.pyunitwizard.context(standard_units=["pm", "ps", "radians"])
    policy.__enter__()
    try:
        view = host.view
        host.wait(lambda: host.bridge.ready)
        host.received(view)
        host.open_panel("chemistry")
        host.fill("task", "protonation")
        host.fill("assessment-ph", "12")

        def inspect():
            host.click(".msm-system [data-inspect]")
            host.wait(lambda: host.visible(".msm-system [data-report]"))

        phase = "read-only assessment"
        inspect()
        assert "6 proposed H removals" in host.evaluate(
            "document.querySelector('[data-assessment-summary]').textContent"
        )
        same(view.molsys, before)
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0
        checks.append(
            "The native assessed decision preserves the source before explicit action"
        )
        phase = "Back and independent apply"
        host.click(".msm-system [data-protonation-review]")
        host.wait(lambda: host.visible(".msm-system [data-protonation-confirm]"))
        host.click(".msm-system [data-protonation-back]")
        host.wait(lambda: not host.visible(".msm-system [data-protonation-confirm]"))
        same(view.molsys, before)
        host.click(".msm-system [data-protonation-prepare]")
        host.wait(lambda: host.visible(".msm-system [data-preparation-result]"))
        records = view.addons.manager.presentations.records()
        assert len(records) == 1
        handle = records[0]["id"]
        child = view.addons.manager.presentations.get(handle)
        same(child.molsys, expected)
        same(view.molsys, before)
        assert child.molsys is not view.molsys
        checks.append(
            "Back cancels and independent assessed apply keeps source data and scene"
        )
        phase = "independent native window"
        host.click(".msm-system [data-show-window]")
        runtime = view.addons.manager.presentations._records[handle]["runtime"]
        host.wait(lambda: runtime["window"].isVisible())
        host.received(
            child, runtime["webview"], runtime["webview"]._molsysviewer_qt_bridge
        )
        checks.append(
            "The separate native result renders in its independently owned Qt window"
        )
        phase = "managed assessed apply"
        inspect()
        host.click(".msm-system [data-protonation-review]")
        host.wait(lambda: host.visible(".msm-system [data-protonation-confirm]"))
        host.click(".msm-system [data-protonation-apply]")
        host.wait(
            lambda: (
                view.molsys.get_n_atoms() == 590
                and view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
            )
        )
        host.received(view)
        same(view.molsys, expected)
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
        assert not host.visible(".msm-system [data-report]")
        checks.append(
            "Managed apply projects every structure through the inspected native atom map"
        )
        phase = "assessed no-op"
        inspect()
        assert "0 proposed H removals" in host.evaluate(
            "document.querySelector('[data-assessment-summary]').textContent"
        )
        host.click(".msm-system [data-protonation-review]")
        host.wait(lambda: host.visible(".msm-system [data-protonation-confirm]"))
        host.click(".msm-system [data-protonation-apply]")
        host.wait(lambda: not host.visible(".msm-system [data-report]"))
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
        same(view.molsys, expected)
        checks.append("A consumed assessed no-op adds no molecular revision")
        same(child.molsys, expected)
        assert view.molsys.structures.structure_id.tolist() == ["C", "A", "C"]
        assert (
            len(view.molsys.interactions["source-observations"].occurrence_structures)
            == 3
        )
        assert view.player.n_structures == 3 and view.whole.get(n_atoms=True) == 590
        assert not host.bridge.failed_deliveries
        checks.append(
            "Named observations and repeated structure labels remain mapped with independent lifetime"
        )
        (output / "report.json").write_text(
            json.dumps(
                {
                    "checks": checks,
                    "qt_platform": host.app.platformName(),
                    "scope": "Automated real native Qt assessed protonation reconciliation; not environmental pKa, human, installed or release qualification.",
                },
                indent=2,
            )
            + "\n"
        )
    finally:
        policy.__exit__(None, None, None)
        host.window.close()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        host.app.processEvents()


if __name__ == "__main__":
    main()
