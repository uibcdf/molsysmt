"""Actual native Qt chemistry repair and independently owned result windows."""


def main():
    import json
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from PySide6.QtCore import QCoreApplication, QEvent

    import molsysmt as msm
    from tests.molsysviewer_molsysmt.native_panel_host import NativePanelHost
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import same
    from tests.molsysviewer_molsysmt.test_chemistry_repair_panel import (
        arguments,
        source,
    )

    out = Path(sys.argv[1])
    out.mkdir(exist_ok=True)
    base = source("terminal_cappings")
    original = msm.copy(base)
    phase = "initialization"
    host = NativePanelHost(base, out, phase=lambda: phase)
    view, web, window, app = host.view, host.web, host.window, host.app
    checks = []
    try:
        host.wait(lambda: host.bridge.ready)
        host.received(view)
        host.open_panel("chemistry")
        phase = "explicit terminal completion"
        host.fill("task", "terminal_cappings")
        host.fill("source", "all")
        host.fill("n-cap", "ACE")
        host.fill("c-cap", "NME")
        host.fill("ph", "12")
        host.click(".msm-system [data-prepare]")
        host.wait(lambda: host.visible(".msm-system [data-result]"))
        records = view.addons.manager.presentations.records()
        assert len(records) == 1
        handle = records[0]["id"]
        child = view.addons.manager.presentations.get(handle)
        method, kwargs = arguments("terminal_cappings")
        same(child.molsys, getattr(msm.build, method)(view.molsys, **kwargs))
        same(view.molsys, original)
        checks.append("Explicit native terminal completion preserves the source")
        host.click(".msm-system [data-replace-review]")
        host.wait(lambda: host.visible(".msm-system [data-replacement]"))
        host.click(".msm-system [data-replace-back]")
        host.wait(lambda: not host.visible(".msm-system [data-replacement]"))
        same(view.molsys, original)
        checks.append("Replacement Back leaves molecular data unchanged")
        host.click(".msm-system [data-show-window]")
        runtime = view.addons.manager.presentations._records[handle]["runtime"]
        host.wait(lambda: runtime["window"].isVisible())
        host.received(
            child, runtime["webview"], runtime["webview"]._molsysviewer_qt_bridge
        )
        checks.append("Independent Qt result window renders native capped coordinates")
        host.click(".msm-system [data-new-result]")
        host.wait(lambda: not host.visible(".msm-system [data-result]"))
        phase = "explicit typing"
        view.load(source("partial_charges"), mode="replace")
        original = msm.copy(view.molsys)
        host.received(view)
        host.fill("task", "autodock_types")
        host.click(".msm-system [data-prepare]")
        host.wait(lambda: host.visible(".msm-system [data-result]"))
        candidates = [
            r for r in view.addons.manager.presentations.records() if r["id"] != handle
        ]
        assert len(candidates) == 1
        typed = view.addons.manager.presentations.get(candidates[0]["id"])
        assert typed.molsys.molecular_mechanics.atom_ff_type.tolist() == [
            "C",
            "OA",
            "H",
            "H",
            "H",
            "HD",
        ]
        same(view.molsys, original)
        checks.append(
            "Native AutoDock4 labels are attached only to the separate result"
        )
        host.click(".msm-system [data-new-result]")
        host.wait(lambda: not host.visible(".msm-system [data-result]"))
        phase = "explicit charges"
        host.fill("task", "partial_charges")
        host.fill("expected-charge", "0")
        host.click(".msm-system [data-prepare]")
        host.wait(lambda: host.visible(".msm-system [data-result]"))
        candidates = [
            r for r in view.addons.manager.presentations.records() if r["id"] != handle
        ]
        assert len(candidates) == 1
        charged = view.addons.manager.presentations.get(candidates[0]["id"])
        same(
            charged.molsys,
            msm.build.assign_partial_charges(
                view.molsys, method="gasteiger_marsili", expected_total_charge=0
            ),
        )
        same(view.molsys, original)
        checks.append(
            "Named charge assignment preserves primary data and retained cap window"
        )
        view.addons.manager.presentations.close(handle)
        host.wait(lambda: child.closed)
        assert not view.closed and not charged.closed
        checks.append("Closing the retained independent window preserves other owners")
        assert not host.bridge.failed_deliveries
        web.grab().save(str(out / "chemistry.png"))
        (out / "report.json").write_text(
            json.dumps(
                {
                    "checks": checks,
                    "qt_platform": app.platformName(),
                    "scope": "Automated native Qt/WebEngine/Mol* capping, Back, separate geometry window, AutoDock/charge assignments and independent lifetime; not human or installed acceptance.",
                },
                indent=2,
            )
            + "\n"
        )
    finally:
        for record in list(view.addons.manager.presentations.records()):
            view.addons.manager.presentations.close(record["id"])
        window.close()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()


if __name__ == "__main__":
    main()
