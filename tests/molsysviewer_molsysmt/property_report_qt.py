"""Native Qt/WebEngine/Mol* property report and source-participant receiving."""


def main():
    import json
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    import molsysviewer as msv
    import numpy as np
    from PySide6.QtCore import QCoreApplication, QEvent

    import molsysmt as msm
    from tests.molsysviewer_molsysmt.native_panel_host import NativePanelHost
    from tests.molsysviewer_molsysmt.test_aromatic_tools import caffeine_system
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import same

    out = Path(sys.argv[1])
    out.mkdir(exist_ok=True)
    with msv.demo["pentalanine"] as seed:
        base = msm.extract(seed.molsys, structure_indices=[0, 8, 3])
    before = msm.copy(base)
    phase = "initialization"
    host = NativePanelHost(base, out, phase=lambda: phase)
    view = host.view
    checks = []
    try:
        host.wait(lambda: host.bridge.ready)
        host.received(view)
        host.open_panel("analysis")
        host.click('[data-family="property"]')
        host.fill("source", "indices")
        host.fill("indices", "20,10,6,20")

        def calculate(task, success=True):
            host.fill("task", task)
            host.click(".msm-analysis [data-calculate]")
            host.wait(
                lambda: host.evaluate(
                    "!document.querySelector('.msm-analysis [data-calculate]').disabled"
                )
            )
            if success:
                host.wait(lambda: host.visible(".msm-analysis [data-report]"))
            else:
                host.wait(
                    lambda: host.evaluate(
                        "!!document.querySelector('.msm-analysis [data-status]').textContent"
                    )
                )
            return host.evaluate(
                "Array.from(document.querySelectorAll('.msm-analysis [data-rows] tr'),r=>Array.from(r.querySelectorAll('td'),c=>c.textContent))"
            )

        phase = "native properties"
        for task in (
            "mass",
            "reference_charge",
            "hydrophobicity",
            "polarity",
            "sequence",
            "bonds",
            "blocks",
        ):
            rows = calculate(task)
            assert rows or task == "bonds"
            same(view.molsys, before)
        checks.append(
            "Seven native property and molecular reports preserve source data"
        )
        phase = "observed secondary structure"
        host.fill("task", "secondary_structure")
        host.fill("secondary-mode", "full")
        host.fill("structures", "indices")
        host.fill("structure-indices", "2,0,2")
        rows = calculate("secondary_structure")
        groups = list(
            dict.fromkeys(
                map(
                    int,
                    msm.get(
                        view.molsys,
                        element="atom",
                        selection=[20, 10, 6, 20],
                        group_index=True,
                    ),
                )
            )
        )
        expected = msm.structure.get_secondary_structure(
            view.molsys, selection=groups, structure_indices=[2, 0, 2], simplified=False
        )
        assert rows == [
            [str(f), str(g), repr(str(expected[i, j]))]
            for i, f in enumerate([2, 0, 2])
            for j, g in enumerate(groups)
        ]
        same(view.molsys, before)
        checks.append(
            "Observed categorical DSSP retains group and repeated structure correspondence"
        )
        phase = "source participants"
        rows = calculate("mass")
        expected = msm.pyunitwizard.get_value(
            msm.physchem.get_mass(
                view.molsys, element="atom", selection=[20, 10, 6, 20]
            ),
            to_unit="dalton",
        )
        np.testing.assert_allclose([float(r[-1]) for r in rows], expected, rtol=5e-9)
        host.click('[data-result-row="0"]')
        host.click("[data-select-participants]")
        host.wait(lambda: view.active_selection.atom_indices == [20])
        host.click("[data-focus-participants]")
        host.wait(
            lambda: (
                "Focused"
                in host.evaluate(
                    "document.querySelector('.msm-analysis [data-status]').textContent"
                )
            )
        )
        assert view.player.index == 0
        checks.append(
            "Explicit property participant selection and focus preserve structure identity"
        )
        phase = "SASA"
        host.fill("task", "sasa")
        host.fill("structures", "indices")
        host.fill("structure-indices", "2,0,2")
        rows = calculate("sasa")
        expected = msm.pyunitwizard.get_value(
            msm.physchem.get_sasa(
                view.molsys,
                selection=[20, 10, 6, 20],
                structure_indices=[2, 0, 2],
                pbc=False,
                parallel=False,
                num_threads=1,
                use_gpu=False,
            ),
            to_unit="nm**2",
        )
        np.testing.assert_allclose(
            [float(r[-1]) for r in rows], expected.ravel(), rtol=5e-9
        )
        assert [int(r[0]) for r in rows] == [2] * 4 + [0] * 4 + [2] * 4
        checks.append(
            "SASA preserves explicit area units and repeated source structures"
        )
        phase = "ring prerequisites"
        calculate("rings", success=False)
        assert "Bond chemistry columns are missing" in host.evaluate(
            "document.querySelector('.msm-analysis [data-status]').textContent"
        )
        same(view.molsys, before)
        checks.append("Missing bond chemistry is refused without implicit preparation")
        phase = "declared rings"
        view.load(caffeine_system(), mode="replace")
        before = msm.copy(view.molsys)
        host.received(view)
        host.fill("structures", "current")
        host.fill("source", "all")
        rows = calculate("rings")
        assert sorted(r[-1] for r in rows) == sorted(
            ["1, 2, 3, 4, 5", "4, 5, 6, 8, 9, 11"]
        )
        same(view.molsys, before)
        checks.append("Native ring memberships retain known caffeine source atom sets")
        host.click("[data-clear]")
        host.wait(lambda: not host.visible(".msm-analysis [data-report]"))
        same(view.molsys, before)
        assert not host.bridge.failed_deliveries
        checks.append("Clear releases the report and preserves the molecular system")
        host.web.grab().save(str(out / "properties.png"))
        (out / "report.json").write_text(
            json.dumps(
                {
                    "checks": checks,
                    "qt_platform": host.app.platformName(),
                    "scope": "Automated native Qt/WebEngine/Mol* property, graph, SASA, participant and report lifetime receiving; not human or installed acceptance.",
                },
                indent=2,
            )
            + "\n"
        )
    finally:
        host.window.close()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        host.app.processEvents()


if __name__ == "__main__":
    main()
