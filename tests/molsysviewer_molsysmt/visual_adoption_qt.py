"""Native Qt real color themes, core series and plot-to-molecule navigation."""


def main():
    import json
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    import molsysviewer as msv
    import numpy as np
    from molsysviewer.colors import scalar_to_color_list
    from PySide6.QtCore import QCoreApplication, QEvent

    import molsysmt as msm
    from tests.molsysviewer_molsysmt.native_panel_host import NativePanelHost
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import same

    out = Path(sys.argv[1])
    out.mkdir(exist_ok=True)
    with msv.demo["pentalanine"] as seed:
        base = msm.extract(seed.molsys, structure_indices=[0, 8, 3])
    before = msm.copy(base)
    phase = "initialization"
    host = NativePanelHost(base, out, phase=lambda: phase)
    view, app, checks = host.view, host.app, []
    try:
        host.wait(lambda: host.bridge.ready)
        host.received(view)
        host.open_panel("analysis")
        host.click('[data-family="property"]')
        host.fill("task", "mass")
        host.fill("source", "all")
        host.click("[data-calculate]")
        host.wait(lambda: host.visible("[data-report]"))
        host.click('[data-result-row="0"]')
        host.click("[data-color-actions] summary")
        host.fill("color-palette", "blue_red")
        host.fill("color-range", "manual")
        host.fill("color-minimum", "0")
        host.fill("color-maximum", "20")
        host.click("[data-apply-report-colors]")
        host.wait(
            lambda: (
                "Colored Whole"
                in host.evaluate("document.querySelector('[data-status]').textContent")
            )
        )
        expected = scalar_to_color_list(
            msm.physchem.get_mass(view.molsys, element="atom"),
            palette=["#2166ac", "#f7f7f7", "#b2182b"],
            value_range=msm.pyunitwizard.quantity([0, 20], "dalton"),
        )
        colors_script = """(() => {const c=window.__molsysviewerDocsController,s=c?.getStructureData();if(!s)return null;const r=Array.from(c.state.globalReprs||[]).map(ref=>c.plugin.state.data.cells.get(ref)?.obj?.data?.repr).find(r=>r?.theme?.color?.color);if(!r)return null;return Array.from({length:62},(_,i)=>{const unit=s.units.find(u=>Array.from(u.elements).includes(i));return Number(r.theme.color.color({kind:'element-location',structure:s,unit,element:i},false));});})()"""
        host.wait(lambda: host.evaluate(colors_script) == expected)
        checks.append("Core Whole scalar colors reach the actual native Molstar theme")
        host.click("[data-clear]")
        host.wait(lambda: not host.visible("[data-report]"))
        assert host.evaluate(colors_script) == expected
        same(view.molsys, before)
        checks.append("Clearing the report retains colors and source molecular data")
        phase = "SASA series"
        host.fill("task", "sasa")
        host.fill("source", "indices")
        host.fill("indices", "20,10,6,20")
        host.fill("structures", "all")
        host.click("[data-calculate]")
        host.wait(lambda: host.visible("[data-report]"))
        host.click('[data-result-row="0"]')
        host.click("[data-selected-plot-actions] summary")
        host.click("[data-add-result-plot]")
        host.wait(lambda: len(view.trajectory_plot.records()) == 1)
        expected_series = msm.pyunitwizard.get_value(
            msm.physchem.get_sasa(
                view.molsys,
                selection=[20, 10, 6, 20],
                structure_indices="all",
                pbc=False,
                parallel=False,
                num_threads=1,
                use_gpu=False,
            ),
            to_unit="nm**2",
        )[:, 0]
        record = view.trajectory_plot.records()[0]
        np.testing.assert_allclose(record["series"][0]["values"], expected_series)
        assert record["y_label"] == "Value (nm**2)"
        host.wait(
            lambda: host.visible('[data-molsysviewer-datacard^="molsysmt-report-"] svg')
        )
        checks.append(
            "SASA source-indexed series has explicit area units in the real core card"
        )
        host.click("[data-clear]")
        host.wait(lambda: not host.visible("[data-report]"))
        script = """(() => {const svg=document.querySelector('[data-molsysviewer-datacard^="molsysmt-report-"] svg:has(polyline)'),p=svg.querySelector('polyline').getAttribute('points').trim().split(/\\s+/)[1].split(',').map(Number),point=svg.createSVGPoint();point.x=p[0];point.y=p[1];const s=point.matrixTransform(svg.getScreenCTM());svg.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:s.x,clientY:s.y}));return true;})()"""
        assert host.evaluate(script)
        host.wait(lambda: view.player.index == 1)
        host.wait(
            lambda: (
                host.evaluate(
                    "window.__molsysviewerDocsController.trajectory.getTrajectoryState().currentFrame"
                )
                == 1
            )
        )
        assert host.evaluate(colors_script) == expected
        checks.append(
            "A native DOM plot point navigates Python and Molstar without recoloring"
        )
        same(view.molsys, before)
        assert not host.bridge.failed_deliveries
        host.web.grab().save(str(out / "visuals.png"))
        (out / "report.json").write_text(
            json.dumps(
                {
                    "checks": checks,
                    "qt_platform": app.platformName(),
                    "scope": "Automated native Qt/WebEngine/Molstar theme, explicit core plot, DOM point navigation and source preservation; not human or installed acceptance.",
                },
                indent=2,
            )
            + "\n"
        )
    finally:
        host.window.close()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()


if __name__ == "__main__":
    main()
