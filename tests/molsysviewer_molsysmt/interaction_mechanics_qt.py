"""Native Qt sparse interaction tasks and reviewed mechanical observations."""


def main():
    import json
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    import molsysviewer as msv
    import numpy as np
    from PySide6.QtCore import QCoreApplication, QEvent

    import molsysmt as msm
    from molsysviewer_molsysmt._analysis_interactions import INTERACTION_METHODS
    from tests.molsysviewer_molsysmt.native_panel_host import NativePanelHost
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import same
    from tests.molsysviewer_molsysmt.test_interaction_analysis_panel import source

    out = Path(sys.argv[1])
    out.mkdir(exist_ok=True)
    phase = "initialization"
    host = NativePanelHost(source("hbonds"), out, phase=lambda: phase)
    view = host.view
    checks = []

    def status():
        return host.evaluate(
            "document.querySelector('.msm-analysis [data-status]').textContent"
        )

    def rows():
        return host.evaluate(
            "Array.from(document.querySelectorAll('.msm-analysis [data-rows] tr'),r=>Array.from(r.querySelectorAll('td'),c=>c.textContent))"
        )

    def calc():
        host.click("[data-calculate]")
        host.wait(lambda: host.visible("[data-report]"))
        host.wait(
            lambda: host.evaluate("!document.querySelector('[data-refresh]').disabled")
        )
        return rows()

    try:
        host.wait(lambda: host.bridge.ready)
        host.received(view)
        source_atoms = host.evaluate(
            """(() => {const c=window.__molsysviewerDocsController,l=c.atomIndicesToLoci([1]);return l.elements.flatMap(e=>Array.from(e.indices,i=>e.unit.model.atomicHierarchy.atomSourceIndex.value(e.unit.elements[i])));})()"""
        )
        assert source_atoms == [1], (
            f"Source atom 1 selects native source atoms {source_atoms}"
        )
        host.open_panel("analysis")
        host.click('[data-family="interactions"]')
        host.fill("source", "all")
        host.fill("structures", "all")
        for task, (family, name) in INTERACTION_METHODS.items():
            phase = task
            if family != "hbonds":
                view.load(source(family), mode="replace")
                host.received(view)
            original = msm.copy(view.molsys)
            host.fill("task", task)
            if not host.visible("[data-interaction-distance]"):
                host.click("[data-interaction-settings] details summary")
            for key in ["distance", "angle", "offset", "planarity"]:
                if host.visible("[data-interaction-" + key + "]"):
                    host.fill("interaction-" + key, "")
            args = dict(
                structure_indices="all", pbc=False, output_type="molsysmt.Interactions"
            )
            if family == "ionic":
                args["distance_threshold"] = ".4 nm"
                host.fill("interaction-distance", ".4 nm")
            if family == "pi_pi":
                for key, value in dict(
                    distance=".6 nm",
                    angle="30 degrees",
                    offset=".2 nm",
                    planarity=".02 nm",
                ).items():
                    args[key + "_threshold"] = value
                    host.fill("interaction-" + key, value)
            expected = getattr(getattr(msm.interactions, family), name)(
                view.molsys, **args
            )
            actual = calc()
            assert len(actual) == expected.n_interactions > 0
            assert [int(row[0]) for row in actual] == expected.to_page(limit=50)[
                "structure_indices"
            ].tolist()
            same(view.molsys, original)
            if family == "hbonds":
                host.click('[data-result-row="0"]')
                host.click("[data-select-participants]")
                host.wait(lambda: len(view.active_selection.atom_indices) == 3)
                host.fill("analysis-name", "qt-hbonds")
                host.click("[data-store-interactions]")
                host.wait(lambda: "Stored analysis qt-hbonds" in status())
                assert not view.interactions.tags()
                host.click("[data-add-interaction-set]")
                host.wait(lambda: len(view.interactions.tags()) == 1)
                visual = view.interactions.get(view.interactions.tags()[0])
                visual.hide()
                visual.show()
                host.click("[data-clear]")
                host.wait(lambda: not host.visible("[data-report]"))
                assert "qt-hbonds" in view.molsys.interactions
        checks.append(
            "All nine native interaction task controls retain sparse source indices and source data"
        )
        checks.append(
            "Hydrogen-bond science is stored separately from explicit core visualization and report retirement"
        )
        phase = "mechanical model"
        with msv.demo["pentalanine"] as seed:
            view.load(
                msm.extract(seed.molsys, structure_indices=[0, 8, 3]), mode="replace"
            )
        host.received(view)
        before = msm.copy(view.molsys)
        host.click('[data-family="mechanical"]')
        host.fill("task", "potential_energy")
        host.fill("structures", "current")
        assert host.evaluate("document.querySelector('[data-calculate]').disabled")
        host.click("[data-review-model]")
        host.wait(lambda: host.visible("[data-model-review]"))
        actual = calc()
        expected = msm.molecular_mechanics.get_potential_energy(
            msm.extract(view.molsys, structure_indices=[0]), platform="Reference"
        )
        np.testing.assert_allclose(
            float(actual[0][-1]),
            msm.pyunitwizard.get_value(expected, to_unit="kJ/mol"),
            rtol=5e-9,
        )
        host.fill("mechanical-platform", "CPU")
        assert host.evaluate("document.querySelector('[data-calculate]').disabled")
        host.fill("mechanical-platform", "Reference")
        checks.append(
            "Model review precedes complete-model energy and changed execution settings expire it"
        )
        phase = "atomic forces"
        host.fill("task", "forces")
        host.fill("source", "indices")
        host.fill("indices", "0")
        host.fill("structures", "indices")
        host.fill("structure-indices", "2,0,2")
        host.click("[data-review-model]")
        host.wait(lambda: host.visible("[data-model-review]"))
        actual = calc()
        assert [int(row[0]) for row in actual] == [2, 0, 2]
        expected = msm.molecular_mechanics.get_forces(
            view.molsys,
            selection=[0],
            structure_indices=[2, 0, 2],
            platform="Reference",
        )
        np.testing.assert_allclose(
            [[float(v) for v in row[2:]] for row in actual],
            msm.pyunitwizard.get_value(expected, to_unit="kJ/(mol*nm)")[:, 0],
            rtol=5e-9,
            atol=1e-8,
        )
        same(view.molsys, before)
        assert not host.bridge.failed_deliveries
        checks.append(
            "Atomic force components preserve repeated structure order, units and the complete source environment"
        )
        phase = "physical model"
        host.fill("task", "model_recipe")
        host.fill("structures", "current")
        host.click("[data-review-model]")
        host.wait(lambda: host.visible("[data-model-review]"))
        model_rows = calc()
        particle_row = next(
            row for row in model_rows if row[1] == "Compiled: n_particles"
        )
        assert int(particle_row[2]) == 62
        assert not host.visible("[data-mechanical-platform-label]")
        same(view.molsys, before)
        checks.append(
            "Native compiled physical settings retain explicit source scope without selecting a device"
        )
        host.web.grab().save(str(out / "interaction-mechanics.png"))
        (out / "report.json").write_text(
            json.dumps(
                dict(
                    checks=checks,
                    qt_platform=host.app.platformName(),
                    scope="Automated native Qt/WebEngine source receiving; not installed or human acceptance.",
                ),
                indent=2,
            )
            + "\n"
        )
    except BaseException:
        diagnostic = host.evaluate(
            """(() => {const c=window.__molsysviewerDocsController,s=c?.getStructureData();return {body:document.body.innerText,frame:c?.trajectory?.getTrajectoryState(),elements:s?.elementCount,atoms:s?.units?.flatMap(u=>Array.from(u.elements,a=>({a,source:u.model.atomicHierarchy.atomSourceIndex.value(a),position:Array.from(u.conformation.position(a,[0,0,0]))}))) };})()"""
        )
        (out / "failure-diagnostic.json").write_text(
            json.dumps(
                dict(
                    phase=phase,
                    actual=diagnostic,
                    expected=msm.pyunitwizard.get_value(
                        view.molsys.structures.coordinates, to_unit="angstrom"
                    )[0].tolist(),
                ),
                indent=2,
            )
        )
        raise
    finally:
        host.window.close()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        host.app.processEvents()


if __name__ == "__main__":
    main()
