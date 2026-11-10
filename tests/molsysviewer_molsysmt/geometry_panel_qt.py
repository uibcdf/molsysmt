"""Actual native Qt Geometry UI receiving, without replacing its transport."""


def main():
    import json
    import sys
    import time
    from pathlib import Path

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
    base = msm.extract(seed.molsys, structure_indices=[0, 8, 3])
    xyz = puw.get_value(base.structures.coordinates, to_unit="nm").copy() + 10
    msm.set(
        base,
        coordinates=puw.quantity(xyz, "nm"),
        box=puw.quantity(np.repeat((5 * np.eye(3))[None], 3, axis=0), "nm"),
    )
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

    positions = "(() => {const c=window.__molsysviewerDocsController,s=c?.getStructureData();if(!s)return null;const out=[];for(const u of s.units)for(const a of u.elements)out[a]=Array.from(u.conformation.position(a,[0,0,0]));return out;})()"

    def receive(target_view=view, target_web=web, target_bridge=bridge):
        idle(target_bridge)
        expected = puw.get_value(
            target_view.molsys.structures.coordinates, to_unit="angstrom"
        )[target_view.player.index]
        wait(
            lambda: (
                (raw := evaluate(positions, target_web)) is not None
                and np.asarray(raw).shape == expected.shape
                and np.allclose(raw, expected, rtol=0, atol=1e-4)
            )
        )
        assert (
            evaluate(
                "window.__molsysviewerDocsController.hasPythonAuthority()", target_web
            )
            is True
        )
        assert (
            evaluate(
                "window.__molsysviewerDocsController.plugin.canvas3d.reprCount.value",
                target_web,
            )
            > 0
        )

    def open_geometry():
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
        wait(lambda: visible("[data-geometry-heading]"))

    try:
        receive()
        open_geometry()
        for task in ["rotate", "axes", "fit", "wrap", "cell"]:
            phase = task
            view.load(base, mode="replace")
            receive()
            fill("task", task)
            wait(lambda: visible(".msm-system [data-preview]"))
            if task != "cell":
                fill("source", "indices")
                fill("indices", "0,1,2,3,4,5,6,7,2")
            fill("scope", "indices")
            fill("frames", "2,0")
            fill("effect", "update")
            if task == "wrap":
                fill("wrap-compact", "atom")
            before = puw.get_value(
                view.molsys.structures.coordinates, to_unit="nm"
            ).copy()
            click(".msm-system [data-preview]")
            wait(lambda: visible(".msm-system [data-review]"))
            click(".msm-system [data-back]")
            wait(lambda: visible(".msm-system [data-preview]"))
            np.testing.assert_array_equal(
                puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), before
            )
            receive()
            checks.append(
                task + ": review and Back leave science and rendered model unchanged"
            )
            click(".msm-system [data-preview]")
            wait(lambda: visible(".msm-system [data-review]"))
            click(".msm-system [data-confirm]")
            wait(
                lambda: (
                    "up to date"
                    in (
                        evaluate(
                            'document.querySelector(".msm-system [data-status]")?.textContent'
                        )
                        or ""
                    )
                )
            )
            after = puw.get_value(
                view.molsys.structures.coordinates, to_unit="nm"
            ).copy()
            np.testing.assert_array_equal(after[1], before[1])
            if task == "rotate":
                expected = before.copy()
                for frame in [2, 0]:
                    center = before[frame, :8].mean(axis=0)
                    expected[frame, :8, :2] = (
                        before[frame, :8, :2] - center[:2]
                    ) @ np.array([[0, 1], [-1, 0]]) + center[:2]
                np.testing.assert_allclose(after, expected, atol=1e-12)
            elif task == "axes":
                for frame in [2, 0]:
                    centered = after[frame, :8] - after[frame, :8].mean(axis=0)
                    moments = centered.T @ centered / 8
                    np.testing.assert_allclose(
                        moments - np.diag(np.diag(moments)), 0, atol=1e-12
                    )
                    np.testing.assert_allclose(
                        after[frame, :8].mean(axis=0),
                        before[frame, :8].mean(axis=0),
                        atol=1e-12,
                    )
                    np.testing.assert_allclose(
                        np.linalg.norm(
                            after[frame, :8, None] - after[frame, None, :8], axis=-1
                        ),
                        np.linalg.norm(
                            before[frame, :8, None] - before[frame, None, :8], axis=-1
                        ),
                        atol=1e-12,
                    )
                np.testing.assert_array_equal(after[:, 8:], before[:, 8:])
            elif task == "fit":
                np.testing.assert_array_equal(after[:, 8:], before[:, 8:])
                assert np.linalg.norm(after[2, :8] - before[0, :8]) < np.linalg.norm(
                    before[2, :8] - before[0, :8]
                )
            elif task == "wrap":
                expected = before.copy()
                expected[np.ix_([2, 0], np.arange(8))] = np.mod(
                    before[np.ix_([2, 0], np.arange(8))], 5
                )
                np.testing.assert_allclose(after, expected, atol=1e-12)
            else:
                np.testing.assert_array_equal(after, before)
                boxes = puw.get_value(view.molsys.structures.box, to_unit="nm")
                np.testing.assert_allclose(
                    boxes[[2, 0]],
                    np.repeat((3 * np.eye(3))[None], 2, axis=0),
                    atol=1e-12,
                )
                np.testing.assert_allclose(boxes[1], 5 * np.eye(3), atol=1e-12)
            receive()
            checks.append(task + ": native reviewed edit reaches real Mol* coordinates")
            fill("effect", "result")
            fill("title", "Qt " + task + " result")
            click(".msm-system [data-preview]")
            wait(lambda: visible(".msm-system [data-review]"))
            click(".msm-system [data-confirm]")
            wait(lambda: visible(".msm-system [data-result]"))
            service = view.addons.manager.presentations
            wait(lambda service=service: len(service.records()) == 1)
            handle = next(iter(service._records))
            child = service.get(handle)
            child_runtime = service._records[handle]["runtime"]
            assert child is not view and child.molsys is not view.molsys
            assert not child_runtime["window"].isVisible()
            click(".msm-system [data-show-window]")
            wait(
                lambda child_runtime=child_runtime: child_runtime["window"].isVisible()
            )
            receive(
                child,
                child_runtime["webview"],
                child_runtime["webview"]._molsysviewer_qt_bridge,
            )
            np.testing.assert_array_equal(
                puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), after
            )
            checks.append(
                task
                + ": independent native result owns a real rendered window and preserves source"
            )
            child_runtime["window"].close()
            wait(
                lambda child=child, service=service: (
                    child.closed and not service.records()
                )
            )
            assert not view.closed
            receive()
            checks.append(
                task + ": result close releases ownership without closing source"
            )
        phase = "PCA"
        before = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
        click('[data-molsysviewer-addon-panel-tab="analysis"]')
        wait(lambda: visible(".msm-analysis [data-calculate]"))
        fill("task", "pca")
        wait(
            lambda: (
                not evaluate(
                    "document.querySelector('.msm-analysis [data-task]').disabled"
                )
            )
        )
        fill("source", "indices")
        fill("indices", "4,0,4")
        fill("structures", "indices")
        fill("structure-indices", "2,0,2")
        fill("pca-weighting", "custom")
        fill("pca-weights", "[1,2,3]")
        click(".msm-analysis [data-calculate]")
        wait(lambda: visible(".msm-analysis [data-report]"))
        flat = before[[2, 0, 2]][:, [4, 0, 4]].transpose(0, 2, 1).reshape(3, 9)
        centered = (flat - flat.mean(axis=0)) * np.sqrt(np.tile([1, 2, 3], 3))
        covariance = centered.T @ centered / 3
        rows = evaluate(
            "Array.from(document.querySelectorAll('.msm-analysis [data-rows] tr'),r=>Array.from(r.querySelectorAll('td'),x=>x.textContent))"
        )
        np.testing.assert_allclose(
            [float(row[1]) for row in rows],
            np.linalg.eigvalsh(covariance)[::-1],
            atol=1e-10,
        )
        receive()
        checks.append(
            "PCA: explicit weighted eigenvalues match independent population covariance"
        )
        fill("pca-component", "1")
        click(".msm-analysis [data-show-component]")
        wait(
            lambda: (
                "Coefficient"
                in (
                    evaluate(
                        "document.querySelector('.msm-analysis [data-columns]')?.textContent"
                    )
                    or ""
                )
            )
        )
        rows = evaluate(
            "Array.from(document.querySelectorAll('.msm-analysis [data-rows] tr'),r=>Array.from(r.querySelectorAll('td'),x=>x.textContent))"
        )
        vector = np.array([float(row[4]) for row in rows])
        np.testing.assert_allclose(
            covariance @ vector, vector * np.linalg.eigvalsh(covariance)[-1], atol=1e-9
        )
        np.testing.assert_allclose(vector @ vector, 1, atol=1e-8)
        assert [row[1] for row in rows] == ["X"] * 3 + ["Y"] * 3 + ["Z"] * 3
        checks.append(
            "PCA: dimensionless coefficient axes match the native Cartesian feature order"
        )
        click('.msm-analysis [data-rows] input[data-result-row="0"]')
        click(".msm-analysis [data-select-participants]")
        wait(lambda: tuple(view.active_selection.atom_indices) == (4,))
        click(".msm-analysis [data-focus-participants]")
        wait(
            lambda: (
                "Focused"
                in (
                    evaluate(
                        "document.querySelector('.msm-analysis [data-status]')?.textContent"
                    )
                    or ""
                )
            )
        )
        np.testing.assert_array_equal(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), before
        )
        receive()
        checks.append(
            "PCA: deliberate participant selection/focus preserves native and rendered coordinates"
        )
        click(".msm-analysis [data-clear]")
        wait(lambda: not visible(".msm-analysis [data-report]"))
        assert not view.trajectory_plot.records()
        checks.append(
            "PCA: Clear releases the mounted result without creating a trajectory projection"
        )
        web.grab().save(str(out / "geometry.png"))
        (out / "report.json").write_text(
            json.dumps(
                {
                    "checks": checks,
                    "provider_file": msm.__file__,
                    "qt_platform": app.platformName(),
                    "scope": "Actual native Qt window/WebEngine, shared Geometry UI and native Analysis/PCA. Review/cancel, selected structures, received updates, independent result windows, covariance/coefficients and participant ownership. Representative host receiving, not an installed package or human visual acceptance.",
                },
                indent=2,
            )
            + "\n"
        )
    finally:
        for handle in list(view.addons.manager.presentations._records):
            view.addons.manager.presentations.close(handle)
        window.close()
        base = None
        seed.close()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        app.processEvents()


if __name__ == "__main__":
    main()
