/** First-canvas observations from the real widget and Mol* controller for #615. */
import { randomUUID } from 'node:crypto';
import { writeFile } from 'node:fs/promises';

export async function installInitialCanvasTrace(page, expectedAtoms) {
    await page.addInitScript(expectedAtoms => {
        let cell, target, controller, runTime, attempt, sceneSubscription, drawSubscription;
        const marks = {};
        let observerErrors = 0;

        const mark = name => {
            if (runTime !== undefined && marks[name] === undefined) {
                marks[name] = performance.now() - runTime;
            }
        };
        const observe = action => {
            try {
                action();
            } catch {
                observerErrors++;
            }
        };
        const release = () => {
            sceneSubscription?.unsubscribe();
            drawSubscription?.unsubscribe();
            sceneSubscription = drawSubscription = undefined;
        };
        const readScene = () => {
            if (controller.canvasHost?.querySelector('canvas')?.isConnected) mark('canvas_connected');
            if (controller.getStructureData()?.elementCount === expectedAtoms) mark('scene_registered');
        };
        const belongsToCell = element => {
            for (let node = element; node; node = node.parentElement ?? node.getRootNode()?.host) {
                if (node === cell) return true;
            }
            return false;
        };

        window.__initialCanvasTrace = {
            arm(initialCell, label) {
                cell = initialCell;
                attempt = label;
                runTime = performance.now();
                if (window.__molsysviewer_anywidget_runtime__) mark('runtime_available');
            },
            runtimeAvailable() {
                mark('runtime_available');
            },
            controllerStarted(element) {
                observe(() => {
                    if (!cell || target || !element.parentElement?.hasAttribute('data-molsysviewer-canvas-output')) return;
                    // AnyWidget can start rendering before attaching its output to the cell.
                    target = element;
                    mark('widget_mount_started');
                });
            },
            controllerReady(created, element) {
                observe(() => {
                    if (element !== target || controller) return;
                    controller = created;
                    mark('controller_ready');
                    const canvas = controller.plugin.canvas3d;
                    readScene();
                    if (!canvas) return;
                    sceneSubscription = controller.plugin.state.data.events.changed.subscribe(() => observe(readScene));
                    let subscribed = false;
                    drawSubscription = canvas.didDraw.subscribe(() => {
                        // BehaviorSubject emits its cached value during subscribe.
                        if (!subscribed) return;
                        observe(() => {
                            readScene();
                            if (marks.scene_registered === undefined || !controller.canvasHost?.isConnected) return;
                            if (canvas.reprCount.value <= 0 || canvas.boundingSphereVisible.radius <= 0) return;
                            mark('first_native_draw');
                            release();
                        });
                    });
                    subscribed = true;
                    mark('draw_observer_armed');
                });
            },
            finish() {
                const canvas = target?.querySelector('canvas');
                if (canvas?.isConnected) mark('canvas_connected');
                const rect = canvas?.getBoundingClientRect();
                let observedAtoms = null;
                observe(() => { observedAtoms = controller?.getStructureData()?.elementCount ?? null; });
                const data = {
                    attempt,
                    run_epoch_ms: runTime === undefined ? null : performance.timeOrigin + runTime,
                    elapsed_ms: runTime === undefined ? null : performance.now() - runTime,
                    marks: { ...marks },
                    expected_atoms: expectedAtoms,
                    observed_atoms: observedAtoms,
                    belongs_to_initial_cell: target ? belongsToCell(target) : null,
                    canvas: rect ? {
                        connected: canvas.isConnected,
                        x: rect.x, y: rect.y, width: rect.width, height: rect.height,
                    } : null,
                    viewport: { width: innerWidth, height: innerHeight, visible: !document.hidden },
                    output_errors: cell?.querySelectorAll('.jp-OutputArea-error').length ?? null,
                    observer_errors: observerErrors,
                };
                release();
                cell = target = controller = undefined;
                return data;
            },
        };
    }, expectedAtoms);
    const attempt = randomUUID();
    return cell => cell.evaluate(
        (element, label) => window.__initialCanvasTrace?.arm(element, label),
        attempt,
        { timeout: 750 },
    ).catch(() => undefined);
}

/** Persist before retiring the browser, while preserving the original test verdict. */
export async function saveInitialCanvasTrace(page, path, outcome) {
    let timer;
    const capture = page.evaluate(() => window.__initialCanvasTrace?.finish()).catch(() => null);
    try {
        const trace = await Promise.race([
            capture,
            new Promise(resolve => { timer = setTimeout(() => resolve(null), 750); }),
        ]);
        await writeFile(path, JSON.stringify({
            schema: 'molsysviewer.initial_canvas_trace@1',
            outcome,
            capture: trace ? (trace.attempt ? 'available' : 'unarmed') : 'unavailable',
            trace: trace ?? null,
        }, null, 2));
    } catch {
        console.warn('Could not write initial canvas diagnostic');
    } finally {
        clearTimeout(timer);
    }
}
