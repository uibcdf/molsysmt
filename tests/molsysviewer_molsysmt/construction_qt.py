"""Receive explicit native construction controls in an actual desktop WebEngine."""


def main():
    import faulthandler
    import json
    import sys
    import traceback
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

    import numpy as np
    from PySide6.QtCore import QCoreApplication, QEvent
    from shiboken6 import isValid

    import molsysmt as msm
    from molsysmt.native import Structures

    faulthandler.enable()
    from tests.molsysviewer_molsysmt.native_panel_host import NativePanelHost
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import same
    from tests.molsysviewer_molsysmt.test_solvation_tools import source

    out = Path(sys.argv[1])
    out.mkdir(exist_ok=True)
    phase = "empty construction"
    host = NativePanelHost(None, out, phase=lambda: phase)
    view, checks = host.view, []
    native_owners = [(host.window, host.web.page(), host.web.page().profile())]

    def field(key, value):
        selector = '[data-construction="' + key + '"]'
        host.wait(
            lambda: host.evaluate(
                f"(() => {{const e=document.querySelector({json.dumps(selector)});return !!e&&!e.disabled&&e.getClientRects().length>0;}})()"
            )
        )
        assert host.evaluate(
            f"(() => {{const e=document.querySelector({json.dumps(selector)});if(!e||e.disabled||!e.getClientRects().length)return false;e.value={json.dumps(value)};e.dispatchEvent(new Event('input',{{bubbles:true}}));e.dispatchEvent(new Event('change',{{bubbles:true}}));return true;}})()"
        ), key

    def prepare(task):
        host.fill("task", task)
        host.click("[data-prepare]")
        host.wait(lambda: host.visible("[data-result]"))
        host.wait(lambda: host.visible("[data-replace-review]"))
        records = view.addons.manager.presentations.records()
        runtime = view.addons.manager.presentations._records[records[-1]["id"]][
            "runtime"
        ]
        native_owners.append(
            (
                runtime["window"],
                runtime["webview"].page(),
                runtime["webview"].page().profile(),
            )
        )
        return view.addons.manager.presentations.get(records[-1]["id"]), records[-1][
            "id"
        ]

    def next_result():
        host.click("[data-new-result]")
        host.wait(lambda: not host.visible("[data-result]"))

    try:
        host.wait(lambda: host.bridge.ready)
        host.open_panel("chemistry")
        host.fill("task", "peptide")
        field("sequence", "AlaGly")
        child, handle = prepare("peptide")
        assert view.molsys is None
        assert (
            child.molsys.get_n_atoms()
            == msm.build.build_peptide(
                "amino_acids_3:AlaGly", from_naming_scheme="sequence"
            ).get_n_atoms()
        )
        checks.append("Explicit peptide construction starts from an empty desktop view")
        host.click("[data-show-window]")
        runtime = view.addons.manager.presentations._records[handle]["runtime"]
        host.wait(lambda: runtime["window"].isVisible())
        host.received(
            child, runtime["webview"], runtime["webview"]._molsysviewer_qt_bridge
        )
        next_result()
        checks.append(
            "The independent peptide window renders native molecular coordinates"
        )
        water, _ = prepare("water_cell")
        assert msm.get(water.molsys, n_waters=True) == 268
        host.click("[data-replace-review]")
        host.wait(lambda: host.visible("[data-replacement]"))
        host.click("[data-replace-back]")
        host.wait(lambda: not host.visible("[data-replacement]"))
        assert view.molsys is None
        host.click("[data-replace-review]")
        host.wait(lambda: host.visible("[data-replacement]"))
        host.click("[data-replace-apply]")
        host.wait(lambda: view.molsys is not None)
        host.received(view)
        assert view.molsys is not water.molsys
        next_result()
        checks.append(
            "Water-cell Back and deliberate replacement preserve independent owners"
        )
        phase = "seeded ion placement"
        before = msm.copy(view.molsys)
        host.fill("task", "ions")
        field("n_cations", "2")
        field("n_anions", "1")
        field("random_seed", "19")
        ions, _ = prepare("ions")
        expected = msm.build.add_ions(
            view.molsys, n_cations=2, n_anions=1, random_seed=19
        )
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(
                ions.molsys.structures.coordinates, to_unit="nm"
            ),
            msm.pyunitwizard.get_value(expected.structures.coordinates, to_unit="nm"),
        )
        same(view.molsys, before)
        next_result()
        checks.append("Native seeded whole-water ion placement preserves the source")
        phase = "declared assembly"
        assembly = msm.copy(view.molsys)
        assembly.structures = Structures(
            coordinates=assembly.structures.coordinates,
            box=assembly.structures.box,
            bioassembly={
                "declared": {
                    "chain_indices": [0],
                    "rotations": [np.eye(3), np.eye(3)],
                    "translations": msm.pyunitwizard.quantity(
                        [[0, 0, 0], [3, 0, 0]], "nm"
                    ),
                }
            },
        )
        view.load(assembly, mode="replace")
        host.received(view)
        host.fill("task", "bioassembly")
        field("assembly_name", "declared")
        result, _ = prepare("bioassembly")
        assert result.molsys.get_n_atoms() == 1608
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                result.molsys.structures.coordinates, to_unit="nm"
            )[:, 804:],
            msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit="nm")
            + [3, 0, 0],
            atol=1e-13,
        )
        next_result()
        checks.append("Deposited assembly choices produce the declared translated copy")
        phase = "independent solvation"
        view.load(source(), mode="replace")
        host.received(view)
        before = msm.copy(view.molsys)
        host.fill("task", "solvate")
        field("clearance", "0.35 nm")
        field("construction_forcefield", "AMBER14")
        field("random_seed", "19")
        result, _ = prepare("solvate")
        assert msm.get(result.molsys, n_waters=True) > 0
        same(view.molsys, before)
        assert not host.bridge.failed_deliveries
        checks.append(
            "Explicit solvent construction leaves the prepared solute unchanged"
        )
        host.web.grab().save(str(out / "construction.png"))
        (out / "report.json").write_text(
            json.dumps(
                {
                    "checks": checks,
                    "qt_platform": host.app.platformName(),
                    "scope": "Actual native Qt/WebEngine/Mol* five construction tasks and independent result window; source evidence, not human or installed qualification.",
                },
                indent=2,
            )
            + "\n"
        )
    except BaseException:
        traceback.print_exc()
        sys.stderr.flush()
        (out / "failure.json").write_text(
            json.dumps(
                {
                    "phase": phase,
                    "traceback": traceback.format_exc(),
                    "body": host.evaluate("document.body.innerText"),
                    "failed_deliveries": host.bridge.failed_deliveries,
                },
                indent=2,
            )
            + "\n"
        )
        raise
    finally:
        for row in list(view.addons.manager.presentations.records()):
            view.addons.manager.presentations.close(row["id"])
        host.window.close()

        def retired():
            QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
            host.app.processEvents()
            return (
                all(
                    not isValid(page) and not isValid(profile)
                    for _, page, profile in native_owners
                )
                and all(not isValid(window) for window, _, _ in native_owners[1:])
                and not host.window.isVisible()
            )

        host.wait(retired)
        (out / "retirement.json").write_text(
            json.dumps(
                {
                    "pages_and_profiles_destroyed": len(native_owners),
                    "result_windows_destroyed": len(native_owners) - 1,
                    "source_hidden": not host.window.isVisible(),
                }
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
